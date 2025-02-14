#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ai import AI
from storage import Storage


def run():
    """Run the application."""
    contents, lang = get_contents()

    print("文章已抓取，片段数量：", len(contents))
    for content in contents:
        print('\t', content)

    ai = AI()

    # 1. 对文章的每个段落生成embedding
    embeddings, tokens = ai.create_embeddings(contents)
    print("已创建嵌入，嵌入数量：", len(embeddings), "，使用的令牌数：", tokens, "，花费：", tokens / 1000 * 0.0004, "美元")

    storage = Storage()
    storage.clear()
    storage.add_all(embeddings)
    print("已存储嵌入")
    print("=====================================")
    # 2. 生成embedding式摘要，有基于SIF的加权平均和一般的直接求平均，懒得中文分词了这里使用的是直接求平均，英文可以改成SIF
    summary = ai.generate_summary(embeddings, num_candidates=100, use_sif=lang not in ['zh', 'ja', 'ko', 'hi', 'ar', 'fa'])
    print(f"已生成摘要：{summary}")
    print("=====================================")

    while True:
        query = input("请输入查询(help可查看指令)：")
        if query == "quit":
            break
        elif query == "help":
            print("输入limit [数字]设置limit")
            print("输入quit退出")
            continue

        # 1. 对问题生成embedding
        embedding = ai.create_embedding(query)
        # 2. 从数据库中找到最相似的片段
        texts = storage.get_texts(embedding[1])
        print("已找到相关片段（前5个）：")
        for text in texts[:5]:
            print('\t', text)
        # 3. 把相关片段推给AI，AI会根据这些片段回答问题
        answer = ai.completion(query, texts)
        print(answer.strip())
        print("=====================================")


def web_crawler_newspaper(url) -> (list[str], str):
    """Run the web crawler."""
    from newspaper import fulltext
    raw_html, lang = _get_raw_html(url)
    text = fulltext(raw_html, language=lang)
    contents = [text.strip() for text in text.splitlines() if text.strip()]
    return contents, lang


def _get_raw_html(url):
    from readability import Document
    from langdetect import detect
    from requests import get
    doc = Document(get(url).text)
    html = doc.summary()
    lang = detect(html)
    return html, lang[0:2]


def get_contents() -> (list[str], str):
    """Get the contents."""
    while True:
        try:
            url = input("请输入文章链接：")
            return web_crawler_newspaper(url)
        except Exception as e:
            print("Error:", e)


if __name__ == '__main__':
    run()
