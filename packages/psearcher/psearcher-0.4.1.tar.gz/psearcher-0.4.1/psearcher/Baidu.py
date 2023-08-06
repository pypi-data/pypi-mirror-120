from psearcher.BaseEngine import BaseEngine
import time

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
                with open("{}.html".format(int(time.time())), "w") as f:
                    f.write(str(tag))

                continue
            title = tag.h3.get_text() if tag.h3 else tag.p.get_text()
            link = self.get_real_link(tag.h3.a.get("href") if tag.h3 else tag.a.get("href"))
            describe = tag.get_text()
            result = {
                "link": link,
                "describe": describe,
                "title": title,
            }
            results.append(result)
        return results

    def get_real_link(self, baidu_search_link):
        r = self.session.get(baidu_search_link, proxies=self.proxies)
        return r.url
