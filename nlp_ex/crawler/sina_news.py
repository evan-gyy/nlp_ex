import requests
import pandas as pd
import time
from pyquery import PyQuery as pq
from pyhanlp import *
from snownlp import SnowNLP
from django.http import JsonResponse


headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.6 Safari/537.36',
        'upgrade-insecure-requests': '1'
}
pos_num, neg_num, neu_num = 0, 0, 0
pos_text, neg_text = "", ""
titles = []


def get_pages(request):
    global pos_num, neg_num, neu_num, pos_text, neg_text
    search_word = request.POST.get('search_word')
    base_url = f"https://search.sina.com.cn/?q={search_word}&c=news&from=channel&ie=utf-8"
    result_list = []
    # 翻页爬取新闻
    for page in range(1, 4):
        time.sleep(0.5)
        print(f'正在爬取第{page}页...')
        if page == 1:
            response = requests.get(base_url, headers=headers)
            if response.status_code == 200:
                # 第一次请求成功时保存cookies供翻页时使用
                cookies = response.cookies
                data = parse_page(response.text)
                result_list += data
        else:
            url = base_url + f"&col=&range=&source=&country=&size=&time=&a=&page={page}&pf=0&ps=0&dpc=1"
            response = requests.get(url, headers=headers,cookies=cookies)
            if response.status_code == 200:
                cookies = response.cookies
                data = parse_page(response.text)
                result_list += data
        print(data)
    # 数据整合
    total = float(pos_num + neu_num + neg_num)
    print(total)
    result_dict = {
        'data': result_list,
        'stat': {
            'num': {
                'pos_num': pos_num,
                'neg_num': neg_num,
                'neu_num': neu_num,
                'total_num': total
            },
            'per': {
                'pos_per': pos_num / total,
                'neg_per': neg_num / total,
                'neu_per': neu_num / total
            }
        },
        'word': {
            'pos_word': list(HanLP.extractPhrase(pos_text, 20)),
            'neg_word': list(HanLP.extractPhrase(neg_text, 20))
        }
    }
    pos_num, neg_num, neu_num = 0, 0, 0
    pos_text, neg_text = "", ""
    titles = []
    return JsonResponse(result_dict)


def parse_page(html):
    global pos_num, neg_num, neu_num, pos_text, neg_text
    doc = pq(html)
    # 检测是否搜索到新闻
    if not doc(".l_v2").text()[6:-1]:
        print('请求失败')
        return 0
    print(doc(".l_v2").text())
    data_list = []
    for news in doc(".box-result").items():
        # 标题去重
        title = news("h2 > a").text()
        if title in titles:
            continue
        else:
            titles.append(title)
        # 作者和时间
        both = news("h2 > span").text().split(' ')
        if len(both) == 3:
            author = both[0]
            if author == '黑猫投诉':
                continue
        else:
            author = "佚名"
        time = both[-2] + " " + both[-1]
        # 情感分析
        abstract = news(".content").text()
        if not abstract:
            continue
        mix = title+"，"+abstract
        score1 = SnowNLP(title).sentiments
        score2 = SnowNLP(abstract).sentiments
        if score1 > 0.4 and score1 < 0.6 or score2 > 0.4 and score2 < 0.6:
            score = score2
            sentiment = 0.5
            neu_num += 1
        elif score1 <= 0.4 and score2 <= 0.4:
            score = min(score1, score2)
            sentiment = 0
            neg_num += 1
            neg_text += mix
        else:
            score = max(score1, score2)
            sentiment = 1
            pos_num += 1
            pos_text += mix
        data = {
            'title': title,
            'author': author,
            'time': time,
            'abstract': abstract,
            'link': news("h2 > a").attr('href'),
            'score': score,
            'sentiment': sentiment,
        }
        data_list.append(data)
    return data_list


def get_detail(link):
    # 爬取k.sina开头网站中的文章内容
    if 'k.sina' in link:
        res = requests.get(link, headers=headers)
        if res.status_code == 200:
            res.encoding = 'utf-8'
            html = res.text
            doc = pq(html)
            article = doc('#artibody p').text()
            return article
    else:
        return None


def to_excel(data):
    columns = ['title', 'author', 'time', 'abstract', 'score', 'sentiment', 'link']
    fm = pd.DataFrame(data, columns=columns)
    fm.to_excel('sina_news.xlsx')
    print('成功写入excel')


if __name__ == '__main__':
    data_list = get_pages('科比')
    print(data_list)
    # to_excel(data_list)

    # 提取单篇文章测试
    # test_link = 'https://k.sina.com.cn/article_2620088113_9c2b5f3102000s8h0.html?from=news&subch=onews'
    # content = get_detail(test_link)
    # print(content)

