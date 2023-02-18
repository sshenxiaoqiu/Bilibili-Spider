
import requests
import json
import re
import os

def get_url(url):

    # user-agent需自己提供

    headers = {
        'user-agent': '',
        'referer': 'https://www.bilibili.com/'}
    respose = requests.get(url, headers=headers)
    respose.encoding = respose.apparent_encoding
    return respose

def get_josn_url(url):
    res = get_url(url).text
    title = re.findall('<title data-vue-meta="true">(.*?)_哔哩哔哩_bilibili</title>', res)[0]
    play_info = json.loads(re.findall('<script>window.__playinfo__=(.*?)<script>', res)[0][0:-9])
    audio = play_info['data']['dash']['audio'][0]['baseUrl']
    video = play_info['data']['dash']['video'][0]['baseUrl']
    tit_au_vi = [title, video, audio]
    return tit_au_vi

def save(url):
    json_data = get_josn_url(url)
    title = json_data[0]
    video_content = get_url(json_data[1]).content
    audio_content = get_url(json_data[2]).content
    with open(title + '.mp4', mode='wb') as file:
        file.write(video_content)
    with open(title + '.mp3', mode='wb') as file:
        file.write(audio_content)
    merge(title)

def start(url):
    print('开始下载')
    save(url)
    print('下载完成')

def merge(title):

    # 需要ffmpeg提供合并视频和音频
    # path为ffmpeg.exe所在位置

    path = '' + '\\ffmpg.exe'
    cmd = f'{path} -y -i "{title}.mp4" -i "{title}.mp3" -vcodec copy -acodec copy 1234.mp4'
    os.system(cmd)
    os.system(f'del "{title}.mp4"')
    os.system(f'del "{title}.mp3"')
    os.system(f'rename 1234.mp4 "{title}.mp4"')

if __name__ == '__main__':
    url = input('输入视频BV号：')
    start(url)