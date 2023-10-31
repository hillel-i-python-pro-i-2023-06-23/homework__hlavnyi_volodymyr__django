import asyncio
import logging
from typing import TypeAlias

import aiohttp
import bs4

T_URL: TypeAlias = str
T_URLS: TypeAlias = list[T_URL]
T_URLS_AS_SET: TypeAlias = set[T_URL]

T_TEXT: TypeAlias = str


async def get_urls_from_text(text: T_TEXT) -> T_URLS_AS_SET:
    soup = bs4.BeautifulSoup(markup=text, features="html.parser")
    urls = set()
    for link_element in soup.find_all("a"):
        url = link_element.get("href")
        if url is not None and url.find("http") != -1 and url not in urls:
            urls.add(url)

    return set(urls)


async def make_request(
    url: T_URL,
    session: aiohttp.ClientSession,
    logger: logging.Logger,
) -> T_TEXT:
    text_for_return = ""
    logger.info(f"Start request for url: {url}")
    try:
        async with session.get(url) as response:
            if response.status == 200:
                text_for_return = await response.text()
            else:
                logger.error(f"HTTP error {response.status} for url: {url}")
    except aiohttp.ClientError as e:
        logger.error(f"Client error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    return text_for_return


async def handle_url(url: T_URL, session: aiohttp.ClientSession, logger: logging.Logger) -> T_URLS:
    text = await make_request(url=url, session=session, logger=logger)
    urls_as_set = await get_urls_from_text(text=text)
    return list(urls_as_set)


async def async_search_for_site_sub_sites_from_list(sites_list: list, logger: logging.Logger) -> tuple:
    async with aiohttp.ClientSession(
        cookie_jar=aiohttp.DummyCookieJar(),
    ) as session:
        tasks_search = [handle_url(url=url, session=session, logger=logger) for url in sites_list]
        list_for_return_sites = await asyncio.gather(*tasks_search)

    return list_for_return_sites
