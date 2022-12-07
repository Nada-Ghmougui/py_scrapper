from typing import Union

import uvicorn
from fastapi import FastAPI
from fb_scrapper import Facebook_scraper
import json
import pymongo

app = FastAPI()


@app.get('/page/{page_name}/{nbr_posts}')
def scrape_page(page_name: str, nbr_posts: int):
    page = page_name
    proxy_port = 10001
    posts_count = nbr_posts
    browser = "chrome"
    timeout = 600
    headless = True
    scraper = Facebook_scraper(page, posts_count, browser, timeout=timeout, headless=headless)
    json_data = scraper.scrap_to_json()
    js = json.loads(json_data)
    client = pymongo.MongoClient()
    db = client.task
    db.facebook_posts.insert_one(js)
    return "done"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
