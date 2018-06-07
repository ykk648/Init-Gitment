#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import json

site_url = 'https://ykksmile.top/'
sitemap_url = 'https://ykksmile.top/sitemap.xml'
token = 'token '+'********'
username = 'cloisonne'
repo_name = 'cloisonne.github.io'


def getHTMLText(url):
    try:
        kv = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
        r = requests.get(url, timeout=30, headers=kv)
        r.raise_for_status()  # 检查状态码
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"

wb_data = getHTMLText(sitemap_url)

pattern = re.compile('<loc>([a-zA-z]+://[^\s]*)</loc>')
urls = pattern.findall(str(wb_data))

print(urls)

for url in urls:
    url_data = getHTMLText(url)
    title_pattern = re.compile('<title>(.+)</title>')
    title = title_pattern.search(url_data).group(1).replace('&#39;','\'')
    print(title.replace('&#39;','\''))
    headers = {
        "Accept": "application/vnd.github.squirrel-girl-preview, application/vnd.github.html+json",
        "Accept-Encoding": "gzip, deflate, br",
        'Connection': 'keep-alive',
        'Host': 'api.github.com',
        'Origin': site_url,
        "Referer": url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
        'Authorization': token
    }
    payload = {
        'title': title,
        'labels': ['gitment', url],
        'body': url
    }
    payload_json = json.dumps(payload)
    feedback = requests.post('https://api.github.com/repos/'+username+'/'+repo_name+'/issues',headers=headers,data=payload_json)
    print(feedback)
