#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B站视频搜索和字幕获取工具 - 简洁版
功能：关键词搜索 → 获取视频列表 → 批量下载字幕
"""

import requests
import certifi
import json
import re
import time
import random
import urllib.parse
import os
from hashlib import md5
from functools import reduce
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


# ==================== 配置管理 ====================
def load_config():
    """加载配置文件"""
    config_file = Path(__file__).parent / 'config.json'

    if not config_file.exists():
        print("❌ 配置文件不存在！")
        print("请复制 config.json.example 为 config.json 并填入你的Cookie信息")
        print("获取Cookie方法：")
        print("1. 在浏览器中登录哔哩哔哩")
        print("2. 按F12打开开发者工具")
        print("3. 在Network标签页刷新页面")
        print("4. 找到任意请求，查看请求头中的Cookie")
        print("5. 复制SESSDATA、bili_jct、DedeUserID三个值")
        return None

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 验证必要配置
        cookies = config.get('cookies', {})
        required_fields = ['SESSDATA', 'bili_jct', 'DedeUserID']

        for field in required_fields:
            if not cookies.get(field) or cookies[field].startswith('请在这里'):
                print(f"❌ 配置文件中缺少 {field} 或未正确配置")
                print("请编辑 config.json 文件，填入正确的Cookie信息")
                return None

        return config

    except Exception as e:
        print(f"❌ 配置文件读取失败: {e}")
        return None


# ==================== API 请求封装 ====================
class BilibiliAPI:
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.verify = certifi.where()
        
        # 设置请求头
        headers = config.get('headers', {})
        self.session.headers.update(headers)
        
        # 设置 Cookie
        cookies = config.get('cookies', {})
        self.session.cookies.update(cookies)
        
        # 请求频率控制
        self.last_request_time = 0
        self.min_delay = config.get('settings', {}).get('request_delay_min', 1)
        self.max_delay = config.get('settings', {}).get('request_delay_max', 3)

    def _rate_limit(self):
        """请求频率控制"""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        if elapsed < self.min_delay:
            sleep_time = self.min_delay - elapsed + random.uniform(0, 0.5)
            time.sleep(sleep_time)
        else:
            time.sleep(random.uniform(0, self.min_delay))
            
        self.last_request_time = time.time()

    def search_videos(self, keyword, page=1, page_size=10):
        """搜索视频"""
        self._rate_limit()
        
        url = "https://api.bilibili.com/x/web-interface/search/type"
        params = {
            'search_type': 'video',
            'keyword': keyword,
            'page': page,
            'page_size': page_size
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                return data.get('data', {}).get('result', [])
            else:
                print(f"❌ 搜索失败: {data.get('message', '未知错误')}")
                return []
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return []

    def get_video_info(self, bvid):
        """获取视频详细信息"""
        self._rate_limit()
        
        url = "https://api.bilibili.com/x/web-interface/view"
        params = {'bvid': bvid}
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                return data.get('data')
            else:
                print(f"❌ 获取视频信息失败: {data.get('message', '未知错误')}")
                return None
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return None

    def get_subtitle_list(self, bvid):
        """获取视频字幕列表"""
        self._rate_limit()
        
        url = "https://api.bilibili.com/x/player/v2"
        params = {'bvid': bvid}
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                subtitle_info = data.get('data', {}).get('subtitle', {})
                subtitles = subtitle_info.get('subtitles', [])
                return subtitles
            else:
                print(f"❌ 获取字幕信息失败: {data.get('message', '未知错误')}")
                return []
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return []

    def download_subtitle(self, subtitle_url):
        """下载字幕文件"""
        self._rate_limit()
        
        try:
            response = self.session.get(subtitle_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ 下载字幕失败: {e}")
            return None


# ==================== 字幕处理 ====================
def parse_subtitle_time(time_str):
    """解析字幕时间戳"""
    # 处理 B站字幕时间格式: 00:00:00,123
    match = re.match(r'(\d+):(\d+):(\d+),(\d+)', time_str)
    if match:
        hours, minutes, seconds, milliseconds = map(int, match.groups())
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
        return total_seconds
    return 0


def format_time(total_seconds):
    """格式化时间为 mm:ss 或 hh:mm:ss"""
    if total_seconds >= 3600:
        return f"{int(total_seconds//3600):02d}:{int((total_seconds%3600)//60):02d}:{int(total_seconds%60):02d}"
    else:
        return f"{int(total_seconds//60):02d}:{int(total_seconds%60):02d}"


def convert_to_markdown(subtitle_data, video_title, output_dir):
    """将字幕转换为 Markdown 格式"""
    if not subtitle_data or 'body' not in subtitle_data:
        return None
        
    # 清理文件名
    safe_title = re.sub(r'[\\/*?:"<>|]', '_', video_title)[:50]
    
    # 创建输出目录
    output_path = Path(output_dir) / f"{safe_title}.md"
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {video_title}\n\n")
            
            for item in subtitle_data['body']:
                if 'from' in item and 'content' in item:
                    start_time = parse_subtitle_time(item['from'])
                    formatted_time = format_time(start_time)
                    content = item['content'].strip()
                    
                    f.write(f"## {formatted_time}\n")
                    f.write(f"{content}\n\n")
        
        return output_path
        
    except Exception as e:
        print(f"❌ 保存字幕失败: {e}")
        return None


# ==================== 主要功能函数 ====================
def search_videos(api, keyword, min_play_count=50000, max_results=5):
    """搜索高质量视频"""
    print(f"🔍 搜索关键词: {keyword}")
    
    videos = api.search_videos(keyword, page_size=max_results)
    filtered_videos = []
    
    for video in videos:
        try:
            play_count = video.get('play', 0)
            
            if play_count >= min_play_count:
                video_info = {
                    'bvid': video.get('bvid'),
                    'title': video.get('title', '').replace('<em class="keyword">', '').replace('</em>', ''),
                    'author': video.get('author'),
                    'play_count': play_count,
                    'description': video.get('description', '')[:100]
                }
                filtered_videos.append(video_info)
        except Exception as e:
            continue
    
    return filtered_videos


def download_subtitle_for_video(api, bvid, output_dir="subtitles"):
    """下载单个视频的字幕"""
    print(f"📥 正在下载视频 {bvid} 的字幕...")
    
    # 获取视频信息
    video_info = api.get_video_info(bvid)
    if not video_info:
        print(f"❌ 获取视频信息失败: {bvid}")
        return None
    
    video_title = video_info.get('title', '未知标题')
    print(f"📹 视频标题: {video_title}")
    
    # 获取字幕列表
    subtitles = api.get_subtitle_list(bvid)
    if not subtitles:
        print(f"⚠️  视频 {bvid} 没有找到字幕")
        return None
    
    # 下载第一个中文字幕
    for subtitle in subtitles:
        if '中文' in subtitle.get('lan_doc', '') or subtitle.get('lan') == 'zh-CN':
            subtitle_url = subtitle.get('url')
            if subtitle_url:
                subtitle_data = api.download_subtitle(subtitle_url)
                if subtitle_data:
                    output_path = convert_to_markdown(subtitle_data, video_title, output_dir)
                    if output_path:
                        print(f"✅ 字幕下载成功: {output_path}")
                        return output_path
            break
    
    print(f"❌ 视频 {bvid} 没有找到中文字幕")
    return None


def batch_download_subtitles(api, bvid_list, output_dir="subtitles", max_workers=3):
    """批量下载字幕"""
    print(f"🚀 开始批量下载 {len(bvid_list)} 个视频的字幕...")
    
    # 创建输出目录
    Path(output_dir).mkdir(exist_ok=True)
    
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_bvid = {executor.submit(download_subtitle_for_video, api, bvid, output_dir): bvid for bvid in bvid_list}
        
        for future in as_completed(future_to_bvid):
            bvid = future_to_bvid[future]
            try:
                result = future.result()
                results.append({'bvid': bvid, 'success': result is not None, 'path': result})
            except Exception as e:
                print(f"❌ 下载 {bvid} 时出现异常: {e}")
                results.append({'bvid': bvid, 'success': False, 'error': str(e)})
    
    # 统计结果
    success_count = sum(1 for r in results if r['success'])
    print(f"\n📊 下载完成: 成功 {success_count}/{len(bvid_list)} 个")
    
    return results


# ==================== 命令行接口 ====================
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='B站视频搜索和字幕获取工具')
    parser.add_argument('command', choices=['search', 'download', 'batch'], help='执行的操作')
    parser.add_argument('keyword_or_bvid', nargs='+', help='搜索关键词或BV号')
    parser.add_argument('--output', '-o', default='subtitles', help='输出目录')
    parser.add_argument('--min-play', '-m', type=int, default=50000, help='最小播放量')
    parser.add_argument('--max-results', '-r', type=int, default=5, help='最大搜索结果数')
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config()
    if not config:
        return
    
    # 初始化API
    api = BilibiliAPI(config)
    
    # 执行操作
    if args.command == 'search':
        keyword = ' '.join(args.keyword_or_bvid)
        videos = search_videos(api, keyword, args.min_play, args.max_results)
        
        if videos:
            print(f"\n📺 找到 {len(videos)} 个视频:")
            for i, video in enumerate(videos, 1):
                print(f"{i}. {video['title']}")
                print(f"   BV号: {video['bvid']}")
                print(f"   作者: {video['author']}")
                print(f"   播放量: {video['play_count']:,}")
                print(f"   简介: {video['description']}\n")
        else:
            print("❌ 没有找到符合条件的视频")
    
    elif args.command == 'download':
        bvid = args.keyword_or_bvid[0]
        result = download_subtitle_for_video(api, bvid, args.output)
        if not result:
            print("❌ 字幕下载失败")
    
    elif args.command == 'batch':
        bvid_list = args.keyword_or_bvid
        results = batch_download_subtitles(api, bvid_list, args.output)
        
        # 显示详细结果
        for result in results:
            if result['success']:
                print(f"✅ {result['bvid']}: {result['path']}")
            else:
                print(f"❌ {result['bvid']}: {result.get('error', '失败')}")


if __name__ == '__main__':
    main()