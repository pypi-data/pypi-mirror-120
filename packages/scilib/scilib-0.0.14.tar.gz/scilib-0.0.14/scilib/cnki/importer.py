# coding: utf-8

from __future__ import unicode_literals, absolute_import, print_function, division

import os
import re
import json
import asyncio
import datetime
import concurrent
from pathlib import Path
from collections import Counter
from pyquery import PyQuery

FIELDS = [
    'SrcDatabase',
    'Title',
    'Author',
    'Organ',
    'Source',
    'Keyword',
    'Summary',
    'PubTime',
    'FirstDuty',
    'Fund',
    'Year',
    'Volume',
    'Period',
    'PageCount',
    'CLC',
]


def parse_txt_file(file_path):
    """ 解析自定义导出文件
    """
    with open(file_path) as f:
        content = f.read()

    articles = {}
    currentIndex = 0
    currentField = None
    for line in content.split('\n'):
        if line.startswith('SrcDatabase-'):
            currentField = 'SrcDatabase'
            content = line[(line.index(':') + 1):].strip()
            article = articles.setdefault(currentIndex, {})
            if article:
                currentIndex += 1
                article = articles.setdefault(currentIndex, {})
                article[currentField] = article.get(currentField, '') + content
            else:
                article[currentField] = article.get(currentField, '') + content
        elif [i for i in FIELDS if line.startswith(i + '-')]:
            currentField = line.split('-')[0]
            content = line[(line.index(':') + 1):].strip()
            article = articles.setdefault(currentIndex, {})
            article[currentField] = article.get(currentField, '') + content
        else:
            content = line
            article = articles.setdefault(currentIndex, {})
            article[currentField] = article.get(currentField, '') + content
    return articles.values()


def read_text_format_dir(from_dir):
    for file in Path(from_dir).glob('**/*.txt'):
        yield from parse_txt_file(file)


def _parse_list_date(list_date):
    try:
        list_date = list_date.split()[0]
        tokens = list_date.split('-')
        y = int(tokens[0])
        m = int(tokens[1])
        d = int(tokens[2])
        return datetime.date(y, m, d).strftime(r'%Y-%m-%d')
    except Exception:
        return None


def read_spider_format(file_path):
    print('file_path', file_path)
    base_dir = os.path.dirname(file_path)
    files = os.listdir(base_dir)
    txt_file = [i for i in files if i.endswith('.txt')][0]
    htmls_file = [i for i in files if i.endswith('.json')][0]
    items = parse_txt_file(os.path.join(base_dir, txt_file))

    with open(os.path.join(base_dir, htmls_file)) as f:
        htmls = json.load(f)['htmls']

    list_items = []
    for html in htmls:
        for row in PyQuery(html).find('tr'):
            pq_row = PyQuery(row)
            list_name = pq_row.find('.name a').text().strip()
            if not list_name:
                continue
            list_marktip = pq_row.find('.name .marktip').text().strip()
            list_author = pq_row.find('.author').text().strip()
            list_source = pq_row.find('.source').text().strip()
            list_date = pq_row.find('.date').text().strip()
            list_data = pq_row.find('.data').text().strip()

            try:
                list_quote = int(pq_row.find('.quote').text().strip() or 0)
                list_download = int(pq_row.find('.download').text().strip() or 0)
            except (ValueError, TypeError):
                continue
            # print(
            #     f'list_name={list_name} list_marktip={list_marktip} list_author={list_author}'
            #     f'list_source={list_source} list_date={list_date} list_data={list_data}'
            #     f'list_quote={list_quote} list_download={list_download}'
            # )

            icon_collect = pq_row.find('.icon-collect')[0]
            list_dbname = icon_collect.attrib['data-dbname']
            list_filename = icon_collect.attrib['data-filename']
            list_id = f'dbname={list_dbname}&filename={list_filename}'

            list_date_format = _parse_list_date(list_date)
            if not list_date_format:
                print('list_date_format error:', list_date, list_date_format)

            list_item = dict(
                list_name=list_name,
                list_marktip=list_marktip,
                list_author=list_author,
                list_source=list_source,
                list_date=list_date,
                list_date_format=_parse_list_date(list_date),
                list_data=list_data,
                list_quote=list_quote,
                list_download=list_download,
                list_dbname=list_dbname,
                list_filename=list_filename,
                list_id=list_id,
            )
            list_items.append(list_item)

    if len(items) != len(list_items):
        print('len(items)', len(items))
        print('len(list_items)', len(list_items))
        print('error: list items length error', '=' * 50)
        # raise ValueError('list items length error')
        yield from iter([])
    for item, list_item in zip(items, list_items):
        item.update(list_item)

    yield from iter(items)


def read_spider_format_dir(from_dir):
    for file in Path(from_dir).glob('**/end'):
        yield from read_spider_format(file)


async def read_spider_format_dir_parallel(from_dir, callback, *args):
    """ parallel read
    """
    loop = asyncio.get_running_loop()
    futures = []
    with concurrent.futures.ProcessPoolExecutor() as pool:
        for file_path in Path(from_dir).glob('**/end'):
            future = loop.run_in_executor(pool, callback, file_path, *args)
            futures.append(future)
    return await asyncio.gather(*futures, return_exceptions=False)


def collect_keywords(items, keyword_field='Keyword', year_field='Year', keyword_replace_map=None, top_size=50):
    """ 搜集关键词
    """

    keyword_replace_map = keyword_replace_map or {}
    keywords = []
    keywords_map = {}
    tokens_list = []
    for item in items:
        keyword = item.get(keyword_field, '') or ''
        year = item.get(year_field, '') or ''
        if str(keyword) == 'nan' or str(year) == 'nan' or len(str(int(year))) != 4:
            continue
        tokens = re.split(r'[,;，]', keyword)
        tokens = list(set([keyword_replace_map.get(i.strip(), i.strip()) for i in tokens if i and i.strip()]))
        keywords.extend(tokens)
        keywords_map.setdefault(year, []).extend(tokens)
        tokens_list.append((year, tokens))
    counter = Counter(keywords)
    counter_map = {k: Counter(v) for k, v in keywords_map.items()}

    top_n = [k for k, v in counter.most_common(top_size)]
    print(top_n)
    years_items = []
    years_items_flat = []
    for year, year_keywords in keywords_map.items():
        years_items_flat.extend([dict(year=year, keyword=k) for k in year_keywords if k in top_n])
        for keyword in top_n:
            if keyword in year_keywords:
                years_items.append([f'{int(year)}', year_keywords.count(keyword), keyword])
    print(years_items)

    corrs = []
    for keyword1 in top_n:
        print(keyword1 + ',', end='')
        for index, keyword2 in enumerate(top_n):
            count = len([True for year, tokens in tokens_list if keyword1 in tokens and keyword2 in tokens])
            corrs.extend([
                dict(year=year, keyword1=keyword1, keyword2=keyword2)
                for year, tokens in tokens_list if keyword1 in tokens and keyword2 in tokens
            ])
            if (index + 1) == top_size:
                print(str(count), end='')
            else:
                print(str(count) + ',', end='')
        print('')

    return counter, counter_map, years_items_flat, corrs
