import asyncio
import logging
from typing import TypeAlias

import aiohttp
import bs4
from asgiref.sync import sync_to_async

from apps.crawler.additionaly.rw_db import save_sub_site_list_to_database
from apps.crawler.models import Site

from apps.crawler.additionaly.loggers import get_custom_logger

T_URL: TypeAlias = str
T_URLS: TypeAlias = list[T_URL]
T_URLS_AS_SET: TypeAlias = set[T_URL]

T_TEXT: TypeAlias = str


async def get_urls_from_text(text: T_TEXT) -> T_URLS_AS_SET:
    soup = bs4.BeautifulSoup(markup=text, features="html.parser")
    urls = set()
    for link_element in soup.find_all("a"):
        url = link_element.get("href")
        # Save only http and https urls.
        if url is not None and url.find("http") != -1:
            urls.add(url)

    return set(urls)


async def make_request(
    url: T_URL,
    session: aiohttp.ClientSession,
    logger: logging.Logger,
) -> T_TEXT:
    try:
        async with session.get(url) as response:
            logger.info(response.status)
            return await response.text()
    except Exception as e:
        logger.error(f"Exception: {e}")
        return ""


async def handle_url(url: T_URL, session: aiohttp.ClientSession) -> T_URLS:
    logger = get_custom_logger(name=url)
    text = await make_request(url=url, session=session, logger=logger)
    urls_as_set = await get_urls_from_text(text=text)
    await save_sub_site_list_to_database(site_str=url, sub_url=list(urls_as_set), flag_ready=True)
    return list(urls_as_set)


@sync_to_async
def async_get_list_of_sites_from_db(flag_ready: bool = False) -> T_URLS:
    sites = Site.objects.filter(flag_was_finished_crawling=flag_ready)
    return ["".join(site.url) for site in list(sites)]


async def async_search_for_site_sub_sites_from_db(max_number_of_pass: int = 2) -> None:
    number_of_pass = 1
    while True:
        sites_list = await async_get_list_of_sites_from_db(flag_ready=False)
        if len(sites_list) == 0 or number_of_pass > max_number_of_pass:
            break
        async with aiohttp.ClientSession(
            cookie_jar=aiohttp.DummyCookieJar(),
        ) as session:
            tasks_search = [handle_url(url=url, session=session) for url in sites_list]
            await asyncio.gather(*tasks_search)
        number_of_pass += 1
