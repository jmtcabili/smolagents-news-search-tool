from smolagents.tools import Tool
from urllib.parse import quote_plus
import json
import re
import requests
import trafilatura
import xml.etree.ElementTree as ET
from markdownify import markdownify
from googlenewsdecoder import gnewsdecoder
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import warnings


# # """
# # I want an agent to search for news revolving around Anthropic, OpenAI, and Google. 
# #         For this sample agent, it will get news from reuters and read articles that can be
# #         found under these URLs:
# #         Reuters: https://www.reuters.com/site-search/?query={{company}}
# #         CNN: https://edition.cnn.com/search?q={{company}}&from=0&size=10&page=1&sort=newest&types=all&section=
# #         Then from their scraped content, summarize latest news and compare how articles 
# #         present the information 
# # """

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# outlets that are generally scrapeable; edit freely
SITES = ["theguardian.com", "techcrunch.com", "theverge.com", "arstechnica.com", "cnbc.com"]

def structureLink (RSSItem) -> dict: 
    title = RSSItem.findtext("title")
    description = RSSItem.findtext("description")
    link = RSSItem.findtext("link")
    date = RSSItem.findtext("pubDate")

    def clean_text(html_text): 
        soup = BeautifulSoup(html_text, "html.parser")
        return soup.get_text()

    warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
    return {
        "title": clean_text(title), 
        "description": clean_text(description), 
        "link": clean_text(link), 
        "date": clean_text(date)
    }


class NewsSearchTool(Tool):
    name =  "news_search"
    description = "Fetches and summarizes news on a given tech company from an RSS feed"
    inputs = {'company': 
                {
                    'type': 'string',
                    'description': 'the company to perform the search queries on'
                 }
             }
    output_type = 'string'

    def _read_article(self, link, snippet): 
        try:

            #decode url from google rss
            decoded = gnewsdecoder(link, interval=1)
            if not decoded.get("success"): 
                return "hatdog"

            real_url = decoded["decoded_url"]

            #fetch request
            res = requests.get(real_url, headers=HEADERS, timeout=20)
            res.raise_for_status() #Raise an exception for bad status codes

            #check if response url is still news.google -> did not redirect
            if "news.google.com" in res.url:
                return snippet
            
            #get text from response as markdown
            text = trafilatura.extract(
                res.text,
                include_links=False,
                include_images=False,
                include_comments=False,
                include_tables=False,
            )

            if not text or len(text) < 300:      # paywall or empty extraction
                return None
            return text[:10000]
        except requests.RequestException:
            return snippet

    def forward(self, company: str) -> str: 

        #fetch RSS feed
        sites = " OR ".join(f"site:{s}" for s in SITES)
        query = f"{company} ({sites})"
        url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en-US&gl=US&ceid=US:en"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        items = ET.fromstring(r.content).findall("./channel/item") #what is this for?

        #group links and titles
        links = []
        for it in items[:10]: 
            links.append(structureLink(it))

        #parse text from links
        for article in links:
            article["text"] = self._read_article(link=article["link"], snippet=article["description"])

        return json.dumps(links, indent=2, ensure_ascii=False)


    


        




    