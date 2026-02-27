from .report_utils import split_references, extract_references
from .claim_processor import extract_claims, add_line_sent_to_report
from .claim_verifier import verify_claims_async, backtrack_claims, replace_claims_to_url
from .eval_metrics import compute_metrics
# from .directquote_detector import detect_direct_quote
# from .fairuse_detector import calculate_fairuse
from tqdm import tqdm
import asyncio
import time
import json


async def evaluate_report(report: str, batch_size=20, extract_model: str = "gpt-5-mini", verify_model: str = "gpt-4.1"):
    """
    Evaluate the report by extracting claims, verifying them, and adding line numbers to the report.

    Args:
        report (str): The report text to evaluate.

    Returns:
        str: The processed report with claims verified and line numbers added.
    """
    start_time = time.time()
    
    # Split the report into main content and references section
    report, references_section = split_references(report)
    report = report.strip()

    # Extract claims from the report
    references = extract_references(references_section)
    if not references:
        references = extract_references(report)

    # Add line numbers to the report and extract sentences
    # This will also return a dictionary mapping line numbers to sentences
    # and a report with line numbers prefixed to each sentence.
    # Example: "L1. S1: Sentence 1" for line 1
    report_line_prefixed, line_sents = add_line_sent_to_report(report)
    line_sentences = [
        f"L{line_number}.S{idx+1}: {s}"
        for line_number, sents in line_sents.items()
        for idx, s in enumerate(sents)
    ]

    # Process the report in batches for efficiency
    print(f"Starting claim extraction for {len(line_sentences)} sentences in {len(range(0, len(line_sentences), batch_size))} batches...")
    batch_start = time.time()
    
    tasks = []
    for i in range(0, len(line_sentences), batch_size):
        batch_sentences = (
            line_sentences[i : i + batch_size]
            if i + batch_size <= len(line_sentences)
            else line_sentences[i:]
        )
        if not batch_sentences:
            continue
        tasks.append(extract_claims(report_line_prefixed, batch_sentences, model=extract_model))

    all_claims = await asyncio.gather(*tasks)
    all_claims = [claim for sublist in all_claims for claim in sublist]
    
    batch_end = time.time()
    print(f"✓ Claim extraction completed in {batch_end - batch_start:.2f}s - Found {len(all_claims)} claims")

    # Backtrack claims to find their source URLs for B2 type of claims
    backtrack_claims(all_claims)

    # Replace citation indices in claims with actual URLs from the references
    replace_claims_to_url(all_claims, references)

    # Verify claims asynchronously
    print(f"Starting claim verification for {len(all_claims)} claims...")
    verify_start = time.time()
    
    verified_claims, contexts = await verify_claims_async(all_claims, model=verify_model, return_context=True)
    
    verify_end = time.time()
    print(f"✓ Claim verification completed in {verify_end - verify_start:.2f}s")

    # fairuse_results = calculate_fairuse(report)
    # fairuse_results.pop("citation_sentences_list", None)  # Remove this key if not needed

    citation_to_contexts = {
        citation: contexts.get(url, {}).get("context", "")
        for citation, url in references.items()
    }
    
    # print("Starting direct quote detection...")
    # quote_start = time.time()
    
    # direct_quote_results = await detect_direct_quote(
    #     report, citation_to_contexts, similarity_threshold=0.8
    # )
    
    # quote_end = time.time()
    # print(f"✓ Direct quote detection completed in {quote_end - quote_start:.2f}s")
    
    metrics = compute_metrics(verified_claims, references=references, context_informations=contexts)
    # metrics['raw']['quote']=direct_quote_results['results']
    # metrics["ethics_compliance"] = direct_quote_results['ethics_compliance']

    total_time = time.time() - start_time
    print(f"🎉 Total evaluation completed in {total_time:.2f}s")

    return dict(
        report=report_line_prefixed,
        references=references,
        claims=verified_claims,
        reference_informations=contexts,
        metrics=metrics
    )


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    # file = "deep_research_samples/openai_o3-pro_6_cleaned.md"
    # file = "deep_resea`rch_samples/gemini-2.5-pro_cleaned_6_0706.md"
    # file = "deep_research_samples/chatexaone_deepresearch_1.md"
    # file = "deep_research_samples/chatexaone_fast_1.md"

    async def main():
        files = [
            "data/test/economics-gemini-2.5-pro_deep_1.md",
            # "data/micro1_economics/1/gemini-2.5-pro_deep_1.md",
            # "data/micro1_economics/1/claude_opus4.1_deep_1.md",
            # "data/micro1_economics/1/chatexaone_251208_deepresearch_1.md",
            # "data/micro1_economics/1/gpt5_deep_1.md",
        ]
        
        for file in files:
            print(f"Processing {file}...")
            try:
                with open(file, "r", encoding="utf-8") as f:
                    report = f.read()

                result = await evaluate_report(report, batch_size=10)

                # Compute metrics based on the verified claims and references
                metrics = result["metrics"] 
                report_line_prefixed = result.pop("report")

                with open(file.replace(".md", "_processed.md"), "w", encoding="utf-8") as f:
                    f.write(report_line_prefixed)

                result["claims"] = [claim.model_dump() for claim in result["claims"]]

                with open(file.replace(".md", "_metrics.json"), "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)
            except Exception as e:
                print(f"Error processing {file}: {e}")

    asyncio.run(main())
