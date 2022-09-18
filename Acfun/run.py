# _*_ coding: utf-8 _*_
# @Time: 2022/9/18 13:47
# @Author: lemon
# @File: run
# @Project: spider-100
import json
import os.path
import re
import shutil
from urllib.parse import urljoin

import requests

from common.utils import get_common_headers


def run(acid):
    # 从网页中提取视频信息
    url = f'https://www.acfun.cn/v/{acid}'
    v_url = r'https://ali-safety-video.acfun.cn/mediacloud/acfun/acfun_video/'
    headers = {
        'referer': 'https://www.acfun.cn/'
    }
    headers.update(get_common_headers())
    resp = requests.get(url, headers=headers)
    video_info = re.search('window.videoInfo = (.*?);', resp.text).group(1)
    video_info = json.loads(video_info)
    title = video_info['title']
    filename = f'{title}.mp4'
    path = f'./resource/{acid}/'

    # 取m3u8链接
    play_json = json.loads(video_info['currentVideoInfo']['ksPlayJson'])
    m3u8_url = play_json['adaptationSet'][0]['representation'][0]['url']

    # 取每个切片的链接
    m_slice = requests.get(m3u8_url, headers=headers).text
    temps = re.findall('#EXTINF(.*?),\n(.*?)\n', m_slice)
    urls = [urljoin(v_url, item[1]) for item in temps]

    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

    # 请求所有切片拼接成完整视频
    print(f'开始下载视频切片...\n数量:{len(urls)}')
    for url in urls:
        resp = requests.get(url, headers=headers)
        with open(path + filename, 'ab') as f:
            f.write(resp.content)
    print(f'{filename}  下载完成.')


if __name__ == '__main__':
    run('ac36838840')
