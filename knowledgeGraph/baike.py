import os
import re
from urllib import parse
from bs4 import BeautifulSoup
import jieba
from urllib import request
import requests
from lxml import etree
import urllib
import urllib.parse
import urllib.request
import copy


# 爬虫主程序入口
class MainCrawler():

    def getHTMLText(self, url):  # 判断是否异常并返回文本信息
        try:
            headers = {
                'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
            r = requests.get(url, timeout=30, headers=headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            return "error"

    def down_load(self, url):
        if url is None:
            return None
        else:
            rt = request.Request(url=url, method='GET')  # 发GET请求
            with request.urlopen(rt) as rp:  # 打开网页
                if rp.status != 200:
                    return None
                else:
                    return rp.read()  # 读取网页内容

        # 每个词条中，可以有多个超链接

    # main_url指url公共部分，如“https://baike.baidu.com/”
    def _get_new_url(self, main_url, soup):
        # baike.baidu.com/
        # <a target="_blank" href="/item/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1%E8%AF%AD%E8%A8%80" rel="external nofollow" >计算机程序设计语言</a>
        new_urls = set()
        # 解析出main_url之后的url部分
        child_urls = soup.find_all('a', href=re.compile(r'/item/(\%\w{2})+'))
        for child_url in child_urls:
            new_url = child_url['href']
            # 再拼接成完整的url
            full_url = parse.urljoin(main_url, new_url)
            new_urls.add(full_url)
        return new_urls

    # 每个词条中，只有一个描述内容，解析出数据（词条，内容）
    def _get_new_data(self, main_url, soup):
        new_datas = {}
        new_datas['url'] = main_url
        # <dd class="lemmaWgt-lemmaTitle-title"><h1>计算机程序设计语言</h1>...
        new_datas['title'] = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1').get_text()
        # class="lemma-summary" label-module="lemmaSummary"...
        new_datas['content'] = soup.find('div', attrs={'label-module': 'lemmaSummary'},
                                         class_='lemma-summary').get_text()
        return new_datas

    # 解析出url和数据（词条，内容）
    def parse(self, main_url, html_cont):
        if main_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'lxml', from_encoding='utf-8')
        new_url = self._get_new_url(main_url, soup)
        new_data = self._get_new_data(main_url, soup)
        return new_url, new_data

    # 结巴分词处理
    def jieba_deal(self, content):
        first_txt_content = []
        first_txt_content.append(content)
        first_txt_tokens = list(jieba.cut(''.join(first_txt_content)))
        stopword_path = os.getcwd()
        # 获取去停用词
        stopwords = []
        with open(os.path.join(stopword_path, 'knowledgeGraph\\stopwords.txt'), 'r') as f:
            for stopword in f.readlines():
                stopwords.append(stopword.strip())  # 读取每行的去停用词的时候需要把后面的换行去除，否则下面循环匹配去停用词的时候，根本都匹配不上

        final_txt_tokens = []
        # 将文本中的停用词进行出去
        for token in first_txt_tokens:
            if token not in stopwords:
                final_txt_tokens.append(token)
        # print(len(final_txt_tokens))

        res = final_txt_tokens
        # print(res)
        next = []
        flag = 0
        for i in range(len(res)):
            key = res[i]
            if key == '涉及' or key == "包含" or key == "包括":
                if res[i - 1] != "不":
                    flag = 1

            if key == "等" or key == "等等":
                break

            if flag == 1:
                next.append(key)

        try:
            del next[0]
        except:
            next = []
        return next

    # 开始爬虫方法
    def start_craw(self, list_name):
        # print('爬虫开始...')
        # print(list_name)
        try:
            new_url = 'https://baike.baidu.com/item/' + urllib.parse.quote(list_name)
            html_cont = self.down_load(new_url)
            new_urls, new_data = self.parse(new_url, html_cont)
            content = new_data["content"].replace("\n", "")
            datas = self.jieba_deal(content)
            new_datas = []

            # 进行分词合并
            for i in range(len(datas) - 1):
                url = 'https://baike.baidu.com/item/' + urllib.parse.quote(datas[i] + datas[i + 1])
                demo = self.getHTMLText(url)
                html = etree.HTML(demo)

                # 利用XPATH进行爬取#
                title = html.xpath('/html/head/title/text()')
                if title[0] == "百度百科——全球领先的中文百科全书":
                    new_datas.append(datas[i + 1])
                else:
                    new_datas.append(datas[i] + datas[i + 1])

            datas = copy.deepcopy(new_datas)
            lenth = 0
            for i in range(1, len(new_datas) - 1):
                if new_datas[i] in new_datas[i + 1] or new_datas[i] in new_datas[i - 1]:
                    del datas[i - lenth]
                    lenth += 1

            for i in range(len(datas)):
                if datas[i] == "[]":
                    del datas[i]
                    del datas[i]
                    break

            for i in range(len(datas)):
                if datas[i] == list_name:
                    del datas[i]
                    break
            # print(list_name, datas)
            # print(datas)
        except:
            datas = []
            # print(list_name, datas)
        return datas, (len(datas) is None)


def getBaiKe(label, mc):
    # mc = MainCrawler()
    items, tag = mc.start_craw(label)
    print(items)
    return items, tag

# getBaiKe()
