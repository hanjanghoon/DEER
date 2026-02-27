import re
import numpy as np
from collections import defaultdict
from typing import List, Dict, Tuple, Optional
from pprint import pprint
from nltk import sent_tokenize


def calculate_fairuse(text: str) -> Dict[str, float]:
    """
    문장 기반 인용 비율 계산
    """
    # 문장 분리
    # sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = sent_tokenize(text.strip())
    
    # 인용 포함 문장 식별
    citation_pattern = re.compile(r'\[\d+\]')
    citation_sentences = [s for s in sentences if citation_pattern.search(s)]
    
    total_sentences = len(sentences)
    citation_sentence_count = len(citation_sentences)
    
    # 비율 계산
    citation_sentence_ratio = citation_sentence_count / total_sentences if total_sentences > 0 else 0
    original_content_ratio = 1 - citation_sentence_ratio
    
    return {
        'total_sentences': total_sentences,
        'citation_sentences': citation_sentence_count,
        'citation_sentence_ratio': citation_sentence_ratio,
        'original_content_ratio': original_content_ratio,
        'citation_sentences_list': citation_sentences
    }


if __name__ == "__main__":

    # 예시 텍스트로 평가 수행
    sample_text = """
To objectively compare capabilities, several benchmarks and head-to-head tests have been conducted.
OpenAI reported that its Deep Research model significantly outperforms previous models on certain challenging evaluations[64].
One example is Humanity's Last Exam (HLE), a broad benchmark of expert-level academic questions across 100+ subjects.
In this test, OpenAI Deep Research achieved about 26.6% accuracy, beating other contemporary systems by a margin[65].
For context, the next best, Perplexity's version, scored 21.1%, and Google's Gemini-based 'Thinking' model scored only 6.2% on the same expert-level questions[66].
This suggests that OpenAI's approach to multi-step research currently yields more correct answers on very difficult, open-ended questions.
Another benchmark is GAIA (General AI Assistant), which evaluates real-world problem-solving with tool use and web browsing.
OpenAI's Deep Research averaged 72.6% accuracy on GAIA, surpassing the previous best models that were around 63–64%[67][68].
Notably, standard GPT-4 with plugins scored only 15% on GAIA Level 3 tasks, highlighting how much improvement these specialized research agents provide[69].
"""

    # 평가 수행
    result = calculate_fairuse(sample_text)

    # 결과 출력
    print(f"전체 문장 수: {result['total_sentences']}")
    print(f"인용 포함 문장 수: {result['citation_sentences']}")
    print(f"인용 포함 문장 비율: {result['citation_sentence_ratio']:.1f}")
    print(f"원본 내용 비율: {result['original_content_ratio']:.1f}")
    print("인용 포함 문장 목록:")
    for i, sent in enumerate(result['citation_sentences_list'], 1):
        print(f"  {i}. {sent}")