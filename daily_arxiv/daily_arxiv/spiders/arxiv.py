import os

import scrapy


class ArxivSpider(scrapy.Spider):
    name = "arxiv"  # 爬虫名称
    allowed_domains = ["arxiv.org"]  # 允许爬取的域名

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        configured_categories = os.environ.get("CATEGORIES", "cs.CV").split(",")
        self.target_categories = []
        seen_categories = set()
        for category in (item.strip() for item in configured_categories):
            if not category or category in seen_categories:
                continue
            seen_categories.add(category)
            self.target_categories.append(category)

        self.start_urls = [
            f"https://arxiv.org/list/{cat}/new" for cat in self.target_categories
        ]

    @staticmethod
    def _section_type(li) -> str:
        text = " ".join(
            item.strip() for item in li.css("::text").getall() if item.strip()
        ).lower()
        if "new submissions" in text:
            return "new"
        if "cross submissions" in text or "cross-lists" in text:
            return "cross"
        if "replacement submissions" in text or "replacements" in text:
            return "replacement"
        return "unknown"

    def parse(self, response):
        page_category = response.url.rstrip("/").split("/")[-2]
        section_starts = []
        for li in response.css("div[id=dlpage] ul li"):
            href = li.css("a::attr(href)").get()
            if href and "item" in href:
                section_starts.append(
                    (int(href.split("item")[-1]), self._section_type(li))
                )

        for paper in response.css("dl dt"):
            paper_anchor = paper.css("a[name^='item']::attr(name)").get()
            if not paper_anchor:
                continue

            abstract_link = paper.css("a[title='Abstract']::attr(href)").get()
            if not abstract_link:
                continue

            arxiv_id = abstract_link.split("/")[-1]
            paper_index = int(paper_anchor.split("item")[-1])

            listing_type = "unknown"
            for section_start, section_name in section_starts:
                if paper_index < section_start:
                    break
                listing_type = section_name

            yield {
                "id": arxiv_id,
                "source_category": page_category,
                "listing_type": listing_type,
            }
