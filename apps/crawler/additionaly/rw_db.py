import logging

from asgiref.sync import sync_to_async

from apps.crawler.models import Site


def separate_sites_list(sites_text: str) -> list:
    return sites_text.splitlines()


async def save_sites_list_to_database(url: str, flag_ready: bool) -> None:
    list_of_sites = separate_sites_list(sites_text=url)
    for site_line_url in list_of_sites:
        # t2 = threading.Thread(target=save_site_to_database, args=(site_line_url, flag_ready))
        # t2.start()
        await save_site_to_database(url=site_line_url, flag_ready=flag_ready)


@sync_to_async
def save_site_to_database(url: str, flag_ready: bool) -> None:
    logger = logging.getLogger("core")
    logger.info(f"Start Site '{url}', Flag '{flag_ready}' to Save to DB")
    queryset = Site.objects.filter(url=url)
    if queryset.count() == 0:
        Site.objects.create(url=url, flag_was_finished_crawling=flag_ready)
    else:
        queryset.update(flag_was_finished_crawling=flag_ready)
