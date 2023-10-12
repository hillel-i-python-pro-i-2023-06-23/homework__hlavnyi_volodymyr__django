import logging


def start_crawling(site_text: str) -> None:
    logger = logging.getLogger("django")
    logger.info(f"Start Crawling for site_text: {site_text}")

    # queryset = Contact.objects.all()
    #
    # logger.info(f"Current amount of contacts before: {queryset.count()}")
    #
    # for contact in generate_contacts(amount=amount):
    #     contact.save()
    #     add_random_groups(contact=contact)
    #     add_random_info_of_contact(contact=contact)

    # logger.info(f"Current amount of contacts after: {queryset.count()}")
