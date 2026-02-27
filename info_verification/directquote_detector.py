import re
import litellm
from typing import List, Dict, Tuple
from difflib import SequenceMatcher
from typing import List, Tuple
from nltk import sent_tokenize
import asyncio
import multiprocessing as mp
import os
from functools import partial
from rapidfuzz import fuzz


def _calculate_ratio_worker(text1, sentence, fuzz_threshold: float = 0.6) -> float:
    """
    두 텍스트(text1과 text2의 한 문장) 간의 유사도 비율을 계산합니다.
    """
    fuzz_ratio = fuzz.ratio(text1, sentence) / 100.0
    if fuzz_ratio < fuzz_threshold:
        return fuzz_ratio
    return SequenceMatcher(None, text1, sentence).ratio()

def calculate_similarity_parallel(text1: str, text2: str) -> float:
    text2_sentences = sent_tokenize(text2)
    if not text2_sentences:
        return 0.0, []

    # tasks = [(text1, sentence) for sentence in text2_sentences]
    # with mp.Pool(processes=2) as pool:
    #     ratios = pool.starmap(_calculate_ratio_worker, tasks)
    ratios = [_calculate_ratio_worker(text1, sentence) / 100.0 for sentence in text2_sentences]

    # 4. 계산된 모든 유사도 비율 중에서 최대값을 찾습니다.
    if not ratios:
        return 0.0, []
        
    max_ratio = max(ratios)
    best_index = ratios.index(max_ratio) # 최대값의 인덱스를 찾습니다.

    # 5. 원본 코드의 로직에 따라 가장 유사한 문장 주변의 문장들을 추출합니다.
    # [best_index - 10 : best_index + 10] 범위
    start_index = max(0, best_index - 10)
    end_index = min(len(text2_sentences), best_index + 10)
    nearby_sentences = text2_sentences[start_index:end_index]

    return max_ratio, nearby_sentences

# --- Asyncio 환경을 위한 래퍼(Wrapper) 함수 (핵심) ---
async def calculate_similarity_async(text1: str, text2: str) -> tuple[float, list[str]]:
    loop = asyncio.get_running_loop()

    func = partial(calculate_similarity_parallel, text1, text2)

    result = await loop.run_in_executor(None, func)
    
    return result

