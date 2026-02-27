from typing import Optional, List, Union
from pydantic import BaseModel, Field
import litellm
import json
import os
from collections import defaultdict
from typing import Optional, Union
from .web_downloader import fetch_webpages
from .source_filter import limit_tokens_by_chunk
from .report_utils import clean_url
from .claim_processor import Claim
import asyncio
from pprint import pprint
from retry import retry


ALLOWED_RESULTS = {"supported", "not_supported", "error"}


class VerificationResultSchema(BaseModel):
    claim_index: int = Field(..., ge=1, description="1-based index of the claim")
    explanation: str = Field(..., description="Explanation of the verification result.")
    result: str = Field(..., description="The verification result: 'supported', 'not_supported', or 'conflict'.")

class VerificationResponse(BaseModel):
    reliable_explanation: str = Field(..., description="Explanation of the reliability judgment.")
    reliable: bool = Field(..., description="Whether the URL is from a reliable source.")
    results: List[VerificationResultSchema]

class VerificationResult(BaseModel):
    claim: str = Field(..., description="The claim to be verified.")
    explanation: str = Field(..., description="Explanation of the verification result.")
    result: str = Field(..., description="The verification result.")
    url: str = Field(..., description="The URL where the claim was found.")
    reliable_explanation: str = Field(..., description="Explanation of the reliability judgment.")
    reliable: bool = Field(..., description="Whether the URL is from a reliable source.")

