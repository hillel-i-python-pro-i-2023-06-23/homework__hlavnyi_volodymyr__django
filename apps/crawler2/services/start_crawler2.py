import asyncio
import logging
import os
import datetime
import threading
from typing import TypeAlias

import aiohttp
import argparse
from urllib.parse import urljoin

import environ
from bs4 import BeautifulSoup

from pathlib import Path

all_found_links = []  # list of all found links
dict_new_sites = {}  # dict of new sites for Crawling

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env = environ.FileAwareEnv()
env.read_env(env_file=BASE_DIR.joinpath(".env"))
FOLDER_FOR_SAVE_RESULT_FILES = BASE_DIR.joinpath(env.str("FOLDER_WITH_DB", default="db"))

T_URL: TypeAlias = str
T_FILENAME: TypeAlias = str


def get_file_name(file_name: T_FILENAME) -> T_FILENAME:
    """
    Get file name with iteration
    :param file_name: - file name
    :return: - file name with iteration
    """
    extension_of_file = file_name.find(".txt")

    return f"{file_name[:extension_of_file]}{file_name[extension_of_file:]}"


def get_initial_list_of_sites_for_crawling() -> list:
    return [
        "https://www.example.com",
        "https://www.djangoproject.com",
        "https://www.wikipedia.org",
    ]


def save_from_file_site_to_list(fileout: T_FILENAME, list_start_site: list) -> None:
    fileout_with_iteration = get_file_name(file_name=fileout)
    fileout_full = str(os.path.join(f"{FOLDER_FOR_SAVE_RESULT_FILES}", fileout_with_iteration))
    if not list_start_site:
        list_start_site = get_initial_list_of_sites_for_crawling()

    with open(fileout_full, "a") as fileout_open:
        for line in list_start_site:
            if isinstance(line, list):
                for sub_line in line:
                    fileout_open.write(f"{sub_line.strip()}\n")
            else:
                fileout_open.write(f"{line.strip()}\n")
        fileout_open.close()


def get_from_file_site_to_list(filein: T_FILENAME, list_start_site: list) -> list:
    """
    Get list of sites from file
    :param filein: - file name
    :return: list of sites
    """

    filein_with_iteration = get_file_name(file_name=filein)
    filein_full = str(os.path.join(f"{FOLDER_FOR_SAVE_RESULT_FILES}", filein_with_iteration))

    if not os.path.exists(filein_full):
        save_from_file_site_to_list(fileout=filein, list_start_site=list_start_site)

    list_sites_for_crawling = []
    with open(filein_full) as filein_open:
        list_sites_for_crawling.extend(line.strip() for line in filein_open)
    filein_open.close()

    return list_sites_for_crawling


def get_correct_url(url: T_URL, base_url: T_URL) -> T_URL:
    if url is None:
        return ""
    if url.startswith("http://") or url.startswith("https://"):
        return url
    else:
        return urljoin(base_url, url)


class Crawler:
    def __init__(self, start_url, max_depth, max_links, logger):
        self.start_url = start_url
        self.max_depth = max_depth
        self.max_links = max_links
        self.visited = set()
        self.to_visit = [start_url]
        self.logger = logger

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def crawl(self, session, url, depth):
        if depth > self.max_depth or len(self.visited) >= self.max_links:
            return

        if url in self.visited:
            return

        self.visited.add(url)
        try:
            html = await self.fetch(session, url)
            soup = BeautifulSoup(html, "html.parser")
            links = [a.get("href") for a in soup.find_all("a", href=True)]
            logging.info(f"Crawling links: {links}")
            tasks_local = []
            for link in links:
                next_url = get_correct_url(url=link, base_url=url)
                logging.info(f"Found link (depth {depth}): {next_url}")
                if next_url not in self.visited:
                    if next_url not in all_found_links:
                        all_found_links.append(next_url)
                        tasks_local.append(self.crawl(session, next_url, depth + 1))

            await asyncio.gather(*tasks_local)

        except Exception as e:
            logging.info(f"Error fetching {url}: {e}")

    async def run(self):
        async with aiohttp.ClientSession() as session:
            await self.crawl(session, self.start_url, 0)


async def async_main(list_sites_for_crawling, depth, max_links, logger, fileout):
    tasks = [run_crawler(link, depth, max_links, logger) for link in list_sites_for_crawling]
    await asyncio.gather(*tasks)
    #    save_from_file_site_to_list(fileout=fileout, list_start_site=all_found_links)
    #    all_found_links = []
    print(f"Finished and saved asyncio worker {list_sites_for_crawling}")


def start_crawling_main():
    parser = argparse.ArgumentParser(description="Async Crawler")
    parser.add_argument("depth", type=int, help="Crawling depth", default=1)
    parser.add_argument("max_links", type=int, help="Maximum number of links to crawl", default=100)
    parser.add_argument("--filein", type=str, help="Name file from take list of site for Crawling", default="in.txt")
    parser.add_argument("--fileout", type=str, help="Name file for save list of site after Crawling", default="out.txt")

    args = parser.parse_args()
    start_crawling_main_part(args.filein, args.fileout, args.depth, args.max_links)


def start_crawling_main_part(
    filein: T_FILENAME = "in.txt", fileout: T_FILENAME = "out.txt", depth: int = 1, max_links: int = 100
):
    logger = logging.getLogger("Crawler")
    logger.setLevel(logging.INFO)

    t_start = datetime.datetime.now()

    list_start_sites = []
    list_sites_for_crawling = get_from_file_site_to_list(filein=filein, list_start_site=list_start_sites)
    # asyncio.run(
    #     async_main(list_sites_for_crawling=list_sites_for_crawling, depth=depth, max_links=max_links, logger=logger)
    # )
    thread_list = []
    for i in range(len(list_sites_for_crawling)):
        t = threading.Thread(
            target=asyncio.run,
            args=(
                async_main(
                    list_sites_for_crawling=[list_sites_for_crawling[i]],
                    depth=depth,
                    max_links=max_links,
                    logger=logger,
                    fileout=fileout,
                ),
            ),
        )
        t.start()
        print(f"Started asyncio worker {list_sites_for_crawling[i].strip()}")
        thread_list.append(t)

    for t in thread_list:
        t.join()  # Wait for the thread to complete

    # Ensure all threads have completed before continuing

    logger.info(f"Finish Crawling for {list_sites_for_crawling}")

    save_from_file_site_to_list(fileout=fileout, list_start_site=all_found_links)

    t_finish = datetime.datetime.now()
    delta = t_finish - t_start
    logger.info(f"---------Time spent for Crawling: {delta.total_seconds()}")


async def run_crawler(start_url, depth, max_links, logger):
    logger.info(f"Start Crawling for {start_url}")
    crawler = Crawler(start_url, depth, max_links, logger)
    await crawler.run()


if __name__ == "__main__":
    start_crawling_main()
