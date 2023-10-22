import os
import asyncio

from apps.crawler.additionaly.search_subsite_file import async_search_for_site_sub_sites_from_list


def get_from_file_site_to_list(filein: str, list_start_sites: list, number_of_iteration: int) -> list:
    """
    Get list of sites from file
    :param filein: - file name
    :param number_of_iteration:  - number of iteration
    :return: list of sites
    """

    filein_with_iteration = get_file_name_with_iteration(file_name=filein, number_of_iteration=number_of_iteration)
    filein_full = str(os.path.join(f"{os.getcwd()}/db/", filein_with_iteration))

    if not os.path.exists(filein_full):
        save_from_file_site_to_list(
            fileout=filein, list_new_site=list_start_sites, number_of_iteration=number_of_iteration
        )

    list_sites_for_crawling = []
    with open(filein_full) as filein_open:
        list_sites_for_crawling.extend(iter(filein_open))
    filein_open.close()

    return list_sites_for_crawling


def get_crawling_site_from_list_to_tuple(list_sites_for_crawling: list) -> tuple:
    return asyncio.run(async_search_for_site_sub_sites_from_list(sites_list=list_sites_for_crawling))


def save_from_file_site_to_list(fileout: str, list_new_site: list, number_of_iteration: int) -> None:
    fileout_with_iteration = get_file_name_with_iteration(file_name=fileout, number_of_iteration=number_of_iteration)
    fileout_full = str(os.path.join(f"{os.getcwd()}/db/", fileout_with_iteration))
    if not list_new_site:
        list_new_site = get_initial_list_of_sites_for_crawling()

    with open(fileout_full, "w") as fileout_open:
        for line in list_new_site:
            if isinstance(line, list):
                for sub_line in line:
                    fileout_open.write(f"{sub_line}\n")
            else:
                fileout_open.write(f"{line}\n")
        fileout_open.close()


def get_file_name_with_iteration(file_name: str, number_of_iteration: int) -> str:
    """
    Get file name with iteration
    :param number_of_iteration:
    :param file_name: - file name
    :return: - file name with iteration
    """
    extension_of_file = file_name.find(".txt")

    return f"{file_name[:extension_of_file]}{number_of_iteration}{file_name[extension_of_file:]}"


def print_list(show_progress: bool, list_new_site, logger):
    if show_progress:
        # for line_start in list_sites_for_crawling:
        for line in iter(list_new_site):
            if isinstance(line, list):
                for sub_line in line:
                    logger.info(f"----- Site {str(sub_line).rstrip()} ----")
            else:
                logger.info(f"\n----- Site {str(line).rstrip()} ----")


def get_initial_list_of_sites_for_crawling() -> list:
    return [
        "https://www.example.com/\n",
        "https://example.com/\n",
        "https://www.djangoproject.com/\n",
        "https://www.facebook.com/\n",
        "https://www.wikipedia.org/\n",
        "https://ithillel.ua\n",
        "https://www.linkedin.com\n",
        "https://www.twitter.com /\n",
        "https://www.live.com/\n",
        "https://cambridge.ua\n",
        "https://www.codewars.com\n",
        "https://cnn.com\n",
    ]