def load_prompt(filename: str) -> str:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "prompts", filename)
    if not os.path.exists(path):
        # Fallback for different CWD scenarios
        path = os.path.join("prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

async def verify_claim_from_url_async(
    claims: list[Claim], context: str, url: str, model: str = "gpt-4.1-mini",
    limit_tokens: bool = True, top_k: int = 2, chunk_size: int = 1000,
    return_output: bool = False, method: str = "openai",
    sentence_transformer_model: Optional[str] = None,
    debug_ctx: Optional[dict] = None,
) -> list[VerificationResult]:
    
    debug_ctx = debug_ctx or {"url": url, "batch_id": None}
    joined_claims = "\n".join([f"{i + 1}. {claim.claim}" for i, claim in enumerate(claims)])
    claim_queries = [claim.claim for claim in claims]

    if limit_tokens:
        context = await limit_tokens_by_chunk(
            queries=claim_queries,
            content=context,
            chunk_size=chunk_size,
            top_k=top_k,
            method=method,
            sentence_transformer_model=sentence_transformer_model,
        )

    prompt_template = load_prompt("claim_verification_v2.txt")
    prompt = prompt_template.format(url=url, claims=joined_claims, context=context)

    max_retries = 3
    
    for attempt in range(1, max_retries + 1):
        try:
            output = await litellm.acompletion(
                messages=[{"role": "user", "content": prompt}],
                **get_model_kwargs(
                    model_id=model,
                    max_tokens=4096,
                    temperature=0.0,
                    reasoning_effort='low'
                ),
                response_format=VerificationResponse,
            )

            raw = output.choices[0].message.content
            data = json.loads(raw)
            
            # Convert to internal objects
            results = []
            for r in data.get("results", []):
                idx = r.get("claim_index", 0) - 1
                result = r['result']
                if result == "conflict":
                    result = "not_supported"
                    
                if 0 <= idx < len(claims):
                    results.append(VerificationResult(
                        claim=claims[idx].claim,
                        result=result,
                        explanation=r["explanation"],
                        url=url,
                        reliable=data['reliable'],
                        reliable_explanation=data['reliable_explanation']
                    ))

            if return_output:
                return results, output
            return results

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt == max_retries:
                return [
                     VerificationResult(
                        claim=c.claim,
                        result="error",
                        explanation=f"Verification failed: {str(e)}",
                        url=url,
                        reliable=False,
                        reliable_explanation=""
                    ) for c in claims
                ], None

def get_model_kwargs(
    model_id: str,
    max_tokens: int,
    temperature: float = 0,
    max_completion_tokens: int = 128000,
    reasoning_effort: str = 'low'
) -> dict:
    params = litellm.get_supported_openai_params(model=model_id)
    out_params = {}
    if "max_completion_tokens" in params:
        out_params = {
            "model": model_id,
            "max_completion_tokens": max_completion_tokens,
        }
    else:
        out_params = {
            "model": model_id,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

    if "reasoning_effort" in params:
        out_params["reasoning_effort"] = reasoning_effort
    return out_params
#여기.
async def batch_verify_claim_from_url_async(
    claims: list[Claim], context: str, url: str, model: str = "gpt-4.1",
    limit_tokens: bool = True, top_k: int = 2, chunk_size: int = 1000, batch_size: int = 20
):
    tasks = []
    for batch_id, i in enumerate(range(0, len(claims), batch_size)):
        batch_claims = claims[i:min(i + batch_size, len(claims))]
        tasks.append(
            verify_claim_from_url_async(
                batch_claims,
                context=context,
                url=url,
                model=model,
                limit_tokens=limit_tokens,
                top_k=top_k,
                chunk_size=chunk_size,
                # Debug context
                debug_ctx={"url": url, "batch_id": batch_id}
            )
        )

    results = await asyncio.gather(*tasks)
    verification_results = []
    for batch_results in results:
        # If return_output was False, verify_claim_from_url_async returns just list[VerificationResult]
        # In this loop we assume it returns list[VerificationResult].
        if isinstance(batch_results, tuple):
             # Handle return_output=True case if needed, but here default is False
             batch_results = batch_results[0]
        verification_results.extend(batch_results)
    return verification_results

##### VerifiedClaim Definition #####
result_priority = [
    "supported",
    "not_supported",
    "error",
    "unverified",
]
result_priority = {result: i for i, result in enumerate(result_priority)}

class VerifiedClaim(BaseModel):
    claim: Claim = Field(..., description="The claim to be verified.")
    verifications: list[VerificationResult] = Field(
        ..., description="The verifications for the claim."
    )

    def final_result_and_explanation(self) -> tuple[str, str]:
        if len(self.verifications) == 0:
            return "unverified", "This claim has not been verified."
        if len(self.verifications) == 1:
            return self.verifications[0].result, self.make_explanation()

        # Simple logic: prioritize supported > not_supported > error
        best_result = min(
            self.verifications,
            key=lambda x: result_priority.get(x.result, result_priority.get("not_supported", 1))
        )
        return best_result.result, self.make_explanation()

    def make_explanation(self) -> str:
        lines = []
        for i, v in enumerate(self.verifications):
            try:
                badge = make_badge(v.result) 
                url = getattr(v, "url", "<no-url>")
                expl = getattr(v, "explanation", "")
                lines.append(f"- {badge}: {expl} [Source]({url})")
            except Exception as e:
                url = getattr(v, "url", "<no-url>")
                lines.append(f"- [ERROR] {e} url={url}")

        return "\n" + "\n".join(lines)

badge_dict = {
    "supported": ":green-badge[:material/check: Supported: {0}]",
    "not_supported": ":orange-badge[:material/help: Not Supported: {0}]",
    "error": ":violet-badge[:material/error: Error: {0}]",
    "unverified": ":grey-badge[:material/pending: Unverified: {0}]",
}

def make_badge(badge_type: str, badge_text: str = "") -> str:
    if badge_type in ("partially_supported", "conflict"):
        badge_type = 'not_supported'
    if badge_type not in badge_dict:
        return f":grey-badge[:material/help: {badge_type}: {badge_text}]"
    return badge_dict[badge_type].format(badge_text)

async def verify_claims_async(
    claims: list[Claim], model: str = "gpt-4.1", return_context: bool = False
) -> Union[list[VerifiedClaim], tuple[list[VerifiedClaim], dict[str, str]]]:
    urls = set()
    for c in claims:
        if c.citations:
            urls.update([clean_url(url) for url in c.citations])
        if c.implicit_citations:
            urls.update([clean_url(url) for url in c.implicit_citations])

    use_docker = os.environ.get("CRAWL4AI_DOCKER") == "true"
    contexts = await fetch_webpages(urls, use_docker=use_docker)

    claims_by_url = defaultdict(list)
    claim_to_claim = {c.claim: VerifiedClaim(claim=c, verifications=[]) for c in claims}
    context_informations = {}

    for claim in claims:
        citations = claim.citations or []
        if claim.implicit_citations:
            citations.extend(claim.implicit_citations)

        for url in set(citations):
            url = clean_url(url)
            claims_by_url[url].append(claim)

    async def process_url(url: str):
        url = clean_url(url)
        context = contexts.get(url, "") # Use .get for safety
        claim_list = claims_by_url[url]
        
        if not context or context.startswith("Failed to fetch"):
            for claim_obj in claim_list:
                if claim_obj.claim in claim_to_claim:
                    claim_to_claim[claim_obj.claim].verifications.append(
                        VerificationResult(
                            claim=claim_obj.claim,
                            result="error",
                            explanation="Failed to fetch content from URL",
                            url=url,
                            numeric_error=None,
                            relavant_context=None,
                            corresponding_scope=None,
                            reliable=False,
                            reliable_explanation="URL fetch failed or content too short",
                        )
                    )
            context_informations[url] = {
                "context": context,
                "reliable": False,
                "reliable_explanation": "URL fetch failed or content too short",
            }
            return
    
        # Updated signature: returns only verification_results
        results = await batch_verify_claim_from_url_async(
            claim_list, context=context, url=url, model=model,
        )

        for result in results:
            # find matching claim object by text
            if result.claim in claim_to_claim:
                claim_to_claim[result.claim].verifications.append(result)

        if len(results) == 0:
            reliable, reliable_explanation = False, "No results"
        else:
            reliable, reliable_explanation = results[0].reliable, results[0].reliable_explanation

        context_informations[url] = {
            "context": context,
            "reliable": reliable,
            "reliable_explanation": reliable_explanation
        }

    await asyncio.gather(*[process_url(url) for url in urls])

    if return_context:
        return list(claim_to_claim.values()), context_informations
    else:
        return list(claim_to_claim.values())


def claim_by_position(claims: list[Claim]):
    position_to_claim = defaultdict(list)
    for claim in claims:
        position_to_claim[claim.position].append(claim)

    return position_to_claim


def backtrack_claims(claims: list[Claim]) -> list[Claim]:
    """
    Backtracks claims to find their source URLs.
    Logic:
    1. Cross-references: If a claim refers to another claim (e.g. "L1.S1"), it inherits citations.
    2. Same-line backtracking: If a claim has no citations, it inherits citations from subsequent claims in the same line.
       Example: "Sentence A. Sentence B [1]." -> Sentence A inherits [1].
    """
    # 1. Handle Same-line Backtracking
    # Group claims by Line
    line_to_claims = defaultdict(list)
    for claim in claims:
        # Parse position "Lx.Sy"
        try:
            line_part = claim.position.split('.')[0] # "Lx"
            line_to_claims[line_part].append(claim)
        except:
            continue

    # Process each line
    for line, line_claims in line_to_claims.items():
        # Sort by sentence index (S1, S2, ...)
        # Assuming format "Lx.Sy", we extract y.
        def get_sent_idx(c):
            try:
                return int(c.position.split('.S')[1].split(':')[0])
            except:
                return 0
        
        line_claims.sort(key=get_sent_idx)

        # Iterate backwards
        # If current claim has citations, it becomes the active citation source.
        # If current claim has NO citations, it inherits active citations.
        # If current claim has citations, they are added to the active set? 
        # Usually, a citation applies to the preceding block.
        # So we collect citations from the end.
        
        active_citations = []
        
        for i in range(len(line_claims) - 1, -1, -1):
            claim = line_claims[i]
            
            # If claim has explicit citations, these become the new active context for preceding sentences
            if claim.citations:
                active_citations = list(claim.citations) # Copy
            
            # If claim has implicit citations (from cross-ref), those might also count?
            # Let's separate "explicit" from "implicit".
            # Standard rule: "Statement [1]." -> [1] covers Statement.
            # "Statement A. Statement B [1]." -> [1] covers B and likely A.
            
            # If claim has NO citations (explicit or implicit), it inherits active_citations
            if not claim.citations and not claim.implicit_citations:
               if active_citations:
                   claim.implicit_citations = list(active_citations)
            
            # If claim ALREADY has citations, those block the flow of previous active citations?
            # E.g. "Sta A [1]. Sta B [2]." -> A should verify against [1], not [2].
            # So if we encounter a claim WITH citations, we update the active_citations to THAT.
            # (which we did above: if claim.citations: active = claim.citations)
            # This correctly handles "A [1]. B [2]." -> B uses [2]. A uses [1].

    # 2. Handle Cross-references
    position_to_claim = claim_by_position(claims)
    for claim in claims:
        if claim.cross_references:
            for cross_ref in claim.cross_references:
                cross_ref_claims = position_to_claim.get(cross_ref, [])
                for cross_ref_claim in cross_ref_claims:
                    if claim.implicit_citations is None:
                        claim.implicit_citations = []
                    # Add citations from the referenced claim
                    if cross_ref_claim.citations:
                        claim.implicit_citations.extend(cross_ref_claim.citations)
                    if cross_ref_claim.implicit_citations:
                        claim.implicit_citations.extend(cross_ref_claim.implicit_citations)

    # 3. Propagate Internal Status (Type Internal Propagation)
    # If a claim has NO citations, check if all its sources (cross-refs or same-line successors) are Type D or E.
    # If so, convert it to Type E.
    # Repeat a few times to propagate chains.
    # 3. Force Convert Unverified B/C to Type D (User Request)
    # If a claim of Type B or C has no citations (explicit or implicit) after backtracking,
    # assume it is an internal/structural statement and convert to Type D.
    for claim in claims:
        if claim.claim_type in ["B", "C"]:
            if not claim.citations and not claim.implicit_citations:
                claim.claim_type = "D"

def replace_claims_to_url(
    claims: list[Claim], citations: dict[str, str]
) -> list[Claim]:
    for claim in claims:
        if claim.citations:
            claim.citations = [citations.get(c, c) for c in claim.citations]
        if claim.implicit_citations:
            claim.implicit_citations = [
                citations.get(c, c) for c in claim.implicit_citations
            ]



async def test_verify_claims_async():
    from pprint import pprint
    print("Starting verify_claims_async test...")

    # 1. Setup Sample Data
    claims = [
        Claim(
            position="L1.S1",
            claim="Python is a popular programming language.",
            claim_type="A", # Fact
            rationale="General knowledge",
            numeric=False,
            citations=["https://www.python.org/doc/"],
            implicit_citations=[],
            cross_references=[]
        ),
        Claim(
            position="L1.S2",
            claim="Python is a popular programming language.",
            claim_type="A", # Fact
            rationale="General knowledge",
            numeric=False,
            citations=["https://medium.com/helloworldexamplehowareyou?"], # 404 not found page
            implicit_citations=[],
            cross_references=[]
        ),
        Claim(
            position="L1.S3",
            claim="Networks among scientific papers are dense.",
            claim_type="A", # Fact
            rationale="General knowledge",
            numeric=False,
            citations=["https://www.science.org/doi/10.1126/science.149.3683.510"], # Captcha page
            implicit_citations=[],
            cross_references=[]
        ),
    ]
    
    results = await verify_claims_async(claims, model="gpt-5-mini")

    # 4. Print Results
    print("\nVerification Results:")
    for verified_claim in results:
        pprint(verified_claim.dict())
        print("-" * 20)


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    import asyncio
    from .report_utils import split_references, extract_references

    asyncio.run(test_verify_claims_async())

    # async def amain_testset():
    #     filename = "deep_research_samples/chatexaone_fast_1"
    #     processed_md = f"{filename}_processed.md"
    #     # If processed_md exists, use it to ensure lines match? 
    #     # But we need references from the original or processed. 
    #     # Typically refs are at bottom.
        
    #     md_file = f"{filename}.md"
    #     print(f"Reading {md_file}...")
    #     with open(md_file, "r") as f:
    #         report = f.read()
    #         report, references_text = split_references(report)
    #         citations = extract_references(references_text)

    #     print(f"Found {len(citations)} citations.")
    #     # pprint(citations)

    #     claims_file = f"{filename}_claims_v5.json"
    #     print(f"Reading {claims_file}...")
    #     with open(claims_file, "r") as f:
    #         data = json.load(f)
    #         claims = [Claim(**claim) for claim in data]
        
    #     print(f"Loaded {len(claims)} claims.")

    #     # Resolve citations
    #     backtrack_claims(claims)
    #     replace_claims_to_url(claims, citations)
        
    #     print(f"Verifying claims... (Model: gpt-4.1-mini)")
    #     # Run verification
    #     results, ctx_info = await verify_claims_async(claims, model="gpt-4.1-mini", return_context=True)
        
    #     # Save results
    #     output_file = f"{filename}_results_v5.json"
        
    #     # clean ctx info for saving
    #     for url in ctx_info:
    #         ctx_info[url]["context"] = f"<hidden length={len(ctx_info[url]['context'])}>"

    #     output_data = {
    #         "verifications": [x.model_dump() for x in results],
    #         "citations": citations,
    #         "context_info": ctx_info
    #     }
        
    #     with open(output_file, "w") as f:
    #         json.dump(output_data, f, indent=2, ensure_ascii=False)
            
    #     print(f"Saved results to {output_file}")

    # asyncio.run(amain_testset())
