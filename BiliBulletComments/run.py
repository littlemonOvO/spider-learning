# _*_ coding: utf-8 _*_
# @Time: 2022/9/18 18:34
# @Author: lemon
# @File: run
# @Project: spider-100
import json
import os
import re
import xml.etree.ElementTree as ET

import jieba
import matplotlib.pyplot as plt
import requests
from wordcloud.wordcloud import WordCloud

from common.utils import get_common_headers


def run(bvid):
    url = f'https://www.bilibili.com/video/{bvid}'
    headers = {
        'referer': 'https://www.bilibili.com',
    }
    headers.update(get_common_headers())

    resp = requests.get(url, headers=headers)
    info_data = json.loads(re.search(r'<script>window.__INITIAL_STATE__=(.*?);\(function', resp.text).group(1))
    cid = info_data['videoData']['cid']

    comment_url = f'https://comment.bilibili.com/{cid}.xml'
    with open('./comment.xml', 'wb') as f:
        f.write(requests.get(comment_url, headers=headers).content)

    tree = ET.parse('./comment.xml')
    root = tree.getroot()
    comments = [item.text for item in root.findall('d')]
    comments_list = jieba.lcut(''.join(comments), cut_all=False)
    txt = ' '.join(comments_list)
    wc = WordCloud(
        background_color='white',
        width=1000,
        height=800,
        font_path='msyh.ttc'
    )
    wc.generate(txt)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    os.remove('./comment.xml')


if __name__ == '__main__':
    run('BV16X4y1g7wT')
