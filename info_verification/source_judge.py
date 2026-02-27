import litellm
import json
from pydantic import BaseModel, Field
from utils import get_model_kwargs
import asyncio


class ReportSourceQualityRequest(BaseModel):
    summary: str
    category: (
        str  # "academic", "news", "social_media", "government", "industry", "other"
    )
    public_confidence: int  # 0-10
    published_date: str  # yyyy-MM-dd


class ReportSourceQuality(BaseModel):
    url: str
    context: str
    summary: str
    category: str
    public_confidence: int
    published_date: str


# 정보의 풍부함 (Depth & Breadth)
# 4.1 필수 데이터 충족 — 핵심 논거를 뒷받침할 1차·2차 자료가 충분한가 (필수) - 희규
# 4.2 풍부한 인용 — 다양한 출처를 포함하는가 (필수) - 희규
# 4.3 최신성 — 인용 데이터·문헌이 최신(발행 5년 이내 등)인지, 구 자료는 맥락을 설명했는가 - 희규
class ReportDepthAndBreadhJudgementRequest(BaseModel):
    explanation: str
    source_depth_score: int
    source_diversity_score: int
    source_freshness_score: int


class ReportDepthAndBreadhJudgement(BaseModel):
    explanation: str
    source_depth_score: int
    source_diversity_score: int
    source_freshness_score: int
    source_qualities: list[ReportSourceQuality]


SOURCE_JUDGE_PROMPT = """You are a research assistant analyzing sources for report writing. Extract the following information:

```
- summary: Extract key information relevant to the user's instruction. Focus on content that will help address their report needs.
- category: Classify as "academic", "news", "social_media", "government", "industry", or "other"
- public_confidence: Rate the source's credibility from 0-10 (0=lowest, 10=highest)
- published_date: Format as yyyy-MM-dd. Use explicit dates if available; otherwise, estimate based on content.
```

For each source, you will receive:
- instruction: The user's report writing request
- context: The source content (web page, markdown text, or PDF document)

# Instruction:
{instruction}

# Context:
{context}
"""


async def judge_source_quality(
    instruction: str, url: str, context: str, model: str = "gpt-4.1-mini"
) -> ReportSourceQuality:
    """
    Uses a language model to evaluate the quality of a source based on the provided instruction and context.

    Args:
        instruction (str): The user's report writing request.
        context (str): The content of the source (web or PDF document).

    Returns:
        ReportSourceQuality: A structured report containing the evaluated quality of the source.
    """
    response = await litellm.acompletion(
        messages=[
            {
                "role": "user",
                "content": SOURCE_JUDGE_PROMPT.format(
                    instruction=instruction, context=context
                ),
            },
            {
                "role": "user",
                "content": f"Instruction: {instruction}\nContext: {context}",
            },
        ],
        response_format=ReportSourceQualityRequest,
        **get_model_kwargs(model_id=model, max_tokens=4096),
    )

    return ReportSourceQuality(
        url=url, context=context, **json.loads(response.choices[0].message.content)
    )


OVERALL_JUDGE_PROMPT = """You are an expert evaluator assessing the quality and diversity of sources for a research report. Based on the analyzed sources, provide a comprehensive evaluation with the following components:

```
- explanation: Provide a detailed assessment of the sources' collective quality, diversity, relevance, and recency. Highlight strengths and weaknesses.
- source_depth_score: Rate 1-5 how thoroughly the sources cover the topic (depth of information)
5 Exceeds expectations with comprehensive primary and secondary sources that strongly support all key arguments. Sources are highly relevant and expertly integrated.
4 Provides thorough primary and secondary sources that effectively support most key arguments with clear relevance to the topic.
3 Includes adequate primary and secondary sources that support main arguments, though some connections could be strengthened.
2 Limited primary and secondary sources that partially support arguments; several key points lack sufficient evidence.
1 Insufficient sources to support arguments; critical evidence is missing or irrelevant to main points

- source_diversity_score: Rate 1-5 how well the sources represent different perspectives, types, and origins
5	Exceptional variety of credible sources (10+ sources) from diverse perspectives, including scholarly journals, books, and authoritative reports.
4	Strong variety of sources (8-10) representing different viewpoints with mostly peer-reviewed or professionally legitimate sources.
3	Adequate variety of sources (5-7) with some diversity in perspective, though more variety would strengthen the work.
2	Limited variety of sources (3-4), over-reliance on similar source types or perspectives.
1	Minimal sources (1-2) with no variety; sources are too similar or from questionable origins

- source_freshness_score: Rate 1-5 how recent and up-to-date the sources are relative to the topic
5	All sources are current (within 5 years) or, if older, their continued relevance is thoroughly explained with contextual analysis.
4	Most sources (80%%+) are current; older sources are justified with adequate contextual explanation.
3	Majority of sources (60-80%%) are current; some older sources lack sufficient context for their inclusion.
2	Many outdated sources (only 40-60%% current) with minimal explanation for their relevance to contemporary understanding.
1	Predominantly outdated sources (less than 40%% current) with no explanation of historical context or continued relevance

```

You will receive:
- The user's original report instruction
- Analysis of each source including summaries, categories, confidence ratings, and publication dates

Provide an objective evaluation focusing on these three dimensions. Your assessment should help determine if the sources are sufficient for creating a high-quality report.

# Instruction:
{instruction}

# Source Qualities:
{source_qualities}
"""


