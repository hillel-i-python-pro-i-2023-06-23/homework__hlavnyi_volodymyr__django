import asyncio
import logging
from typing import TypeAlias

import aiohttp
import bs4
from asgiref.sync import sync_to_async

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
        urls.add(url)

    return set(urls)


async def make_request(
    url: T_URL,
    session: aiohttp.ClientSession,
    logger: logging.Logger,
) -> T_TEXT:
    async with session.get(url) as response:
        logger.info(response.status)
        return await response.text()


async def handle_url(url: T_URL, session: aiohttp.ClientSession) -> T_URLS:
    logger = get_custom_logger(name=url)
    text = await make_request(url=url, session=session, logger=logger)
    urls_as_set = await get_urls_from_text(text=text)
    return list(urls_as_set)


def database_sync_to_async(list):
    pass


@sync_to_async
def get_list_of_sites(flag_ready: bool = False) -> list:
    # return list(Site.objects.filter(flag_was_finished_crawling=flag_ready))
    apps = await database_sync_to_async(list)(Site.objects.filter(flag_was_finished_crawling=flag_ready))
    for app in apps:
        # app_json = ApplicationSerializer(app).data
        # await self.send_json({"action": "create", "data": app_json})
        pass


async def search_for_site_sub_sites_from_db():
    site_list = get_list_of_sites(False)
    # for site in site_list:
    # print(site.url)
    async with aiohttp.ClientSession(
        cookie_jar=aiohttp.DummyCookieJar(),
    ) as session:
        tasks_search = [handle_url(url=url, session=session) for url in site_list]
        result_search = await asyncio.gather(*tasks_search)
        # result = await handle_url(url=site.url, session=session)
    for result in result_search:
        print(result_search)


# def search_for_site_sub_sites_from_db():
#     site_list = list(Site.objects.filter(flag_was_finished_crawling=False))
#     for site in site_list:
#         print(site.url)
#         async with aiohttp.ClientSession(
#                 cookie_jar=aiohttp.DummyCookieJar(),
#         ) as session:
#             # tasks_search = [handle_url(url=url, session=session) for url in site_list]
#             # result_search = await asyncio.gather(*tasks_search)
#             result = handle_url(url=site.url, session=session)
#         # for result in result_search:
#         print(result)


async def test_fetch(client, url: str):
    async with client.get(url) as resp:
        assert resp.status == 200
        return await resp.text()


async def test_main():
    site_list = list(Site.objects.filter(flag_was_finished_crawling=False))
    for site in site_list:
        print(site.url)
        async with aiohttp.ClientSession() as client:
            html = await test_fetch(client, site.url)
            print(html[:200])


if __name__ == "__main__":
    asyncio.run(test_main())
    # asyncio.get_event_loop().run_until_complete(main())
