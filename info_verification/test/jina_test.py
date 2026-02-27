
import os
import aiohttp
import aiofiles
import hashlib

url = "https://www.researchgate.net/publication/46556896_Capacity-Constrained_Monopoly"



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


if __name__ == "__main__":
    import asyncio
    markdown = asyncio.run(fetch_webpage_jina_cached(url))
    print(markdown)