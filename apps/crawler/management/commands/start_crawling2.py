from django.core.management.base import BaseCommand

from apps.crawler2.services.start_crawler2 import start_crawling_main_part


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("depth", type=int, help="Crawling depth", default=1)
        parser.add_argument("max_links", type=int, help="Maximum number of links to crawl", default=100)
        parser.add_argument(
            "--filein", type=str, help="Name file from take list of site for Crawling", default="in.txt"
        )
        parser.add_argument(
            "--fileout", type=str, help="Name file for save list of site after Crawling", default="out.txt"
        )

    def handle(self, *args, **options):
        filein: str = options["filein"]
        fileout: str = options["fileout"]
        max_links: int = options["max_links"]
        depth: int = options["depth"]

        start_crawling_main_part(filein=filein, fileout=fileout, depth=depth, max_links=max_links)


if __name__ == "__main__":
    start_crawling_main_part(filein="in.txt", fileout="out.txt", depth=1, max_links=100)