async def judge_overall_source_quality(
    instruction: str, contexts: dict[str, str], model: str = "gpt-4.1-mini"
):
    """
    Uses a language model to evaluate the overall quality of sources based on the provided instruction and source qualities.

    Args:
        instruction (str): The user's report writing request.
        source_qualities (list[ReportSourceQuality]): A list of evaluated source qualities.

    Returns:
        ReportDepthAndBreadhJudgement: A structured report containing the overall quality evaluation.
    """

    source_qualities = []
    for url, context in contexts.items():
        source_qualities.append(judge_source_quality(instruction, url, context, model))

    source_qualities = await asyncio.gather(*source_qualities)

    source_qualities_dict = [
        {
            "url": source.url,
            "summary": source.summary,
            "category": source.category,
            "public_confidence": source.public_confidence,
            "published_date": source.published_date,
        }
        for source in source_qualities
    ]
    response = litellm.completion(
        messages=[
            {
                "role": "user",
                "content": OVERALL_JUDGE_PROMPT.format(
                    instruction=instruction,
                    source_qualities=json.dumps(source_qualities_dict),
                ),
            },
        ],
        response_format=ReportDepthAndBreadhJudgementRequest,
        **get_model_kwargs(model_id=model, max_tokens=4096),
    )

    return ReportDepthAndBreadhJudgement(
        **json.loads(response.choices[0].message.content),
        source_qualities=source_qualities,
    )


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv()

    EXAMPLE_INSTRUCTION = "모션베드 침대의 장단점을 찾아서 알려주세요"
    EXAMPLE_CONTEXT = """Title: 템퍼 모션베드 직접 누워본 사람들이 말하는 장단점 3가지! | 프로덕트랭크

URL Source: https://productrank.kr/2024/05/08/%ED%85%9C%ED%8D%BC-%EB%AA%A8%EC%85%98%EB%B2%A0%EB%93%9C-%EC%A7%81%EC%A0%91-%EB%88%84%EC%9B%8C%EB%B3%B8-%EC%82%AC%EB%9E%8C%EB%93%A4%EC%9D%B4-%EB%A7%90%ED%95%98%EB%8A%94-%EC%9E%A5%EB%8B%A8%EC%A0%90-3/

Published Time: 2024-05-08T08:13:29+00:00

Markdown Content:
* * *

안녕하세요! 오늘은 최근 수면의 질은 물론, 건강을 위해 떠오르고 있는 침실 가구 중 하나가 바로 모션베드 입니다. **자신의 몸에 맞게 침대의 각도를 조절**할 수 있도록 설계되어 있어 머리, 등, 다리 부위를 원하는 대로 조절할 수 있고 **코골이 방지 모드, 다리 부종 완화 등 건강상의 이점**도 있어 최근 많은 분들이 템퍼 모션베드를 포함하여 모션베드를 선택하고 있습니다. 일반적으로 스프링 매트리스의 경우, 내부 자재가 스프링으로 있기 때문에 매트리스가 구부러지면 복원이 되지 않으며 라텍스 또한, 접히게 되면 라텍스의 성질을 잃어버리거나 손상이 되어 모션베드와 함께 사용하기에 어려운 소재입니다.

하지만, [템퍼 모션베드](https://kr.tempur.com/bed/by-product-type/)와 같이 메모리폼 소재와는 호환이 가능한 이유는!? 바로, 메모리폼 셀이 유동성·탄력성이 가졌기 때문에 구부러져도 원래 모습으로 계속 돌아올 수 있기 때문입니다. 템퍼 모션베드는 이와 같은 메모리폼 기능을 극대화하였으며, 최초의 메모리폼 브랜드로 체압 분산, 코골이 방지, tv시청 등 다양한 장점으로 많은 분들이 선택하고 있습니다.  
그러나, 서양에서 제작된 브랜드인 만큼 **한국인 체형과 우리나라 환경을 고려하지 않고 만들어져 한국인이 사용하면서 몇 가지 불편한 점**들도 있다고 합니다. 따라서, 오늘은 **템퍼 모션베드를 알아보고 국내 모션베드 브랜드 중 꾸준히 인기를 얻고 있는 두 브랜드**에 대해서도 소개해드리고자 합니다.

* * *

목차

*   [템퍼 모션베드 장점](https://productrank.kr/2024/05/08/%ED%85%9C%ED%8D%BC-%EB%AA%A8%EC%85%98%EB%B2%A0%EB%93%9C-%EC%A7%81%EC%A0%91-%EB%88%84%EC%9B%8C%EB%B3%B8-%EC%82%AC%EB%9E%8C%EB%93%A4%EC%9D%B4-%EB%A7%90%ED%95%98%EB%8A%94-%EC%9E%A5%EB%8B%A8%EC%A0%90-3/#%ED%85%9C%ED%8D%BC_%EB%AA%A8%EC%85%98%EB%B2%A0%EB%93%9C_%EC%9E%A5%EC%A0%90 "템퍼 모션베드 장점")
    *   [사용자 맞춤 각도 조절로 삶의 질 향상](https://productrank.kr/2024/05/08/%ED%85%9C%ED%8D%BC-%EB%AA%A8%EC%85%98%EB%B2%A0%EB%93%9C-%EC%A7%81%EC%A0%91-%EB%88%84%EC%9B%8C%EB%B3%B8-%EC%82%AC%EB%9E%8C%EB%93%A4%EC%9D%B4-%EB%A7%90%ED%95%98%EB%8A%94-%EC%9E%A5%EB%8B%A8%EC%A0%90-3/#%EC%82%AC%EC%9A%A9%EC%9E%90_%EB%A7%9E%EC%B6%A4_%EA%B0%81%EB%8F%84_%EC%A1%B0%EC%A0%88%EB%A1%9C_%EC%82%B6%EC%9D%98_%EC%A7%88_%ED%96%A5%EC%83%81 "사용자 맞춤 각도 조절로 삶의 질 향상")
    *   [체압 분산 효과로 결림, 뻐근함 감소](https://productrank.kr/2024/05/08/%ED%85%9C%ED%8D%BC-%EB%AA%A8%EC%85%98%EB%B2%A0%EB%93%9C-%EC%A7%81%EC%A0%91-%EB%88%84%EC%9B%8C%EB%B3%B8-%EC%82%AC%EB%9E%8C%EB%93%A4%EC%9D%B4-%EB%A7%90%ED%95%98%EB%8A%94-%EC%9E%A5%EB%8B%A8%EC%A0%90-3/#%EC%B2%B4%EC%95%95_%EB%B6%84%EC%82%B0_%ED%9A%A8%EA%B3%BC%EB%A1%9C_%EA%B2%B0%EB%A6%BC_%EB%BB%90%EA%B7%BC%ED%95%A8_%EA%B0%90%EC%86%8C "체압 분산 효과로 결림, 뻐근함 감소")
    *   [코골이, 다리 부종 완화 등 건강상 기능](https://productrank.kr/2024/05/08/%ED%85%9C%ED%8D%BC-%EB%AA%A8%EC%85%98%EB%B2%A0%EB%93%9C-%EC%A7%81%EC%A0%91-%EB%88%84%EC%9B%8C%EB%B3%B8-%EC%82%AC%EB%9E%8C%EB%93%A4%EC%9D%B4-%EB%A7%90%ED%95%98%EB%8A%94-%EC%9E%A5%EB%8B%A8%EC%A0%90-3/#%EC%BD%94%EA%B3%A8%EC%9D%B4_%EB%8B%A4%EB%A6%AC_%EB%B6%80%EC%A2%85_%EC%99%84%ED%99%94_%EB%93%B1_%EA%B1%B4%EA%B0%95%EC%83%81_%EA%B8%B0%EB%8A%A5 "코골이, 다리 부종 완화 등 건강상 기능")
*   [실제로 느껴본 템퍼 모션베드 단점](https://productrank.kr/2024/05/08/%ED%85%9C%ED%8D%BC-%EB%AA%A8%EC%85%98%EB%B2%A0%EB%93%9C-%EC%A7%81%EC%A0%91-%EB%88%84%EC%9B%8C%EB%B3%B8-%EC%82%AC%EB%9E%8C%EB%93%A4%EC%9D%B4-%EB%A7%90%ED%95%98%EB%8A%94-%EC%9E%A5%EB%8B%A8%EC%A0%90-3/#%EC%8B%A4%EC%A0%9C%EB%A1%9C_%EB%8A%90%EA%BB%B4%EB%B3%B8_%ED%85%9C%ED%8D%BC_%EB%AA%A8%EC%85%98%EB%B2%A0%EB%93%9C_%EB%8B%A8%EC%A0%90 "실제로 느껴본 템퍼 모션베드 단점")
    *   [작동 시 느껴지는 미세한 소음과 진동](https://productrank.kr/2024/05/08/%ED%85%9C%ED%8D%BC-%EB%AA%A8%EC%85%98%EB%B2%A0%EB%93%9C-%EC%A7%81%EC%A0%91-%EB%88%84%EC%9B%8C%EB%B3%B8-%EC%82%AC%EB%9E%8C%EB%93%A4%EC%9D%B4-%EB%A7%90%ED%95%98%EB%8A%94-%EC%9E%A5%EB%8B%A8%EC%A0%90-3/#%EC%9E%91%EB%8F%99_%EC%8B%9C_%EB%8A%90%EA%BB%B4%EC%A7%80%EB%8A%94_%EB%AF%B8%EC%84%B8%ED%95%9C_%EC%86%8C%EC%9D%8C%EA%B3%BC_%EC%A7%84%EB%8F%99 "작동 시 느껴지는 미세한 소음과 진동")
*   [구매 비용이 높음(헤드보드 별도 구매)](https://productrank.kr/2024/05/08/%ED%85%9C%ED%8D%BC-%EB%AA%A8%EC%85%98%EB%B2%A0%EB%93%9C-%EC%A7%81%EC%A0%91-%EB%88%84%EC%9B%8C%EB%B3%B8-%EC%82%AC%EB%9E%8C%EB%93%A4%EC%9D%B4-%EB%A7%90%ED%95%98%EB%8A%94-%EC%9E%A5%EB%8B%A8%EC%A0%90-3/#%EA%B5%AC%EB%A7%A4_%EB%B9%84%EC%9A%A9%EC%9D%B4_%EB%86%92%EC%9D%8C%ED%97%A4%EB%93%9C%EB%B3%B4%EB%93%9C_%EB%B3%84%EB%8F%84_%EA%B5%AC%EB%A7%A4 "구매 비용이 높음(헤드보드 별도 구매)")
    *   [서양인 체형을 고려한 제작 레시피](https://productrank.kr/2024/05/08/%ED%85%9C%ED%8D%BC-%EB%AA%A8%EC%85%98%EB%B2%A0%EB%93%9C-%EC%A7%81%EC%A0%91-%EB%88%84%EC%9B%8C%EB%B3%B8-%EC%82%AC%EB%9E%8C%EB%93%A4%EC%9D%B4-%EB%A7%90%ED%95%98%EB%8A%94-%EC%9E%A5%EB%8B%A8%EC%A0%90-3/#%EC%84%9C%EC%96%91%EC%9D%B8_%EC%B2%B4%ED%98%95%EC%9D%84_%EA%B3%A0%EB%A0%A4%ED%95%9C_%EC%A0%9C%EC%9E%91_%EB%A0%88%EC%8B%9C%ED%94%BC "서양인 체형을 고려한 제작 레시피")
*   [템퍼 모션베드 단점을 개선한 국내 브랜드](https://productrank.kr/2024/05/08/%ED%85%9C%ED%8D%BC-%EB%AA%A8%EC%85%98%EB%B2%A0%EB%93%9C-%EC%A7%81%EC%A0%91-%EB%88%84%EC%9B%8C%EB%B3%B8-%EC%82%AC%EB%9E%8C%EB%93%A4%EC%9D%B4-%EB%A7%90%ED%95%98%EB%8A%94-%EC%9E%A5%EB%8B%A8%EC%A0%90-3/#%ED%85%9C%ED%8D%BC_%EB%AA%A8%EC%85%98%EB%B2%A0%EB%93%9C_%EB%8B%A8%EC%A0%90%EC%9D%84_%EA%B0%9C%EC%84%A0%ED%95%9C_%EA%B5%AD%EB%82%B4_%EB%B8%8C%EB%9E%9C%EB%93%9C "템퍼 모션베드 단점을 개선한 국내 브랜드")
    *   [헤드까지 조절이 가능한 라클라우드](https://productrank.kr/2024/05/08/%ED%85%9C%ED%8D%BC-%EB%AA%A8%EC%85%98%EB%B2%A0%EB%93%9C-%EC%A7%81%EC%A0%91-%EB%88%84%EC%9B%8C%EB%B3%B8-%EC%82%AC%EB%9E%8C%EB%93%A4%EC%9D%B4-%EB%A7%90%ED%95%98%EB%8A%94-%EC%9E%A5%EB%8B%A8%EC%A0%90-3/#%ED%97%A4%EB%93%9C%EA%B9%8C%EC%A7%80_%EC%A1%B0%EC%A0%88%EC%9D%B4_%EA%B0%80%EB%8A%A5%ED%95%9C_%EB%9D%BC%ED%81%B4%EB%9D%BC%EC%9A%B0%EB%93%9C "헤드까지 조절이 가능한 라클라우드")
    *   [세계 1위 모터 브랜드, 마스슬립](https://productrank.kr/2024/05/08/%ED%85%9C%ED%8D%BC-%EB%AA%A8%EC%85%98%EB%B2%A0%EB%93%9C-%EC%A7%81%EC%A0%91-%EB%88%84%EC%9B%8C%EB%B3%B8-%EC%82%AC%EB%9E%8C%EB%93%A4%EC%9D%B4-%EB%A7%90%ED%95%98%EB%8A%94-%EC%9E%A5%EB%8B%A8%EC%A0%90-3/#%EC%84%B8%EA%B3%84_1%EC%9C%84_%EB%AA%A8%ED%84%B0_%EB%B8%8C%EB%9E%9C%EB%93%9C_%EB%A7%88%EC%8A%A4%EC%8A%AC%EB%A6%BD "세계 1위 모터 브랜드, 마스슬립")
*   [템퍼 모션베드 콘텐츠 요약](https://productrank.kr/2024/05/08/%ED%85%9C%ED%8D%BC-%EB%AA%A8%EC%85%98%EB%B2%A0%EB%93%9C-%EC%A7%81%EC%A0%91-%EB%88%84%EC%9B%8C%EB%B3%B8-%EC%82%AC%EB%9E%8C%EB%93%A4%EC%9D%B4-%EB%A7%90%ED%95%98%EB%8A%94-%EC%9E%A5%EB%8B%A8%EC%A0%90-3/#%ED%85%9C%ED%8D%BC_%EB%AA%A8%EC%85%98%EB%B2%A0%EB%93%9C_%EC%BD%98%ED%85%90%EC%B8%A0_%EC%9A%94%EC%95%BD "템퍼 모션베드 콘텐츠 요약")

템퍼 모션베드 장점
----------

![Image 1: 템퍼 모션베드 직접 누워본 사람들이 말하는 장단점 3가지!](https://productrank.kr/wp-content/uploads/2024/05/image.jpg)

### 사용자 맞춤 각도 조절로 삶의 질 향상

* * *

템퍼 모션베드는 자신의 체형에 맞게 침대 각도를 조절할 수 있으며, 이는 좋은 수면과 더불어 편안한 휴식을 할 수 있도록 해줍니다. 최근에 [허리디스크 발병률이 53%](http://www.bosa.co.kr/news/articleView.html?idxno=2163311)가 넘으면서 허리 통증으로 고생하시는 분들이 많은데, 모션베드 상단부와 하단부를 살짝 올려 U(V)자 형태로 만들어 줌으로써 이는 **몸이 들뜨지 않도록 받쳐주기에 허리가 받는 체압(중력)을 최소화**할 수 있습니다. 또한, **템퍼 모션베드에는 ‘코골이 방지, 릴렉스, tv시청’ 세 가지 모드가 리모콘에 저장**되어 있어 편안하게 수면과 휴식을 취할 수 있도록 도와줍니다.

### 체압 분산 효과로 결림, 뻐근함 감소

* * *

![Image 2: 템퍼 모션베드 직접 누워본 사람들이 말하는 장단점 3가지!](https://productrank.kr/wp-content/uploads/2024/05/image-2-1024x469.jpg)

템퍼 모션베드는 **체중과 압력을 고르게 분산시켜주는 메모리폼 매트리스**와 호환이 되어 허리, 목 등과 같은 특정 부위에 가해지는 **중력(체압)을 줄이는 데 도움**을 줍니다. 이는 체압을 고르게 분산시켜줌으로서 **원할한 혈액 순환과 근육 이완**을 해주어 편안한 몸 상태에서 휴식과 수면을 할 수 있도록 해줍니다. 효율적인 체압분산은 뒤척임을 줄여 수면 중 지친 우리의 몸을 회복에 도움을 주기 때문에 단순한 편안함을 넘어 건강상의 이점도 있습니다.

### 코골이, 다리 부종 완화 등 건강상 기능

* * *

![Image 3: 템퍼 모션베드 직접 누워본 사람들이 말하는 장단점 3가지!](https://productrank.kr/wp-content/uploads/2024/05/TEMPUR-Zero-G-Lifestyle-Adjustable-Bed-Base-1024x575.jpg)

앞서 언급한 바와 같이 템퍼 모션베드는 기본적으로 필요한 자세가 리모콘에 저장되어 있습니다. 상체(목)을 살짝 올리는 **코골이 모드는 수면 중 더 나은 공기 흐름으로 호흡할 수 있도록 하여 수면 무호흡 증상과 코골이를 줄일 수 있습니다.** 또한, 각도를 조절하면서 자신에게 맞는 자세를 찾으면 수면 중 발생할 수 있는 위험을 사전에 방지할 수 있습니다.

하체를 올려 허벅지와 다리를 받쳐주면 원활하게 다리와 발에 혈액이 흘러갈 수 있도록 하여 **하체 부종을 예방하고 심부정맥과 같은 위험을 줄일 수 있습니다.**

실제로 느껴본 템퍼 모션베드 단점
------------------

* * *

![Image 4: 템퍼 모션베드 직접 누워본 사람들이 말하는 장단점 3가지!](https://productrank.kr/wp-content/uploads/2024/05/103452_HERO_Tier_1_Foam_Medium_King_Adjustable_2737_5x7_251218005742177595-1024x768.jpg)

### 작동 시 느껴지는 미세한 소음과 진동

![Image 5: 템퍼 모션베드 직접 누워본 사람들이 말하는 장단점 3가지!](blob:http://localhost/8f957c445471fb64eb341093c2a2af4e)

템퍼 모션베드 일부 사용자들은 **각도 조절 시 소음이 발생하고 진동이 느껴진다고 합니다.** 세계 2위 OKIN사 의 모터를 사용하고 있는 템퍼 모션베드는 일상 생활에는 그렇게 심하게 들리지는 않지만, 조용한 침실에서는 미세하게 소음이 들려 소음이 예민한 사람의 경우 불편함을 느끼며, 각도 조절 시에 간혹 떨림이 느껴지는 경우가 있다고 합니다.

구매 비용이 높음(헤드보드 별도 구매)
---------------------

![Image 6: 템퍼 모션베드 직접 누워본 사람들이 말하는 장단점 3가지!](https://productrank.kr/wp-content/uploads/2024/05/%ED%85%9C%ED%8D%BC-Element-%ED%97%A4%EB%93%9C%EB%B3%B4%EB%93%9C.jpg)

템퍼 모션베드는 프리미엄 메모리폼과 기기가 포함된 모션베드 프레임을 함께 구매 시 퀸 사이즈 기준 700만원으로 **일반 침대에 비해 가격이 높은 편입니다.** 또한, **헤드보드가 미포함된 상품**으로 헤드 포함 시에는 가격이 더 높아질 수 있습니다. 또한, 템퍼의 경우 수입 브랜드인 점에서 카드사 문제로 **모션베드 렌탈 서비스 이용할 수 없기에 초기 구매 비용이 부담**으로 다가올 수 있습니다.

### 서양인 체형을 고려한 제작 레시피

![Image 7: 템퍼 모션베드 직접 누워본 사람들이 말하는 장단점 3가지!](https://productrank.kr/wp-content/uploads/2024/05/Stressless_Reno_page-1024x492.jpg)

덴마크 브랜드인 **템퍼는 서양인 체형 기준**으로 제작되다 보니, 서양인에 비해 골격이 작은 한국인이 사용하기에는 **몸이 갇혀서 답답하거나, 지지력이 부족하여 오히려 허리가 불편하다는 후기**를 볼 수 있습니다. 서양인의 경우 평균적으로 골격이 크고 골반이 넓기 때문에 몸을 받쳐주는 폼 입자가 촘촘하지 않아도 지지력을 느낄 수 있습니다. 따라서, 실제로 템퍼 모션베드 누워본 분들이 누워있으면 **몸이 파묻히는 느낌이 들고 움직이기가 불편하다는 평**도 살펴볼 수 있습니다.

템퍼 모션베드 단점을 개선한 국내 브랜드
----------------------

* * *

### 헤드까지 조절이 가능한 라클라우드

![Image 8: 템퍼 모션베드 직접 누워본 사람들이 말하는 장단점 3가지!](https://productrank.kr/wp-content/uploads/2024/05/sFUm6eLxywHceVMEhkwjg2O5COPladO-2.jpg)

*   상체, 하체를 포함해 **헤드까지 조절이 가능한 모델**
*   다양한 가격대의 상품이 있어 선택의 폭이 넓음
*   상체가 거의 70도까지 올라가는 것처럼 조절되는 폼이 넓음
*   **천연 라텍스와 호환**이 되는 모델로 탄탄한 모션베드를 원하시는 분께 좋은 선택지
*   모터 A/S 기간이 2년이며, 세계 2위 OKIN사 사용

### 세계 1위 모터 브랜드, 마스슬립

* * *

![Image 9: 템퍼 모션베드 직접 누워본 사람들이 말하는 장단점 3가지!](blob:http://localhost/f0b78fcecd4432668a7c27811311ee85)

*   **한국인 체형**에 맞게 제작된 국내 메모리폼 브랜드의 모션베드 (운동선수 사용 브랜드)
*   **세계 1위 모터 브랜드 LINAK사 사용**으로 **‘무소음, 무진동’**으로 유명함 (모터 A/S 기간 5년)
*   코골이, 다리 부종 완화, 무중력 모드, TV모드 기본 4가지 자세 셋팅 및 사용자 지정 자세 설정 가능
*   마스슬립 모든 프레임 주문 제작이 가능하며, **모션베드 렌탈 서비스 진행 가능**
*   리모콘 외에도 스**마트폰을 통한 각도 조절 및 알람 설정** 등 다양한 기능 활용 가능

템퍼 모션베드 콘텐츠 요약
--------------

* * *

모션베드의 인기가 올라가면서 템퍼 모션베드에 대한 관심도 증가하고 있습니다. 따라서, 오늘은 템퍼 모션베드의 장점과 단점에 대해 알아보고 이 외에 국내 브랜드 중 모션베드로 꾸준히 사랑 받고 있는 ‘라클라우드, 마스슬립’ 브랜드에 대해서도 알아보았습니다.

구매 시 적지 않은 비용이 드는 만큼 모션베드 구매 시에는 비용과 더불어 **‘소음과 진동이 느껴지는지, 모터 A/S 기간, 설정 가능한 자세’ 등 다양한 요소들을 고려**함으로 합리적인 선택을 할 수 있을 듯 보입니다. 모션베드를 고려하신다면, 직접 체험해보시고 자신의 몸에 맞는 매트리스 타입과 필요한 기능이 있는 모션베드를 선택하시는 걸 권장드립니다.

* * *
"""

    quality = judge_source_quality(EXAMPLE_INSTRUCTION, EXAMPLE_CONTEXT)
    print(quality)
