#!/usr/bin/env python3
"""Scan all WordPress pages for Rank Math SEO scores."""

import requests
import json

WP_URL = "https://evidepo.com"
WP_USER = "admin"
WP_APP_PASS = "HQmY kKaQ kDY6 W91l v4G5 sHtA"

session = requests.Session()
session.auth = (WP_USER, WP_APP_PASS)

# Get all pages
pages = []
page = 1
while True:
    resp = session.get(f"{WP_URL}/wp-json/wp/v2/pages", params={
        "per_page": 100, "page": page, "status": "publish,draft,private"
    })
    if resp.status_code != 200:
        break
    data = resp.json()
    if not data:
        break
    pages.extend(data)
    total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
    if page >= total_pages:
        break
    page += 1

# Also get posts
for pt in ["posts"]:
    pg = 1
    while True:
        resp = session.get(f"{WP_URL}/wp-json/wp/v2/{pt}", params={
            "per_page": 100, "page": pg, "status": "publish,draft,private"
        })
        if resp.status_code != 200:
            break
        data = resp.json()
        if not data:
            break
        for d in data:
            d["_type"] = "post"
        pages.extend(data)
        tp = int(resp.headers.get("X-WP-TotalPages", 1))
        if pg >= tp:
            break
        pg += 1

print(f"{'ID':>4} | {'Score':>5} | {'Type':>8} | {'Status':>8} | {'Slug':<45} | Focus Keyword")
print("-" * 130)

for p in sorted(pages, key=lambda x: x["id"]):
    pid = p["id"]
    title = p["title"]["rendered"]
    slug = p["slug"]
    status = p["status"]
    ptype = p.get("_type", "page")

    meta_resp = session.get(f"{WP_URL}/wp-json/seo-machine/v1/post-meta/{pid}", params={"filter": "rank_math"})
    meta_data = meta_resp.json() if meta_resp.status_code == 200 else []

    score = "N/A"
    focus_kw = ""
    title_tag = ""
    desc = ""
    for m in meta_data:
        if m["key"] == "rank_math_seo_score":
            score = str(m["value"])
        if m["key"] == "rank_math_focus_keyword":
            focus_kw = str(m["value"])
        if m["key"] == "rank_math_title":
            title_tag = str(m["value"])
        if m["key"] == "rank_math_description":
            desc = str(m["value"])

    print(f"{pid:4d} | {score:>5s} | {ptype:>8s} | {status:>8s} | {slug:<45s} | {focus_kw[:50]}")
