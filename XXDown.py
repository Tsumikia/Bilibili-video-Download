import jsonpath
import requests
import re
import json
import pickle
import os
import subprocess
from lxml import etree
from moviepy.editor import *
from DecryptLogin import login
from tqdm import tqdm  # 实现进度条

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "referer": "https://message.bilibili.com/",
}

if not os.path.exists('./output'):
    os.mkdir('./output')
if not os.path.exists('./buffer.pkl'):
    print('未检测到登录信息, 请扫码登录以获得高清下载资源')
    _, session = login.Login().bilibili()
    with open('buffer.pkl', 'wb') as f:
        pickle.dump(session, f)
    print('登录信息已存储在本目录下buffer.pkl文件')
else:
    with open('buffer.pkl', 'rb') as f:
        session = pickle.load(f)

dir_list = os.listdir()
if 'ffmpeg.exe' not in dir_list:
    print('当前目录下未检测到ffmpeg.exe! 请下载并放置到本目录下!')
    exit()

url = input('请输入要下载视频的网址：')
response = session.get(url=url, headers=headers)
tree = etree.HTML(response.text)
title = tree.xpath('//h1/text()')[0].replace('/', ' ')
print(f'视频标题为{title}\n')
json_data = re.findall(r'<script>window.__playinfo__=(.*?)</script>', response.text)[0]
json_obj = json.loads(json_data)
audio_path_list = jsonpath.jsonpath(json_obj, '$.data.dash.audio.*.baseUrl')

video_path_list = jsonpath.jsonpath(json_obj, '$.data.dash.video.*.baseUrl')
video_support_formats_desc = jsonpath.jsonpath(json_obj, '$.data.support_formats.*.new_description')

audio_codecs_list = jsonpath.jsonpath(json_obj, '$.data.dash.audio.*.codecs')

print(f'共计{len(video_support_formats_desc)}条视频流:')
for index in range(len(video_support_formats_desc)):
    print('\t', video_support_formats_desc[index])

print(f'共计{len(audio_codecs_list)}条音频流:')
for index in range(len(audio_codecs_list)):
    print('\t', audio_codecs_list[index])

print(f'已选择的流:\n\t{video_support_formats_desc[0]}\n\t{audio_codecs_list[0]}')

print('开始下载音频...')
res = requests.get(url=audio_path_list[0], headers=headers, stream=True)
content_size = int(res.headers['Content-Length']) / 1024
with open('./output/' + title + 'buffer' + '.mp3', 'wb') as f:
    for data in tqdm(iterable=res.iter_content(1024), total=content_size, unit='k', desc='音频下载'):
        f.write(data)
print('音频下载完成')

print('开始下载视频...')
res = requests.get(url=video_path_list[0], headers=headers, stream=True)
content_size = int(res.headers['Content-Length']) / 1024

with open('./output/' + title + 'buffer' + '.mp4', 'wb') as f:
    for data in tqdm(iterable=res.iter_content(1024), total=content_size, unit='k', desc='视频下载'):
        f.write(data)
print('视频下载完成')


ffmpeg_path = os.path.join(os.getcwd(), 'ffmpeg.exe')

# 设置输入和输出文件路径
audio_file = './output/' + title + 'buffer' + '.mp3'
video_file = './output/' + title + 'buffer' + '.mp4'
output_file = './output/' + title + '.mp4'

print('开始合并音视频文件...')
with open(os.devnull, 'w') as devnull:
    subprocess.call([ffmpeg_path, '-i', video_file, '-i', audio_file,
                     '-c:v', 'copy', '-c:a', 'aac', output_file],
                    stdout=devnull, stderr=devnull)
print('合并完成')

print('开始删除缓存文件...')
os.remove('./output/' + title + 'buffer' + '.mp4')
os.remove('./output/' + title + 'buffer' + '.mp3')
print('缓存文件删除完成')
print('视频已存放至本目录下output文件夹内')
