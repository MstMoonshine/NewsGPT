import openai
import os

openai.api_base = os.getenv("OPENAI_API_BASE")
openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt_summarize_webpage(content):
    if not content:
        return None
    system_prompt = "You a an assistant who helps me read the news."
    prompt = "The following contents are (a part of) a webpage. Please summarize it in within 150 words. If the contents are not human-readable texts, describe what kind of content it is.\n" + content
    messages = [{"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}]
    try:
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
        )
    except Exception as E:
        print(E)
        response = None
    return response

def gpt_summarize_comments(comments):
    if len(comments) == 0:
        return None
    system_prompt = "You a an assistant who helps me read the comments on Hacker News."
    prompt = "The following is a list of comments from Hacker News. Categorize the comments and summarize the main point of each category. Less than 50 words for each category. List the categories as bullet points in markdown format.\n"
    for (i, comment) in enumerate(comments):
        prompt += f"Comment {i}: {comment}\n"
    messages = [{"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}]
    try:
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
        )
    except Exception as E:
        print(E)
        response = None
    return response
