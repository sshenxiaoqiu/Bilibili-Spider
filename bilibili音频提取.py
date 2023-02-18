#coding=gbk

import requests
import json
import re

def get_url(url):
    headers = {
        'user-agent': '',
        'referer': 'https://www.bilibili.com/'}
    respose = requests.get(url, headers=headers)
    respose.encoding = respose.apparent_encoding
    return respose

def get_josn_url(url):
    res = get_url(url).text
    title = re.findall('<title data-vue-meta="true">(.*?)_��������_bilibili</title>', res)[0]
    play_info = json.loads(re.findall('<script>window.__playinfo__=(.*?)<script>', res)[0][0:-9])
    audio = play_info['data']['dash']['audio'][0]['baseUrl']
    tit_vi = [title, audio]
    return tit_vi

def save(url):
    json_data = get_josn_url(url)
    title = json_data[0]
    audio_content = get_url(json_data[1]).content
    with open(title + '.mp3', mode='wb') as file:
        file.write(audio_content)

def start(url):
    print('��ʼ����')
    save(url)
    print('�������')

if __name__ == '__main__':
    url = input('������Ƶ���ӣ�')
    start(url)

