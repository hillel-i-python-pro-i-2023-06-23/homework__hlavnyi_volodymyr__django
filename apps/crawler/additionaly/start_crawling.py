import asyncio
import logging

from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.crawler.additionaly.init_logging import init_logging
from apps.crawler.additionaly.rw_db import save_sites_list_to_database
from apps.crawler.additionaly.search_subsite import async_search_for_site_sub_sites_from_db


async def start_crawling(site_text: str):
    init_logging()
    logger = logging.getLogger("core")
    #
    logger.info(f"Start Crawling for site_text: \n{site_text}")
    await save_sites_list_to_database(url=site_text, flag_ready=False)
    #
    logger.info("Start search Sub Sites")
    await async_search_for_site_sub_sites_from_db()
    logger.info("Finished to search to DB list of Sub sites")
    #
    # await update_sites_list()


async def update_sites_list():
    await asyncio.sleep(0.5)
    return redirect(reverse_lazy("crawler:sites_list"))
