import requests
import re

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}
session = requests.session()

def get_article(url):
    res = session.get(url, headers=headers)
    article_list = re.findall('<pre class="replay-info-txt answer_con">(.*?)</pre>', res.text, re.S)[0]
    sub_link = re.sub('<A .*?>.*?</A>', '', article_list, flags=re.S)

    article = re.sub('更多.*?参考', '更多的资料可以到图优教育网参考', sub_link)
    return article


if __name__ == '__main__':
    url_ids = ['q355880446']
    for url_id in url_ids:
        url = f'https://wenwen.sogou.com/z/{url_id}.htm'
        get_article(url)
