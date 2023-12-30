import json
import os
# from exceptions.exceptions import MissingEnvironmentVariable
from pathlib import Path
import aiohttp
import asyncio
import os
import time

last_request_time = None
requests_this_second = 0
REQUESTS_PER_SECOND_LIMIT = 10

async def get_amazon_product_links_by_keyword(keywords: str = ""):
    global last_request_time, requests_this_second

    url = "https://amazon-data.p.rapidapi.com/search.php"
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
    RAPIDAPI_HOST = os.environ.get("RAPIDAPI_HOST")

    querystring = {"keyword": keywords}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    current_time = time.time()

    # Throttle requests to adhere to rate limit
    if last_request_time and current_time - last_request_time < 1:
        requests_this_second += 1
        if requests_this_second >= REQUESTS_PER_SECOND_LIMIT:
            await asyncio.sleep(1 - (current_time - last_request_time))
            requests_this_second = 0
    else:
        requests_this_second = 1

    last_request_time = time.time()

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=querystring) as response:
                response.raise_for_status()
                try:
                    data = await response.json()
                except ValueError as e:
                    print(f"Invalid JSON in response: {e}")
                    return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None

    if len(data) > 0:
        return {"product_link": f"https://www.amazon.com/dp/{data[0]['asin']}?&_encoding=UTF8&tag=synth0f-20", "product_name": data[0]['asin_name']}

    return None

def retrieve_amazon_products():

    script_dir = Path(__file__).parent.resolve()
    data_dir = script_dir.parent / 'data'
    infile_path = data_dir / "articles_with_keywords.json"
    outfile_path = data_dir / "articles_with_products.json"
    failed_path = data_dir / "failed_articles_with_keywords.json"

    articles_with_products = []
    failed_articles = []
    with open(infile_path, "r") as infile, \
        open(outfile_path, "w") as outfile, \
        open(failed_path, "w") as failed_articles_with_keywords:

        articles_with_keywords = json.load(infile)
        for index, result in enumerate(articles_with_keywords):
            articles = result['results']
            print(f"Processing result # {index + 1}/{len(articles_with_keywords)}")
            for article in articles:

                if len(article['keywords']) == 0:
                    print(f"Failed to get products for article: {article['url']}")
                    failed_articles.append({'url': article['url'], "keywords": article['keywords']})
                    continue
                
                amount_of_keywords = 3
                products = get_amazon_product_links_by_keyword(",".join(article['keywords'][:amount_of_keywords])) 
                while len(products) < 3 and amount_of_keywords >= 0:
                    print("Could not find product with current keywords. Broadening keyword list.")
                    amount_of_keywords -= 1
                    products = get_amazon_product_links_by_keyword(",".join(article['keywords'][:amount_of_keywords]))

                print(f"Keywords: {article['keywords'][:amount_of_keywords]} \n Products: {products}")
                if(len(products) == 0):
                    print(f"Failed to get products for article: {article['url']}")
                    failed_articles.append({'url': article['url'], "keywords": article['keywords']})
                    continue

                articles_with_products.append({"url": article['url'], "product_links": products})

        json.dump(articles_with_products, outfile)
        json.dump(failed_articles, failed_articles_with_keywords)


if __name__ == "__main__":
    retrieve_amazon_products()