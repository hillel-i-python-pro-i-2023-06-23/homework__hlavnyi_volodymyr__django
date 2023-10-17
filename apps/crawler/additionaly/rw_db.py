import logging

# import threading

from asgiref.sync import sync_to_async

from apps.crawler.additionaly.sites_check import check_is_site_exist
from apps.crawler.models import Site, SubSite


def separate_sites_list(sites_text: str) -> list:
    return sites_text.splitlines()


async def save_sites_list_to_database(url: str, flag_ready: bool) -> None:
    list_of_sites = separate_sites_list(sites_text=url)
    for site_line_url in list_of_sites:
        if site_line_url.strip() != "":
            await save_site_to_database(site_str=site_line_url, flag_ready=flag_ready)


@sync_to_async
def save_site_to_database(site_str: str, flag_ready: bool) -> None:
    logger = logging.getLogger("core")
    logger.info(f"Start Site '{site_str}', Flag '{flag_ready}' to Save to DB")
    site = Site.objects.filter(url=site_str).first()
    if site is None:
        Site.objects.create(url=site_str, flag_was_finished_crawling=flag_ready)
    elif site.flag_was_finished_crawling != flag_ready:
        site.flag_was_finished_crawling = flag_ready
        site.save()


@sync_to_async
def save_sub_site_to_database(site_str: str, sub_url: str, flag_ready: bool) -> None:
    site = Site.objects.filter(url=site_str).first()
    sub_site = SubSite.objects.filter(site_id=site.pk, sub_url=sub_url).first()
    if sub_site is None:
        SubSite.objects.create(site_id=site.pk, sub_url=sub_url, flag_was_finished_crawling=flag_ready)
    elif sub_site.flag_was_finished_crawling != flag_ready:
        sub_site.flag_was_finished_crawling = flag_ready
        sub_site.save()


async def save_site_and_sub_site_to_db(site_str: str, sub_url: str, flag_ready: bool) -> None:
    await save_site_to_database(site_str=site_str, flag_ready=flag_ready)
    await save_sub_site_to_database(site_str=site_str, sub_url=sub_url, flag_ready=flag_ready)


async def save_sub_sites_list_to_database(site_str: str, sub_url: list) -> None:
    logger = logging.getLogger("core")
    for sub_url in sub_url:
        await save_site_and_sub_site_to_db(site_str=site_str, sub_url=sub_url, flag_ready=False)
        if check_is_site_exist(sub_url):  # and (not queryset.flag_was_finished_crawling):
            await save_site_to_database(site_str=sub_url, flag_ready=False)
            await save_site_and_sub_site_to_db(site_str=site_str, sub_url=sub_url, flag_ready=True)
    await save_site_to_database(site_str=site_str, flag_ready=True)
    logger.info(f"Finish Site '{site_str}', Flag True to Save to DB")
