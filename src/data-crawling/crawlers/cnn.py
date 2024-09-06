from aws_lambda_powertools import Logger
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from crawlers.base import BaseAbstractCrawler
from documents import ArticleDocument


logger = Logger(service="decodingml/crawler")

class CnnCrawler(BaseAbstractCrawler):
    model = ArticleDocument

    def set_extra_driver_options(self, options) -> None:
        options.add_argument(r"--profile-directory=Profile 2")

    def extract(self, link: str, **kwargs) -> None:
        logger.info(f"Starting scrapping CNN article: {link}")

        self.driver.get(link)
        self.scroll_page()

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        title = soup.find_all("h1", class_="headline__text inline-placeholder vossi-headline-primary-core-light")
        content = soup.find_all("div", class_="article__content")
        authors = soup.find_all("span", class_="byline__name")

        author_id = authors[0].string
        for i in range(1, len(authors)):
            author_id += ", " + authors[1].string

        data = {
            "Title": title[0].string if title else None,
            "Subtitle": None,
            "Content": content[0].text,
        }

        logger.info(f"Successfully scraped and saved article: {link}")
        self.driver.close()
        instance = self.model(
            platform="medium", content=data, link=link, author_id=author_id
        )
        instance.save()

