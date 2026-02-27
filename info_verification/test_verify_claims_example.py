import asyncio
import sys
import os
from unittest.mock import patch, MagicMock
from datetime import datetime

# Allow running this script directly or as a module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from factchecker_v9.claim_processor import Claim
from factchecker_v9.claim_verifier import verify_claims_async, VerificationResult, VerificationResponse, VerificationResultSchema

async def mock_fetch_webpages(urls, use_docker=False):
    print(f"[Mock] Fetching webpages for URLs: {urls}")
    return {url: "Mocked content for " + url for url in urls}

async def mock_acompletion(*args, **kwargs):
    print("[Mock] LLM Completion called")
    # Simulate the structure expected by verify_claim_from_url_async
    # It expects: output.choices[0].message.content -> JSON string
    
    # We need to return a JSON that matches VerificationResponse schema
    # but verify_claim_from_url_async expects result in 'results' list.
    
    response_data = {
        "reliable": True,
        "reliable_explanation": "Source is reliable.",
        "results": [
            {
                "claim_index": 1,
                "explanation": "The claim is supported by the text.",
                "result": "supported"
            }
        ]
    }
    
    import json
    content = json.dumps(response_data)
    
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = content
    return mock_response

async def main():
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
        )
    ]

    # 2. Mock Dependencies
    # We mock:
    # - fetch_webpages: to strictly control network access
    # - litellm.get_supported_openai_params: to handle model params for mock model
    # - claim_verifier.limit_tokens_by_chunk: to avoid embedding/tokenization calls
    
    with patch('factchecker_v9.claim_verifier.fetch_webpages', side_effect=mock_fetch_webpages), \
         patch('litellm.acompletion', side_effect=mock_acompletion), \
         patch('litellm.get_supported_openai_params', return_value={}), \
         patch('factchecker_v9.claim_verifier.limit_tokens_by_chunk', return_value="Mocked context"):
        
        # 3. Run the function
        results = await verify_claims_async(claims, model="mock-model")

    # 4. Print Results
    print("\nVerification Results:")
    for verified_claim in results:
        print(f"Claim: {verified_claim.claim.claim}")
        status, explanation = verified_claim.final_result_and_explanation()
        print(f"Status: {status}")
        print(f"Explanation: {explanation}")
        print("-" * 20)

if __name__ == "__main__":
    asyncio.run(main())
