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

    # ✅ Remove backticks from both ends
    url = url.strip("`")   # e.g.: 'https://a.com' -> https://a.com

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
    # Regular expression to find [domain](url) pattern
    pattern = r"\[.*?\]\((https?://[^)]+)\)"
    urls = re.findall(pattern, text)

    # Assign a reference number to each unique URL
    unique_urls = []
    url_to_ref = {}
    for url in urls:
        if url not in url_to_ref:
            url_to_ref[url] = len(unique_urls) + 1
            unique_urls.append(url)

    # Replace all URLs in the text with [n] format
    def replacer(match):
        url = match.group(1)
        return f"[{url_to_ref[url]}]"

    processed_text = re.sub(pattern, replacer, text)

    # Add References section at the bottom
    references_section = "\n\n## References\n"
    for i, url in enumerate(unique_urls, 1):
        references_section += f"[{i}] {url}\n"

    return processed_text + references_section


if __name__ == "__main__":
    # Example usage
    file = "deep_research_samples/gemini-2.5-pro_6.md"
    with open(file, "r", encoding="utf-8") as f:
        example_report = f.read()

    report, references_section = split_references(example_report)
    refs = extract_references(references_section)
    print(refs)
    print(sorted(refs.keys()))