class DirectQuoteFormatChecker:

    async def check_quote_format(self, sentence: str, reference: str, similarity_threshold: float = 0.9, model: str = "gpt-4.1") -> Dict:
        """
        직접인용 형식 검사 수행
        
        Args:
            sentence: 검사할 문장
            reference: 비교할 참조 텍스트
            similarity_threshold: 직접인용 판단 임계값
            
        Returns:
            종합 평가 결과
        """
        # 1단계: 유사도 계산
        similarity_score, nearby_sentences = await calculate_similarity_async(sentence.strip().lower(), reference.strip().lower())
        
        # 2단계: 직접인용 여부 판단
        is_direct_quote = similarity_score >= similarity_threshold
        
        if not is_direct_quote:
            return {
                'is_direct_quote': False,
                'similarity_score': similarity_score,
                'format_check_result': None,
                'overall_assessment': {
                    'overall_compliance': 'NOT_APPLICABLE',
                    'assessment': '직접인용이 아니므로 형식 검사가 필요하지 않습니다.',
                    'recommendations': []
                },
                'compliance_score': 100.0
            }
        
        # 3단계: 인용 형식 검사
        format_check = self.check_citation_format(sentence, similarity_score)
        
        # 4단계: LLM 기반 종합 평가
        nearby_sentences_text = "\n".join(nearby_sentences)
        overall_assessment = await self._llm_comprehensive_evaluation(sentence, nearby_sentences_text, format_check, model=model)

        return {
            'is_direct_quote': True,
            'similarity_score': similarity_score,
            'format_check_result': format_check,
            'overall_assessment': overall_assessment,
            'compliance_score': self._calculate_compliance_score([format_check])
        }
    
    def check_citation_format(self, sentence: str, similarity_score: float) -> Dict:
        """인용 형식 검사"""
        
        # 정규식으로 기본 형식 검사
        has_quotation_marks = bool(re.search(r'["""].*?["""]', sentence))
        has_block_quote = self._is_block_quote_format(sentence)
        has_citation_mark = bool(re.search(r'\[([\d\-]+)\]', sentence))
        
        return {
            'sentence': sentence,
            'similarity_score': similarity_score,
            'has_quotation_marks': has_quotation_marks,
            'has_block_quote': has_block_quote,
            'has_citation_mark': has_citation_mark,
            'format_compliance': has_quotation_marks or has_block_quote,
            'needs_review': not (has_quotation_marks or has_block_quote) and similarity_score > 0.9
        }
    
    def _is_block_quote_format(self, sentence: str) -> bool:
        """블록 인용 형식 확인"""
        # 블록 인용 패턴 확인 (들여쓰기, 구분선 등)
        block_patterns = [
            r'^\s{4,}',  # 4칸 이상 들여쓰기
            r'^>\s',     # 인용 기호
            r'^\|',      # 구분선
        ]
        
        for pattern in block_patterns:
            if re.search(pattern, sentence, re.MULTILINE):
                return True
        return False

    async def _llm_comprehensive_evaluation(self, sentence: str, reference: str, format_check: Dict, model: str) -> Dict:
        """LLM 기반 종합 평가"""
        
        # 형식 준수 여부 확인
        if format_check['format_compliance']:
            return {
                'overall_compliance': 'COMPLIANT',
                'assessment': '직접인용이 적절한 형식을 사용하고 있습니다.',
                'recommendations': []
            }
        
        # LLM 프롬프트 구성
        prompt = self._create_evaluation_prompt(sentence, reference, format_check)
        
        try:
            response = await litellm.acompletion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            evaluation = response.choices[0].message.content
            return self._parse_llm_response(evaluation)
            
        except Exception as e:
            return {
                'overall_compliance': 'ERROR',
                'assessment': f'LLM 평가 중 오류 발생: {str(e)}',
                'recommendations': ['수동 검토 필요']
            }
    
    def _create_evaluation_prompt(self, sentence: str, reference: str, format_check: Dict) -> str:
        """LLM 평가용 프롬프트 생성"""
        
        prompt = f"""
The following is a sentence suspected of direct quotation from academic text. Please evaluate whether it complies with fair use guidelines.

**Fair Use Guidelines:**
- Direct quotes must use quotation marks (" ") or block quote format
- Citation sources must be indicated
- Quote length should be limited to the necessary minimum

**Sentence to Review:**
{sentence}

**Reference Text:**
{reference}

**Format Check Results:**
- Similarity Score: {format_check['similarity_score']:.2f}
- Has Quotation Marks: {format_check['has_quotation_marks']}
- Has Block Quote Format: {format_check['has_block_quote']}
- Has Citation Mark: {format_check['has_citation_mark']}

Please provide evaluation results in the following format:

1. Overall Compliance: [COMPLIANT/NON_COMPLIANT]
2. Issues and Improvements: [Specific analysis]
3. Recommendations:
   - [Specific improvement suggestions]
"""
        return prompt
    
    def _parse_llm_response(self, response: str) -> Dict:
        """LLM 응답 파싱"""
        # 응답에서 구조화된 정보 추출
        compliance_match = re.search(r'Overall Compliance: (\w+)', response)
        if compliance_match:
            compliance = compliance_match.group(1)
        elif "NON_COMPLIANT" in response:
            compliance = "NON_COMPLIANT"
        elif "COMPLIANT" in response:
            compliance = "COMPLIANT"
        else:
            compliance = 'UNKNOWN'
        
        # 권고사항 추출
        recommendations = []
        recommendation_section = re.search(r'Recommendations:(.*?)(?=\n\n|\Z)', response, re.DOTALL)
        if recommendation_section:
            rec_text = recommendation_section.group(1).strip()
            recommendations = [line.strip('- ') for line in rec_text.split('\n') if line.strip().startswith('-')]
        
        return {
            'overall_compliance': compliance,
            'assessment': response,
            'recommendations': recommendations
        }
    
    def _calculate_compliance_score(self, format_results: List[Dict]) -> float:
        """준수도 점수 계산"""
        if not format_results:
            return 100.0
        
        compliant_count = sum(1 for r in format_results if r['format_compliance'])
        total_count = len(format_results)
        
        return (compliant_count / total_count) * 100
    

def check_citation_format(sentence: str) -> Dict:
    """
    인용 형식 검사 함수
    
    Args:
        sentence (str): 검사할 문장
        
    Returns:
        Dict: 검사 결과
    """
    checker = DirectQuoteFormatChecker()
    return checker._check_citation_format(sentence, 1.0)  # 유사도는 1.0으로 설정하여 형식만 검사

# async def detect_direct_quote(report: str, references: dict[str, str], similarity_threshold: float = 0.9, model: str = "gpt-4.1") -> Dict:
#     """
#     직접인용 여부를 검사하는 함수
    
#     Args:
#         sentence (str): 검사할 문장
#         reference (str): 비교할 참조 텍스트
#         similarity_threshold (float): 유사도 임계값
        
#     Returns:
#         Dict: 검사 결과
#     """
#     checker = DirectQuoteFormatChecker()
#     sentences = sent_tokenize(report)
#     results = []
#     total_sentence_checked = 0
#     total_citation_checked = 0
#     for sentence in sentences:
#         citations = re.findall(r'\[([\d\-]+)\]', sentence)
#         if not citations:
#             continue
#         total_sentence_checked += 1
#         for citation in citations:
#             total_citation_checked += 1
#             reference = references.get(citation, None)
#             # multiple citations
#             if not reference:
#                 # print(f"Warning: No reference found for citation {citation} in sentence: {sentence}")
#                 continue
#             result = checker.check_quote_format(sentence, reference, similarity_threshold, model=model)
#             results.append(result)

