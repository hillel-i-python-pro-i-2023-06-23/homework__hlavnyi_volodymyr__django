import logging
import datetime

from django.core.management.base import BaseCommand

from apps.crawler.management.commands.file_operations import (
    get_from_file_site_to_list,
    get_crawling_site_from_list_to_tuple,
    save_from_file_site_to_list,
    print_list,
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--level", type=int, help="Verbosity level", default=1)
        parser.add_argument(
            "--filein", type=str, help="Name file from take list of site for Crawling", default="in.txt"
        )
        parser.add_argument(
            "--fileout", type=str, help="Name file for save list of site after Crawling", default="out.txt"
        )
        parser.add_argument(
            "--show-progress",
            action="store_true",
            help="Show progress bar",
        )

    def handle(self, *args, **options):
        filein: str = options["filein"]
        fileout: str = options["fileout"]
        verbosity_level: int = options["level"]
        show_progress: bool = options["show_progress"]

        start_crawling(
            filein=filein,
            fileout=fileout,
            verbosity_level=verbosity_level,
            show_progress=show_progress,
        )


def start_crawling(filein: str, fileout: str, verbosity_level: int, show_progress: bool):
    logger = logging.getLogger("django")
    logger.setLevel(logging.INFO)

    t_start = datetime.datetime.now()
    list_new_site = []
    logger.info("---------Start Crawling")

    for current_level in range(1, verbosity_level + 1):
        create_paket_crawling(logger, current_level, verbosity_level, filein, fileout, list_new_site, show_progress)

    logger.info("---------Finish Crawling")
    t_finish = datetime.datetime.now()
    delta = t_finish - t_start
    logger.info(f"---------Time spent for Crawling: {delta.total_seconds()}")


def create_paket_crawling(logger, current_level, verbosity_level, filein, fileout, list_new_site, show_progress):
    logger.info(f"---------Start cycle {current_level} of {verbosity_level} ---")

    # step 1
    list_sites_for_crawling = get_from_file_site_to_list(
        filein=filein, list_start_sites=list_new_site, number_of_iteration=current_level
    )

    # step 2
    list_new_site = get_crawling_site_from_list_to_tuple(list_sites_for_crawling=list_sites_for_crawling)

    # step 3
    save_from_file_site_to_list(fileout=fileout, list_new_site=list_new_site, number_of_iteration=current_level)
    logger.info(f"---------Finish cycle {current_level} of {verbosity_level} ---")

    print_list(show_progress=show_progress, list_new_site=list_new_site, logger=logger)


if __name__ == "__main__":
    start_crawling(filein="in.txt", fileout="out.txt", verbosity_level=2, show_progress=True)
