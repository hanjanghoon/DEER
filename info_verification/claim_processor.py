from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import litellm
import json
from tqdm import tqdm
from pprint import pprint
from nltk import sent_tokenize
from collections import defaultdict
import re
from .report_utils import split_references
from retry import retry
import os

class Claim(BaseModel):
    position: str = Field(
        ...,
        description="Position of the claim in the report, e.g., 'L1.S1' for line 1, sentence 1.",
    )
    claim: str = Field(
        ..., description="The claim statement extracted from the report."
    )
    claim_type: str = Field(
        ..., description="Type of the claim: 'A', 'B', 'C', 'D', 'E', 'F'."
    )
    rationale: str = Field(
        ..., description="Rationale for the claim type classification."
    )
    numeric: bool = Field(
        ..., description="Whether the claim includes numeric information."
    )
    citations: Optional[List[str]] = Field(
        None, description="List of citations supporting the claim."
    )
    implicit_citations: Optional[List[str]] = Field(
        None, description="List of implicit citations that support the claim, if any."
    )
    cross_references: Optional[List[str]] = Field(
        None,
        description="List of positions in the report that support the claim, formatted as 'Lx.Sy' where x is the line number and y is the sentence number.",
    )


class ClaimExtractionResponse(BaseModel):
    claims: List[Claim] = Field(
        ..., description="List of claims extracted from the report."
    )


def load_prompt(filename: str) -> str:
    """Load prompt from prompts directory."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "prompts", filename)
    if not os.path.exists(path):
        # Fallback for different CWD scenarios
        path = os.path.join("prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def add_line_sent_to_report(report_text: str) -> str:
    lines = report_text.split("\n\n")
    new_lines = []
    line_sents = defaultdict(list)

    for i, line in enumerate(lines):
        if line := line.strip():
            if line == "## References" or line == "Citations:":
                break
            if line.startswith("#"):
                if "\n" in line:
                    lines = line.split("\n", 1)
                    new_lines.append(lines[0].strip())
                    line = lines[1].strip()
                else:
                    new_lines.append(line)
                    continue
            sents = sent_tokenize(line)
            for j, sent in enumerate(sents):
                new_lines.append(f"L{i+1}.S{j+1}: {sent}")
                line_sents[i + 1].append(sent)

            new_lines.append("")

    return "\n".join(new_lines), line_sents


@retry(tries=3, exceptions=(json.JSONDecodeError,))
async def extract_claims(
    report_text: str, target_sentenecs: list[str], model: str = "gpt-5-mini"
) -> List[Claim]:

    prompt_content = load_prompt("claim_classification_v10.txt")
    
    # Prepend schema instruction to ensure JSON output matches the Pydantic model
    system_prompt = (
        f"{prompt_content}\n\n"
        "IMPORTANT: You must output a JSON object with a 'claims' field containing a list of objects "
        "matching the schema provided in the function definition (ClaimExtractionResponse). "
        "Do not include any text outside the JSON object."
    )

    user_text = (
        f"# Report Excerpt\n\n{report_text}\n\n# Target Sentences\n\n"
        + "\n".join(target_sentenecs)
    )

    response = await litellm.acompletion(
        model=model, 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        response_format=ClaimExtractionResponse,
        max_completion_tokens=16384,
        reasoning_effort='low'
    )

    content = response.choices[0].message.content
    
    # Empty check
    if not content or content.strip() == "":
        return []

    claims_data = json.loads(content)
    claims = [Claim(**claim) for claim in claims_data["claims"]]

    def check_citation_validity(citation):
        return all(c.isdigit() or c == '-' for c in citation.strip()) and len(citation.strip()) > 0

    for claim in claims:
        # Filter valid citations
        if claim.citations:
            cleaned_citations = []
            for c in claim.citations:
                clean_c = c.strip().strip("[]")
                if check_citation_validity(clean_c):
                    cleaned_citations.append(clean_c)
            claim.citations = cleaned_citations
        else:
            claim.citations = []

        if claim.implicit_citations:
            cleaned_implicit = []
            for c in claim.implicit_citations:
                clean_c = c.strip().strip("[]")
                if check_citation_validity(clean_c):
                    cleaned_implicit.append(clean_c)
            claim.implicit_citations = cleaned_implicit
        else:
            claim.implicit_citations = []

        # Clear citations for non-cited types
        if claim.claim_type not in ["A", "B", "C"]: 
            # Note: v10 uses A, B, C, D, E, F. 
            # Logic: If type is NOT A/B/C, it likely shouldn't have external citations.
            # A, B, C are the ones with references.
            if claim.claim_type not in ["A", "B", "C"]:
                claim.citations = []
                claim.implicit_citations = []
        
    return claims

if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    import asyncio

    for file in [
        "deep_research_samples/chatexaone_fast_1"
    ]:  # , "testset/sample_02", "testset/sample_03"]:
        with open(f"{file}.md") as f:
            report_text = f.read()
            report_text, references_section = split_references(report_text)

        report_text, line_sents = add_line_sent_to_report(report_text)
        with open(f"{file}_processed.md", "w") as f:
            f.write(report_text)

        line_sentences = [
            f"L{line_number}.S{idx+1}: {s}"
            for line_number, sents in line_sents.items()
            for idx, s in enumerate(sents)
        ]
        batch_size = 20

        # 모든 배치들을 준비
        batches = []
        for i in range(0, len(line_sentences), batch_size):
            batch_sentences = (
                line_sentences[i : i + batch_size]
                if i + batch_size <= len(line_sentences)
                else line_sentences[i:]
            )
            if batch_sentences:
                batches.append(batch_sentences)

        # 비동기로 모든 배치를 동시에 처리
        async def process_all_batches():
            tasks = [
                extract_claims(report_text, batch, model="gpt-5-mini")
                for batch in batches
            ]
            batch_results = await asyncio.gather(*tasks)
            all_claims = []
            for claims in batch_results:
                all_claims.extend(claims)
            return all_claims

        all_claims = asyncio.run(process_all_batches())

        print(f"Extracted {len(all_claims)} claims:")
        with open(f"{file}_claims_v5.json", "w") as f:
            json.dump(
                [claim.model_dump() for claim in all_claims],
                f,
                indent=2,
                ensure_ascii=False,
            )
