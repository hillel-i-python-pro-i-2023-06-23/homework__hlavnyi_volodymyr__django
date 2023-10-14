import asyncio
import logging

from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.crawler.additionaly.init_logging import init_logging
from apps.crawler.additionaly.rw_db import save_sites_list_to_database
from apps.crawler.additionaly.search_subsite import search_for_site_sub_sites_from_db

# from apps.crawler.additionaly.search_subsite import test_main, async_search_for_site_sub_sites_from_db
# from apps.crawler.models import Site


# from apps.crawler.additionaly.search_subsite import async_search_for_site_sub_sites_from_db


async def start_crawling(site_text: str):
    init_logging()
    logger = logging.getLogger("core")
    logger.info(f"Start Crawling for site_text: \n{site_text}")
    # t = threading.Thread(target=save_sites_list_to_database,
    # args = (site_text, False,) )
    # t.start()
    await save_sites_list_to_database(url=site_text, flag_ready=False)
    logger.info("Finished to save to DB list of Sites")
    # logger.info("Wait 1 sec and then go to sites_list")
    # asyncio.run(update_sites_list())
    logger.info("Start search Sub Sites")
    # asyncio.run(async_search_for_site_sub_sites_from_db())
    await search_for_site_sub_sites_from_db()
    # site_list = list(Site.objects.filter(flag_was_finished_crawling=False))
    # search_for_site_sub_sites_from_db()
    # await main()
    logger.info("Finish search Sub Sites")


async def update_sites_list():
    await asyncio.sleep(1)
    return redirect(reverse_lazy("crawler:sites_list"))
