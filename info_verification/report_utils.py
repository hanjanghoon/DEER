import re

REF_PATTERNS = [
    "# References",
    "## References",
    "### References",
    "\nCitations:",
    "\nReferences:",
    "**References:**",
    "#### **참고 자료**",
    "#### 참고 자료",
    "#### **References**",
    "\n\nReferences\n",
]

# e.g.: [1] https://selfdeterminationtheory.org/wp-content/uploads/2022/02/2021_ChiuChaiWilliamsLin_TeacherProfessional.pdf
# CITATION_PATTERN = re.compile(r"\[([\-\d]+)\]\s+(https?://[^\s]+)")
CITATION_PATTERN = re.compile(r"\[([\-\d]+)\][^\n]*?(https?://[^\s]+)") #jang
# e.g.: 1. https://selfdeterminationtheory.org/wp-content/uploads/2022/02/2021_ChiuChaiWilliamsLin_TeacherProfessional.pdf
GEMINI_PATTERN1 = re.compile(r"(\d+)\..*?\<(https?://[^>]+)\>")
GEMINI_PATTERN2 = re.compile(r"^(\d+)\..*?\((https?:\/\/[^\]]+)\)", re.MULTILINE)


# def clean_url(url: str) -> str:
#     """
#     Clean the URL by removing query parameters and fragments.
#     """
#     # if "?" in url:
#     #     url = url.split("?")[0]
#     if "#" in url:
#         url = url.split("#")[0]
#     return url.strip()
def clean_url(url: str) -> str:
    url = url.strip()

    # ✅ 양끝에 붙은 작은따옴표만 제거
    url = url.strip("`")   # 예: 'https://a.com' -> https://a.com

    if "#" in url:
        url = url.split("#")[0]

    return url.strip()


def extract_references(report: str):
    citations = {}
    for pattern in [ GEMINI_PATTERN1, GEMINI_PATTERN2, CITATION_PATTERN]:
        for match in pattern.finditer(report):
            citation_index = match.group(1)
            citation_url = match.group(2)
            citations[citation_index] = citation_url
            # print(CITATION_PATTERN, citation_index, "------>>>>", citation_url)
            report = report.replace(match.group(0), "")  # Remove the citation from the report

    return citations


def split_references(report: str):
    references_section = ""
    for pattern in REF_PATTERNS:
        if pattern in report:
            report, references_section = report.split(pattern, 1)
            break

    return report.strip(), references_section.strip()


import re


def replace_openai_citations(text):
    # [domain](url) 패턴을 찾는 정규표현식
    pattern = r"\[.*?\]\((https?://[^)]+)\)"
    urls = re.findall(pattern, text)

    # 각 고유한 URL에 참조 번호를 할당
    unique_urls = []
    url_to_ref = {}
    for url in urls:
        if url not in url_to_ref:
            url_to_ref[url] = len(unique_urls) + 1
            unique_urls.append(url)

    # 텍스트의 모든 URL을 [n] 형식으로 교체
    def replacer(match):
        url = match.group(1)
        return f"[{url_to_ref[url]}]"

    processed_text = re.sub(pattern, replacer, text)

    # References 섹션을 하단에 추가
    references_section = "\n\n## References\n"
    for i, url in enumerate(unique_urls, 1):
        references_section += f"[{i}] {url}\n"

    return processed_text + references_section


if __name__ == "__main__":
    # Example usage
    # file = "deep_research_samples/chatexaone_deepresearch_1.md"
    file = "deep_research_samples/gemini-2.5-pro_6.md"
    # file = "deep_research_samples/perplexity_2.md"
    # file = "deep_research_samples/openai_1_cleaned.md"
    with open(file, "r", encoding="utf-8") as f:
        example_report = f.read()

    report, references_section = split_references(example_report)
    # print(references_section)
    refs = extract_references(references_section)
    print(refs)
    print(sorted(refs.keys()))
    # print(split_references(example_report))

    # 사용 예시
    # input_text = '''*   **Strategic Hamlet Program (1962–63):** Aimed to fortify villages and isolate the Viet Cong from the population. By August 1963, Diệm's government had established over 7,000 fortified hamlets[rand.org](https://www.rand.org/content/dam/rand/pubs/occasional_papers/2009/RAND_OP258.pdf#:~:text=to%20infiltrate%20and%20destroy%20them,Hill%2C%20Inc.%2C%201995%2C%20p.%20154). Encircled with moats, stakes, and local militia, these hamlets were intended to deny communist infiltrators access to people and resources[rand.org](https://www.rand.org/content/dam/rand/pubs/occasional_papers/2009/RAND_OP258.pdf#:~:text=hamlet%20program%20was%20intended%2C%20among,Politburo%20in%20Hanoi%20grew%20alarmed)[rand.org](https://www.rand.org/content/dam/rand/pubs/occasional_papers/2009/RAND_OP258.pdf#:~:text=to%20infiltrate%20and%20destroy%20them,Hill%2C%20Inc.%2C%201995%2C%20p.%20154). However, the program backfired. The Viet Cong aggressively targeted the hamlets and ultimately managed to "liberate" about three-quarters of them[rand.org](https://www.rand.org/content/dam/rand/pubs/occasional_papers/2009/RAND_OP258.pdf#:~:text=to%20infiltrate%20and%20destroy%20them,Hill%2C%20Inc.%2C%201995%2C%20p.%20154). Rather than winning "hearts and minds," strategic hamlets often angered peasants who were forcibly relocated, thus **undermining Diệm's support** in the countryside.'''

    # result = replace_openai_citations(input_text)
    # print(result)

    # for i in range(1, 6):
    #     file = f"deep_research_samples/chatexaone_deepresearch_{i}.md"
    #     with open(file, "r") as f:
    #         content = f.read()
    #         processed_content = replace_openai_citations(content)
    #         with open(file.replace(".md", "_cleaned.md"), "w") as wf:
    #             wf.write(processed_content)
