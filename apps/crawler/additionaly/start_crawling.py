import logging

# import asyncio
from typing import TypeAlias

import bs4

from apps.crawler.additionaly.rw_db import save_sites_list_to_database

T_URL: TypeAlias = str
T_URLS: TypeAlias = list[T_URL]
T_URLS_AS_SET: TypeAlias = set[T_URL]

T_TEXT: TypeAlias = str


def start_crawling(site_text: str):
    logger = logging.getLogger("django")
    logger.info(f"Start Crawling for site_text: {site_text}")

    save_sites_list_to_database(url=site_text, flag_ready=False)

    # queryset = Contact.objects.all()
    #
    # logger.info(f"Current amount of contacts before: {queryset.count()}")
    #
    # for contact in generate_contacts(amount=amount):
    #     contact.save()
    #     add_random_groups(contact=contact)
    #     add_random_info_of_contact(contact=contact)

    # logger.info(f"Current amount of contacts after: {queryset.count()}")


async def get_urls_from_text(text: T_TEXT) -> T_URLS_AS_SET:
    soup = bs4.BeautifulSoup(markup=text, features="html.parser")

    urls = set()
    for link_element in soup.find_all("a"):
        url = link_element.get("href")
        urls.add(url)

    return set(urls)
