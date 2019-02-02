#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@author:
@file: main.py.py
@time: 2019/1/3
@desc:
'''

import argparse
import requests
import logging
import json
import os
import sys
import time
# from multiprocessing.dummy import Pool
# from functools import partial

LOG_LEVEL = logging.INFO
LOG_FILE = 'download.log' or False
LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s'
HEADERS = {
    'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def get_args():
    parser = argparse.ArgumentParser(
        usage="python main_mli_music.py 网易云音乐用户ID",
        description="根据网易云音乐歌单, 下载对应无损MP3歌曲到本地."
    )
    parser.add_argument('user_id', type=str, help="网易云音乐用户ID")
    parse_result = parser.parse_args()
    user_id = parse_result.user_id
    return user_id


def set_logger():
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if LOG_FILE:
        fh = logging.FileHandler(LOG_FILE)
        fh.setLevel(LOG_LEVEL)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


# 歌单
def get_song_list_list(user_id):
    url = "https://music_download.24mz.cn/test.php?types=userlist&uid=" + \
          str(user_id) + "&cache=9a94264bceaad353ef72684c2f01bb76&_=1549000709303"
    response = requests.get(url, headers=HEADERS)
    # dict
    response_json = json.loads(response.text)
    song_list_list_final= {}
    song_list = {}
    if response_json['code'] == 200:
        song_list_list = response_json['playlist']
        for list in song_list_list:
            # 字典里添加字典
            song_list[list['id']] = {'song_list_id':list['id'], 'song_list_name':list['name']}
            song_list_list_final.update(song_list)
    else:
        song_list_list_final = None

    if not song_list_list_final:
        logger.error('歌单为空 url\n')
        sys.exit(1)

    return song_list_list_final


# 歌单歌曲列表
def get_song_list(song_list_id, song_list_name):
    url = "https://music_download.24mz.cn/test.php?types=playlist&id=" + \
          str(song_list_id) + "&cache=9a94264bceaad353ef72684c2f01bb76&_=1549007084893"
    response = requests.get(url, headers=HEADERS)
    response_json = json.loads(response.text)
    if response_json['code'] == 200:
        song_list = response_json['playlist']['tracks']
        song_list_final= {}
        song_info = {}
        for song in song_list:
            song_info[song['id']] = {'music_id':song['id'], 'music_name':song['name'], 'singer':song['ar'][0]['name'], 'music_path':os.getcwd() + '/music/mli/' + song_list_name + '/'}
            song_list_final.update(song_info)
    else:
        song_list_final = None

    if not song_list_final:
        logger.error('歌单歌曲列表为空 url\n')
        sys.exit(1)

    return song_list_final


# 歌曲信息
def get_song_list_info(song_list):
    song_list_info_final= {}
    song_list_info= {}
    logger.info('******获取歌曲信息开始******')
    # for song_id in song_list:
    #     song = song_list[song_id]
    # 获取index值判断 enumerate 或者 range
    for i,song_id in enumerate(song_list):
        # if i >= 30 and i <= 49:
            song = song_list[song_id]
            logger.info('歌曲名称：%s' % song['music_name'])
            url = "https://music_download.24mz.cn/test.php?types=url&id=" + \
              str(song_id) + "&source=netease&cache=9a94264bceaad353ef72684c2f01bb76&_=1549000709305"
            response = requests.get(url, headers=HEADERS)
            response_json = json.loads(response.text)
            if not response_json:
                logger.error('歌曲信息无法解析 url\n')
                continue
            else:
                song.update({'music_url':response_json['url'].strip()})
                song_list_info[song_id] = song
                song_list_info_final.update(song_list_info)
            logger.info('************')
        # else:
        #     continue
    logger.info('******获取歌曲信息结束******')


    if not song_list_info_final:
        logger.error('歌曲信息列表为空 url\n')
        sys.exit(1)

    return song_list_info_final


# 下载歌曲
def download_song(song_list_info):
    for song_id in song_list_info:
        music_name = song_list_info[song_id]['music_name']
        singer = song_list_info[song_id]['singer']
        music_path = song_list_info[song_id]['music_path']
        music_url = song_list_info[song_id]['music_url']
        # 拼接歌曲名称
        file_name = "{0}-{1}.mp3".format(music_name, singer)
        file_path = os.path.join(music_path, file_name)
        if os.path.exists(file_path):
            logger.info("***文件存在跳过***")
            continue
        else:
            logger.info("下载URL: %s" % music_url)
            logger.info("下载中: %s" % file_path)
            if music_url != '':
                response = requests.get(music_url, headers=HEADERS, timeout=3)
                # 视频是二进制数据流，content就是为了获取二进制数据的方法
                data = response.content
                # 创建路径
                make_dir(music_path)
                f = open(file_path, 'wb')
                f.write(data)
                f.close()
                # with open(file_path, 'wb') as f:
                #     for chunk in response.iter_content(chunk_size=1024):
                #         if chunk:
                #             f.write(chunk)
                logger.info("下载完成: %s " % file_path)
            else:
                logger.info("下载失败: %s " % file_path)
            logger.info('************')


#检测目录创建目录
def make_dir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


def main():
    # 开始时间
    start = time.time()
    # 获取命令行参数
    user_id = get_args()
    # 根据用户ID获取网易云音乐用户歌单
    song_list_list = get_song_list_list(user_id)
    # 输出歌单ID列表方便用户选择
    logger.info("******获取用户歌单列表开始******")
    for song_list_id in song_list_list:
        # logger.info("用户歌单ID: %s" % str(song_list_id))
        logger.info("用户歌单ID: %s" % str(song_list_list[song_list_id]['song_list_id']))
        logger.info("用户歌单名称: %s" % song_list_list[song_list_id]['song_list_name'])
        logger.info("************")
    logger.info("******用户歌单列表结束******")
    # 用户选择下载歌单ID
    song_list_id = input('>>>输入歌单ID<<<')
    # 根据歌单ID获取歌单歌曲列表
    # 注意类型 转 整型
    song_list = get_song_list(song_list_id, song_list_list[int(song_list_id)]['song_list_name'])
    # 手动指定歌单
    # song_list = get_song_list(3778678, '云音乐热歌榜')
    print(song_list)
    # 获取歌曲下载链接
    song_list_info = get_song_list_info(song_list)
    # 下载歌曲
    logger.info("获取歌曲信息完成，开始下载。")
    download_song(song_list_info)
    # 结束时间
    end = time.time()
    logger.info("共耗时 %s s", str(end - start))


# 禁止 requests 模块使用系统代理
os.environ['no_proxy'] = '*'
logger = set_logger()

if __name__ == "__main__":
    main()