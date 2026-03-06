#!/usr/bin/env python3
"""Audit all pages' Rank Math meta: title, description, focus keyword, and content."""

import requests
import json
import re

WP_URL = "https://evidepo.com"
WP_USER = "admin"
WP_APP_PASS = "HQmY kKaQ kDY6 W91l v4G5 sHtA"

session = requests.Session()
session.auth = (WP_USER, WP_APP_PASS)


def get_all_items(post_type):
    items = []
    page = 1
    while True:
        resp = session.get(f"{WP_URL}/wp-json/wp/v2/{post_type}", params={
            "per_page": 100, "page": page, "status": "publish", "context": "edit"
        })
        if resp.status_code != 200:
            break
        data = resp.json()
        if not data:
            break
        items.extend(data)
        tp = int(resp.headers.get("X-WP-TotalPages", 1))
        if page >= tp:
            break
        page += 1
    return items


def get_rankmath_meta(post_id):
    resp = session.get(f"{WP_URL}/wp-json/seo-machine/v1/post-meta/{post_id}", params={"filter": "rank_math"})
    if resp.status_code != 200:
        return {}
    meta = {}
    for m in resp.json():
        meta[m["key"]] = m["value"]
    return meta


def strip_html(text):
    return re.sub(r'<[^>]+>', '', text or '')


def count_keyword_in_text(text, keyword):
    if not keyword or not text:
        return 0
    return text.lower().count(keyword.lower())


# Process all publish pages and posts
for post_type in ["pages", "posts"]:
    print(f"\n{'='*80}")
    print(f"  {post_type.upper()}")
    print(f"{'='*80}")

    items = get_all_items(post_type)

    for item in items:
        pid = item["id"]
        title = item["title"].get("raw", item["title"].get("rendered", ""))
        slug = item["slug"]
        raw_content = item.get("content", {}).get("raw", "")
        plain_content = strip_html(raw_content)
        word_count = len(plain_content.split())

        meta = get_rankmath_meta(pid)
        score = meta.get("rank_math_seo_score", "N/A")
        focus_kw = meta.get("rank_math_focus_keyword", "")
        seo_title = meta.get("rank_math_title", "")
        seo_desc = meta.get("rank_math_description", "")

        # Check issues
        issues = []
        if not focus_kw:
            issues.append("NO_FOCUS_KEYWORD")
        if not seo_title:
            issues.append("NO_SEO_TITLE")
        if not seo_desc:
            issues.append("NO_SEO_DESC")
        if seo_desc and len(seo_desc) < 120:
            issues.append(f"SHORT_DESC({len(seo_desc)}ch)")
        if seo_desc and len(seo_desc) > 160:
            issues.append(f"LONG_DESC({len(seo_desc)}ch)")
        if seo_title and len(seo_title) > 60:
            issues.append(f"LONG_TITLE({len(seo_title)}ch)")
        if focus_kw and seo_title and focus_kw.lower() not in seo_title.lower():
            issues.append("FK_NOT_IN_TITLE")
        if focus_kw and seo_desc and focus_kw.lower() not in seo_desc.lower():
            issues.append("FK_NOT_IN_DESC")
        if word_count < 300 and post_type == "posts":
            issues.append(f"THIN_CONTENT({word_count}w)")

        # Focus keyword in content
        fk_count = count_keyword_in_text(plain_content, focus_kw) if focus_kw else 0

        print(f"\n[{pid}] {title}")
        print(f"  Slug: {slug}")
        print(f"  Score: {score} | Words: {word_count} | FK in content: {fk_count}x")
        print(f"  Focus KW: {focus_kw}")
        print(f"  SEO Title: {seo_title}")
        print(f"  SEO Desc: {seo_desc}")
        if issues:
            print(f"  ISSUES: {', '.join(issues)}")
        else:
            print(f"  OK - no issues found")
