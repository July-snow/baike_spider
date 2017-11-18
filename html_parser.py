import urllib.parse

import re
from bs4 import BeautifulSoup


class HtmlParser(object):
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser')
        new_urls = self.get_new_urls(page_url, soup)
        new_data = self.get_new_data(page_url, soup)
        return new_urls, new_data

    @staticmethod
    def get_new_urls(page_url, soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r"/item/(.*)"))
        for link in links:
            new_url = link.get_text()
            new_full_url = urllib.parse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    @staticmethod
    def get_new_data(page_url, soup):
        res_data = {}
        ## <dd class="lemmaWgt-lemmaTitle-title"> <h1>Python</h1></dd>

        # 地址
        res_data['url'] = page_url

        # 标题
        title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find('h1')
        res_data['title'] = title_node.get_text()
        print(res_data['title'])
        """"
        < div class ="lemma-summary" label-module="lemmaSummary" >       
        < / div >
        """
        # 内容
        summary_node = soup.find('div', class_="lemma-summary")
        res_data['summary'] = summary_node.get_text()
        return res_data
