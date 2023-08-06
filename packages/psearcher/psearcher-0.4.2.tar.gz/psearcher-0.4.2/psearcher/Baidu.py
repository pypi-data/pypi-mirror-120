from psearcher.BaseEngine import BaseEngine
from retry import retry


class Baidu(BaseEngine):
    url = 'http://www.baidu.com/s'
    keyTag = 'word'
    pageTag = 'pn'
    startIndex = 0
    indexGap = 10

    def get_url_and_parmas(self):
        url = self.url
        params = {
            self.keyTag: self.keyWord,
            self.pageTag: self.startIndex + self.indexGap*self.nextPage,
        }
        return url, params

    def parser(self, soup):
        results = []
        tags = soup.find_all("div", class_="c-container")[1:]
        for tag in tags:
            if not tag.h3 and not tag.p:
                continue
            title = tag.h3.get_text() if tag.h3 else tag.p.get_text()
            try:
                link = self.get_real_link(tag.h3.a.get("href") if tag.h3 else tag.a.get("href"))
            except Exception:
                continue
            else:
                describe = tag.get_text()
                result = {
                    "link": link,
                    "describe": describe,
                    "title": title,
                }
                results.append(result)
        return results

    @retry(tries=3, backoff=1, delay=1)
    def get_real_link(self, baidu_search_link):
        r = self.session.get(baidu_search_link, proxies=self.proxies)
        return r.url
