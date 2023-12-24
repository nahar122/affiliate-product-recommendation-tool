from dotenv import load_dotenv
load_dotenv()

import os
import json
from openai_keyword_generator.main import generate_amazon_products, generate_paragraph
from amazon_product_retriever.main import get_amazon_product_links_by_keyword
import asyncio
import aiohttp
from datetime import datetime, timedelta
import pathlib
import logging
from datetime import datetime
from db.models import DatabaseManager
from helpers.funcs import extract_domain

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
MAX_TOKENS_PER_MINUTE = 50_000
MAX_REQUESTS_PER_MINUTE = 400
MAX_REQUESTS_PER_DAY = 10_000
BATCH_SIZE = 10 # Reduced batch size for better control
TOKEN_RESET_INTERVAL = 60  # Time in seconds for token reset

# async def get_new_domains(articles, session):
#     async with session.post("http://localhost:5000/filter-new-domains", json=articles) as response:
#         if response.status == 200:
#             new_articles = await response.json()
#             # print(new_articles)
#             return new_articles['data']
#         else:
#             print(f"Error fetching new domains: {response.json()}")
#             return []

async def process_article(session, article, db_manager):
    # Here, add your logic to process each URL through your APIs
    # For example:
    # 1. Send URL to OpenAI and get data
    # 2. Send data to Amazon API and get response
    # 3. Send Amazon response back to OpenAI
    # Return the final data to be batched for database upload
    article_with_product_names, tokens_used = await generate_amazon_products(article)
    current_dir = pathlib.Path(__file__).parent
    
    if not article_with_product_names:
        with open(current_dir / "data/failed_articles_.json", 'w') as outfile:
            failed_articles = json.load(outfile)
            failed_articles.append(article)
            json.dump(failed_articles, outfile)
        
        return None
    
    article_with_product_names = json.loads(article_with_product_names)

    # print(article)

    article_with_product_links = {'url': article['url'], "products": []}
    for product_name in article_with_product_names['products']:

        product = await get_amazon_product_links_by_keyword(product_name)
        if product:
            product['url'] = article['url']
            article_with_product_links['products'].append(product)
    
    article_with_product_links['article_title'] = article['title']
    article_with_product_links['initial_article_paragraph'] = article['paragraph']
    injected_paragraph_html, tokens_used_2 = await generate_paragraph(article_with_product_links)
    
    article_with_product_links['injected_article_paragraph'] = injected_paragraph_html
    domain = db_manager.add_domain(extract_domain(article_with_product_links['url']))
    article_with_product_links['domain_id'] = domain.id
    return article_with_product_links, tokens_used + tokens_used_2
    

async def main(filepath):
    with open(str(filepath), encoding='utf-8') as infile:
        articles = json.load(infile)
        batch_data = []
        total_requests_made_today = 0
        tokens_remaining = MAX_TOKENS_PER_MINUTE
        last_token_reset = datetime.now()
        db_uri = f"mysql+pymysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
        db_manager = DatabaseManager(db_uri=db_uri)

        async with aiohttp.ClientSession() as session:
            tasks = [process_article(session, article, db_manager) for article in articles]

            while tasks:
                if datetime.now() - last_token_reset >= timedelta(seconds=TOKEN_RESET_INTERVAL):
                    tokens_remaining = MAX_TOKENS_PER_MINUTE
                    last_token_reset = datetime.now()

                current_batch, tasks = tasks[:BATCH_SIZE], tasks[BATCH_SIZE:]
                try:
                    results = await asyncio.gather(*current_batch)

                    for data, tokens_used in results:
                        if data:
                            batch_data.append(data)
                            tokens_remaining -= tokens_used
                            total_requests_made_today += 1

                            if total_requests_made_today >= MAX_REQUESTS_PER_DAY:
                                print("Reached daily request limit.")
                                break

                    if batch_data:
                        db_manager.batch_add_url(batch_data)
                        batch_data.clear()

                    time_to_sleep = TOKEN_RESET_INTERVAL / MAX_REQUESTS_PER_MINUTE - (datetime.now() - last_token_reset).total_seconds()
                    time_to_sleep = max(0, time_to_sleep)
                    await asyncio.sleep(time_to_sleep)

                except aiohttp.ClientResponseError as e:
                    if e.status == 429:
                        retry_after = int(e.headers.get("Retry-After", 10))  # Default to 10 seconds if header is missing
                        print(f"Rate limit reached. Pausing for {retry_after} seconds.")
                        await asyncio.sleep(retry_after)


def process_articles(unique_id):
    start_time = datetime.now()
    logging.info("Script started")
    root_dir = pathlib.Path(__file__).parent
    
    crawled_articles_path = root_dir / f'data/article_{unique_id}.json'  # Replace with your CSV file path
    asyncio.run(main(crawled_articles_path))
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    logging.info(f"Script ended. Total elapsed time: {elapsed_time}")
    os.remove(crawled_articles_path)
if __name__ == "__main__":
    process_articles()
