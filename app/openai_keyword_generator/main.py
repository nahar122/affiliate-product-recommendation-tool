import json
from openai_keyword_generator.OpenAIInterface import OpenAIInterface
import asyncio

OPENAI_KEYWORD_GENERATOR_SYSTEM_MESSAGE = """
You are an Amazon Product Keyword Generation tool.

You will be given a JSON object which is an array of JSON objects in this schema:

{"url": "string", "title": "string", "first_paragraph": "string"}

You will generate the top 5 most relevant keywords for each object and return a list of objects in this JSON schema:

{"results": [{"url": "string", "keywords": []}]

Your response must include the same number of JSON objects as the input.
"""

OPENAI_PARAGRAPH_GENERATOR_SYSTEM_MESSAGE = """
You are an intelligent paragraph generator for articles.

In JSON format, you will receive the title and a paragraph of the article as well as an array of several amazon affiliate links in this schema:

{"title": "", "paragraph": "", "products": [{"product_link": "", "product_name": ""}]}

Based on the title, paragraph, and products, you will choose the products that are relevant to the article based on their "product_name" key.

Then, you will reconstruct the paragraph to include the chosen products in a way that makes sense and is relevant to the article.

Your response must be this adjusted paragraph encolsed by a <p> and </p> tags.
"""

OPENAI_MODEL = "gpt-3.5-turbo-1106"
openai_obj = OpenAIInterface(OPENAI_MODEL)

def process_chunk(chunk, system_message):
    processed_chunk = openai_obj.start_chat(system_message, json.dumps(chunk))
    if processed_chunk is not None:
        processed_data = json.loads(processed_chunk)
        processed_urls = {item['url'] for item in processed_data["results"]}
        input_urls = {item['url'] for item in chunk}
        unprocessed_urls = input_urls - processed_urls
        return processed_chunk, [item for item in chunk if item['url'] in unprocessed_urls]
    else:
        return None, chunk

def generate_keywords():

    unprocessed_items = []

    with open("./articles.json", 'r', encoding='utf-8') as infile, open("articles_with_keywords.json", 'w') as outfile:
        data = json.load(infile)
        chunk_size = 10

        outfile.write('[')
        first_item = True
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            processed_chunk, unprocessed = process_chunk(chunk, OPENAI_KEYWORD_GENERATOR_SYSTEM_MESSAGE)

            if processed_chunk:
                if not first_item:
                    outfile.write(',')
                else:
                    first_item = False
                outfile.write(processed_chunk)
            unprocessed_items.extend(unprocessed)
            print(f"Amount of unprocessed articles: {len(unprocessed_items)}")

        # Retry unprocessed items
        retries = 3
        while unprocessed_items and retries > 0:
            print(f"Attempting to process previously failed articles...")
            new_unprocessed_items = []
            for i in range(0, len(unprocessed_items), chunk_size):
                chunk = unprocessed_items[i:i + chunk_size]
                processed_chunk, unprocessed = process_chunk(chunk)

                if processed_chunk:
                    outfile.write(',' if not first_item else '')
                    first_item = False
                    outfile.write(processed_chunk)
                new_unprocessed_items.extend(unprocessed)

            unprocessed_items = new_unprocessed_items
            print(f"Amount of unprocessed articles: {len(unprocessed_items)}")

            retries -= 1

        outfile.write(']')

        # Write unprocessed items to a file
        if unprocessed_items:
            print("Failed to process all articles.")
            print(f"Amount of failed articles: {len(unprocessed_items)}")
            with open("unprocessed_articles.json", 'w', encoding='utf-8') as unprocessed_file:
                json.dump(unprocessed_items, unprocessed_file, indent=4)


async def generate_amazon_products(article):
    MESSAGE = """
You are an Amazon Product Generation tool.

You will be given a JSON object in this schema:

{"url": "string", "title": "string", "first_paragraph": "string"}

You will generate an array of the names of the top 5 most relevant amazon products and put them in the JSON key "products" under this schema:

{"url": "string", "products": []}

Your response must include the same number of JSON objects as the input.
"""
    response = await openai_obj.start_chat(MESSAGE, json.dumps(article), True)
    # print(response)
    if response:
        return (response['content'], response['tokens_used'])
    
    return None, None

async def generate_paragraph(article_with_affiliate_links):
    response = await openai_obj.start_chat(OPENAI_PARAGRAPH_GENERATOR_SYSTEM_MESSAGE, json.dumps(article_with_affiliate_links))
    
    if response:
        return (response['content'], response['tokens_used'])
    
    return None, None

