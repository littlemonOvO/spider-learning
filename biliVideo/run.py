# _*_ coding: utf-8 _*_
# @Time: 2022/9/13 18:24
# @Author: lemon
# @File: run
# @Project: spider-100
import json
import os
import re
import shutil
import threading

import requests
from moviepy.editor import AudioFileClip, VideoFileClip

from common.utils import get_common_headers, NetworkException


class MergeThread(threading.Thread):
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename
        super().__init__()

    def run(self):
        print('开始合并视频音频...')
        ad = AudioFileClip(f'{self.path}.mp3')
        vd = VideoFileClip(f'{self.path}.mp4')
        vd.set_audio(ad).write_videofile(f'{self.filename}.mp4', logger=None)
        print(f'【{self.filename}】合并完成.')
        os.remove(f'{self.path}.mp3')
        os.remove(f'{self.path}.mp4')


def run(bvid):
    url = f'https://www.bilibili.com/video/{bvid}'
    headers = {
        'referer': 'https://www.bilibili.com',
    }
    headers.update(get_common_headers())

    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            pass
        elif resp.status_code == 404:
            raise NetworkException(resp.status_code, msg=f'Bv号为【{bvid}】的视频不存在.')
        else:
            raise NetworkException(resp.status_code, msg='未知错误')
    except NetworkException:
        print(NetworkException)

    video_str = re.search('<script>window.__playinfo__=(.*?)</script>', resp.text).group(1)
    info_str = re.search(r'<script>window.__INITIAL_STATE__=(.*?);\(function', resp.text).group(1)
    info_data = json.loads(info_str)
    video_name = info_data['videoData']['title']
    up_name = info_data['upData']['name']
    bv_id = info_data['videoData']['bvid']
    video_data = json.loads(video_str)
    dash = video_data['data']['dash']
    video_url = dash['video'][0]['baseUrl']
    audio_url = dash['audio'][0]['baseUrl']

    try:
        print('视频音频下载开始...')
        video_content = requests.get(video_url, headers=headers).content
        audio_content = requests.get(audio_url, headers=headers).content
        print('视频音频下载完成.')
    except Exception:
        raise Exception

    try:
        path = f'./resource/{bv_id}/'
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)

        with open(path + video_name + '.mp4', 'wb') as f:
            f.write(video_content)
        with open(path + video_name + '.mp3', 'wb') as f:
            f.write(audio_content)
        return MergeThread(path + video_name, f'{path}【{up_name}】 {video_name}')
    except Exception:
        raise Exception


if __name__ == '__main__':
    bvid = input('请输入视频Bv号:')
    while len(bvid) > 0:
        thread = run(bvid)
        thread.start()
        bvid = input('\n请输入视频Bv号:')
    print('Exit.')