#     results = await asyncio.gather(*results)

#     # non_compliant_count = sum(1 for r in results if r.get('overall_assessment', {}).get('overall_compliance') == 'NON_COMPLIANT')
#     # compliant_count = sum(1 for r in results if r.get('overall_assessment', {}).get('overall_compliance') == 'COMPLIANT')

#     return {
#         'results': results,
#         # 'non_compliant_count': non_compliant_count,
#         # 'compliant_count': compliant_count,
#         # 'total_sentence_checked': total_sentence_checked,
#         # 'total_citation_checked': total_citation_checked,
#     }
async def detect_direct_quote(report: str, references: dict[str, str], similarity_threshold: float = 0.9, model: str = "gpt-4.1-nano") -> Dict:
    """
    직접인용 여부를 검사하는 함수
    
    Args:
        sentence (str): 검사할 문장
        reference (str): 비교할 참조 텍스트
        similarity_threshold (float): 유사도 임계값
        
    Returns:
        Dict: 검사 결과
    """
    checker = DirectQuoteFormatChecker()
    sentences = sent_tokenize(report)
    results = []
    total_sentence_checked = 0
    total_citation_checked = 0
    
    for sentence in sentences:
        citations = re.findall(r'\[([\d\-]+)\]', sentence)
        if not citations:
            continue
        total_sentence_checked += 1
        for citation in citations:
            total_citation_checked += 1
            reference = references.get(citation, None)
            # multiple citations
            if not reference:
                # print(f"Warning: No reference found for citation {citation} in sentence: {sentence}")
                continue
            result = checker.check_quote_format(sentence, reference, similarity_threshold, model=model)
            results.append(result)

    results = await asyncio.gather(*results)

    # 전체 결과에서 NON_COMPLIANT 비율 계산 (fair_use 점수용)
    total_results = len(results)
    non_compliant_count = sum(1 for r in results if r.get('overall_assessment', {}).get('overall_compliance') == 'NON_COMPLIANT')
    
    # direct_quote인 결과만 필터링 (direct_quote 점수용)
    direct_quote_results = [r for r in results if r.get('is_direct_quote', False)]
    direct_quote_total = len(direct_quote_results)
    direct_quote_non_compliant = sum(1 for r in direct_quote_results if r.get('overall_assessment', {}).get('overall_compliance') == 'NON_COMPLIANT')
    
    # fair_use 점수 계산 (전체 결과 기준, 10% 이하면 10점)
    if total_results == 0:
        fair_use_score = 10.0
    else:
        non_compliant_ratio = non_compliant_count / total_results
        if non_compliant_ratio <= 0.1:  # 10% 이하
            fair_use_score = 10.0
        else:
            # 10%부터 100%까지 선형 감점 (10점 -> 0점)
            fair_use_score = max(0.0, 10.0 - (non_compliant_ratio - 0.1) * (10.0 / 0.9))
    
    # direct_quote 점수 계산 (direct_quote 결과만 기준, 5% 이하면 10점, 50%까지 0점으로 감점)
    if direct_quote_total == 0:
        direct_quote_score = 10.0
    else:
        direct_quote_non_compliant_ratio = direct_quote_non_compliant / direct_quote_total
        if direct_quote_non_compliant_ratio <= 0.05:  # 5% 이하
            direct_quote_score = 10.0
        elif direct_quote_non_compliant_ratio >= 0.5:  # 50% 이상
            direct_quote_score = 0.0
        else:
            # 5%부터 50%까지 선형 감점 (10점 -> 0점)
            direct_quote_score = 10.0 - (direct_quote_non_compliant_ratio - 0.05) * (10.0 / 0.45)

    return {
        'results': results,
        'ethics_compliance': {
            'responsible_info': {
                'fair_use': round(fair_use_score, 1),
                'direct_quote': round(direct_quote_score, 1)
            }
        }
    }


if __name__ == "__main__":
    from dotenv import load_dotenv
    import asyncio

    load_dotenv()
    
    # 검사기 초기화

    references = {
        "2-1": "According to available information, the CEP compensated residential school survivors who were alive on May 30, 2005, with payments calculated at $10,000 for the first year of attendance and $3,000 per subsequent year.",
    }
    sentence = "According to available information, the CEP compensated residential school survivors who were alive on May 30, 2005, with payments calculated at $10,000 for the first year of attendance and $3,000 per subsequent year[2-1][2-2]."

    # 종합 평가 수행
    results = asyncio.run(detect_direct_quote(sentence, references))

    # 결과 출력
    from pprint import pprint
    pprint(results)

    print(f"직접인용 여부: {results['results'][0]['is_direct_quote']}")
    print(f"유사도: {results['results'][0]['similarity_score']:.2f}")
    print(f"준수도 점수: {results['results'][0]['compliance_score']:.1f}%")
    print(f"전체 평가: {results['results'][0]['overall_assessment']['overall_compliance']}")
    print("권고사항:")
    for rec in results['results'][0]['overall_assessment']['recommendations']:
        print(f"- {rec}")