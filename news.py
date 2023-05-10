from urllib.request import urlopen, Request
import json
from pprint import pprint
from bs4 import BeautifulSoup
import datetime
from gpt import *

def get_top_stories(num=10):
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json[:num]

def get_item_content(item_id):
    url = "https://hacker-news.firebaseio.com/v0/item/%d.json" % item_id
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json

def get_story_comments(story):
    comments = []
    kids = story.get('kids')
    if not kids:
        return comments
    for kid in kids:
        kid_data = get_item_content(kid)
        if kid_data.get('dead'):
            continue
        html_text = kid_data.get('text')
        if not html_text:
            continue
        soup = BeautifulSoup(html_text, 'html.parser')
        text = soup.get_text("\n")
        comments += [text]
    return comments

def get_story_webpage_content(story_url, char_limit=10000):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
    }
    req = Request(url, headers)

    try:
        response = urlopen(req)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(' ', strip=True)[:char_limit]
        return text
    except:
        print(f"Error opening the URL(story_id={id}, url={url})")
        return None

# main

if __name__ == '__main__':
    # get top stories
    stories = get_top_stories(30)

    # get webpage contents and comments of the stories
    for id in stories:
        story = get_item_content(id)

        author = story.get('by')
        score = story.get('score')
        title = story.get('title')
        url = story.get('url')
        unix_time = story.get('time')
        time = datetime.datetime.fromtimestamp(unix_time)

        web_content = get_story_webpage_content(url)
        comments = get_story_comments(story)

        gpt_response = gpt_summarize_webpage(web_content)
        comment_gpt_response = gpt_summarize_comments(comments)

        print(f"## Title: {title}")
        print(f"By: {author}")
        print(f"Date: {time}")
        print(f"URL: {url}")
        print(f"HN Score: {score}")
        print("\nGPT Summary:\n")
        if gpt_response:
            print(gpt_response["choices"][0]["message"]["content"])
        else:
            print("\nError\n")
        print("\nComments Summary:\n")
        if comment_gpt_response:
            print(comment_gpt_response["choices"][0]["message"]["content"])
        else:
            print("\nError\n")
        print("---" * 3)

