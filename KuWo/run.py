# _*_ coding: utf-8 _*_
# @Time: 2022/9/13 16:31
# @Author: lemon
# @File: run
# @Project: spider-100

import prettytable as pt
import requests

from common.utils import get_common_headers

url = r'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key=%E5%91%A8%E6%9D%B0%E4%BC%A6&pn=1&rn=30&httpsStatus=1&reqId=e03b6ae2-333f-11ed-a876-6116e2c203a1'
headers = {
    'Cookie': r'_ga=GA1.2.1013379811.1663058069; _gid=GA1.2.2093251282.1663058069; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1663058069; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1663058248; kw_token=HB68AXT2HMJ',
    'csrf': r'HB68AXT2HMJ',
    'Host': r'www.kuwo.cn',
    'Referer': r'http://www.kuwo.cn',
}
headers.update(get_common_headers())

tb = pt.PrettyTable()
tb.field_names = ['序号', '歌名', '歌手', '专辑']

resp = requests.get(url, headers=headers)
json_data = resp.json()
data_list = json_data['data']['list']
for i, data in enumerate(data_list):
    artist = data['artist']
    name = data['name']
    album = data['album']
    rid = data['rid']
    tb.add_row([i + 1, name, artist, album])

print(tb)
