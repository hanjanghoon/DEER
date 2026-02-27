from typing import Optional
import aiohttp
import asyncio, aiofiles
import os, json
from typing import Optional, Union
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
import hashlib


def get_url_cache_file(url: str) -> str:
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return f"cache/{url_hash}.md"


async def check_url_cache(url: str) -> Optional[str]:
    if os.environ.get("USE_WEBPAGE_CACHE") != "true":
        return None

    cache_file = get_url_cache_file(url)
    if os.path.exists(cache_file):
        async with aiofiles.open(cache_file, "r") as f:
            markdown = await f.read()
            return markdown
    return None


async def save_url_cache(url: str, markdown: str) -> None:
    if os.environ.get("USE_WEBPAGE_CACHE") != "true":
        return

    cache_file = get_url_cache_file(url)
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    async with aiofiles.open(cache_file, "w") as f:
        await f.write(markdown)


async def make_filtered_output(urls: list[str]) -> tuple[dict[str, str], list[str]]:
    uncached_urls = []
    results = {}
    for url in urls:
        if markdown := await check_url_cache(url):
            results[url] = markdown
        else:
            uncached_urls.append(url)
    return results, uncached_urls


async def fetch_webpage_crawl4ai(
    urls: list[str], headless: bool = True
) -> dict[str, str]:
    results, uncached_urls = await make_filtered_output(urls)
    if not uncached_urls:
        return results

    config = BrowserConfig(
        headless=headless,
        browser_type="chromium",
        browser_mode="docker",
        viewport_width=1280,
        viewport_height=720,
    )
    run_config = CrawlerRunConfig(
        delay_before_return_html=5.0,
        process_iframes=True,
    )
    async with AsyncWebCrawler(config=config, verbose=True) as crawler:
        uncached_results = await crawler.arun_many(
            urls=uncached_urls, config=run_config
        )
        uncached_markdowns = {
            k: v.markdown for k, v in zip(uncached_urls, uncached_results)
        }

    return {**results, **uncached_markdowns}


OUTPUT_FORMAT = """Title: {title}

{markdown}
"""


async def fetch_webpage_crawl4ai_docker(urls: list[str]) -> str:
    result, uncached_urls = await make_filtered_output(urls)
    if not uncached_urls:
        return result

    JINA_API_KEY = os.environ.get("JINA_API_KEY")
    print(f"JINA_API_KEY: {JINA_API_KEY}")
    headers = {"Authorization": f"Bearer {JINA_API_KEY}"}
    input_data = {
        "urls": uncached_urls,
        "priority": 10,
        "crawler_config": {
            "type": "CrawlerRunConfig",
            "params": {
                "scraping_strategy": {"type": "WebScrapingStrategy", "params": {}},
                "delay_before_return_html": 5,
                "process_iframes": True,
                "exclude_social_media_domains": [
                    "facebook.com",
                    "twitter.com",
                    "x.com",
                    "linkedin.com",
                    "instagram.com",
                    "pinterest.com",
                    "tiktok.com",
                    "snapchat.com",
                    "reddit.com",
                ],
            },
        },
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:11235/crawl",
            json=input_data,
            headers=headers,
        ) as response:
            if response.status == 200:
                response_json = await response.json()
                for item in response_json["results"]:
                    url = item["url"]
                    title = item["metadata"]["title"]
                    markdown = item["markdown"]["raw_markdown"]
                    # Save the markdown to cache
                    formatted_output = OUTPUT_FORMAT.format(
                        title=title, markdown=markdown
                    )
                    await save_url_cache(url, formatted_output)
                    # Format the output
                    result[url] = formatted_output
            else:
                print(
                    f"Failed to start crawl for {urls}: {response.status} \n{await response.text()}"
                )
                return f"Failed to start crawl for {urls}: {response.status}"
    return result


async def fetch_webpage_jina_cached(url: str) -> str:
    # hash the URL to create a unique key
    url_hash = hashlib.md5(url.encode()).hexdigest()
    # check if the URL is already cached
    cache_file = f"cache/{url_hash}.md"
    if os.path.exists(cache_file):
        async with aiofiles.open(cache_file, "r", encoding="utf-8") as f:
            markdown = await f.read()
            return markdown

    # print(os.environ["JINA_API_KEY"])
    headers = {
        "Authorization": "Bearer " + os.environ["JINA_API_KEY"],
        "X-Timeout": "5",
        "X-With-Iframe": "true",
    }
    async with aiohttp.ClientSession() as session: #jang 여기 고쳐야함
    # async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(f"https://r.jina.ai/{url}", headers=headers) as response:
            if response.status == 200:
                markdown = await response.text()
                # save the markdown to cache
                os.makedirs(os.path.dirname(cache_file), exist_ok=True)
                async with aiofiles.open(cache_file, "w", encoding="utf-8") as f:
                    await f.write(markdown)
                return markdown
            else:
                print(
                    f"Failed to fetch {url}: {response.status}, {await response.text()}"
                )
                return f"Failed to fetch {url}: {response.status}"


async def load_webpages_jina(urls: list[str]) -> dict[str, str]:
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            task = asyncio.create_task(fetch_webpage_jina_cached(url))
            tasks.append(task)

    responses = await asyncio.gather(*tasks)
    results = {}
    for url, markdown in zip(urls, responses):
        results[url] = markdown

    return results


async def fetch_webpages(urls: list[str], use_docker=False) -> dict[str, str]:
    # crawl4ai_urls = [url for url in urls if "blog.naver.com" in url]
    # other_urls = [url for url in urls if "blog.naver.com" not in url]
    other_urls = urls
    crawl4ai_urls = []

    tasks = []
    if crawl4ai_urls:
        if use_docker:
            tasks.append(
                asyncio.create_task(fetch_webpage_crawl4ai_docker(crawl4ai_urls))
            )
        else:
            tasks.append(asyncio.create_task(fetch_webpage_crawl4ai(crawl4ai_urls)))

    tasks.append(asyncio.create_task(load_webpages_jina(other_urls)))
    responses = await asyncio.gather(*tasks)
    results = {}
    for response in responses:
        for url, markdown in response.items():
            results[url] = markdown
    return results


if __name__ == "__main__":
    from pprint import pprint
    from dotenv import load_dotenv

    load_dotenv(verbose=True)

    async def amain():
        print(
            await fetch_webpage_jina_cached(
                # "https://theconversation.com/canadas-2-8-billion-settlement-with-indigenous-day-scholars-is-a-long-time-coming-198491"
                "https://www.rand.org/content/dam/rand/pubs/occasional_papers/2009/RAND_OP258.pdf#:~:text=amnesty%20and%20resettlement%20to%20encourage,Grievance%20program%2C%20teams%20of%20South"
            )
        )

    import asyncio

    asyncio.run(amain())
