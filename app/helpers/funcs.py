import csv
import io
import re

def extract_domain(url):
    pattern = r'https?:\/\/(?:www\.)?([^\/]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None


def get_urls_from_csv(file_stream):
    article_urls = []
    failed_article_urls = []

    # Read the file as a stream
    stream = io.StringIO(file_stream.stream.read().decode("UTF8"), newline=None)
    csvreader = csv.reader(stream)

    for index, row in enumerate(csvreader):
        try:
            article_urls.append(row[0])
        except UnicodeDecodeError:
            failed_article_urls.append(failed_article_urls)
            print(f"Error decoding row #{index + 1}: {row}")

    print(f"Total URL's: {len(article_urls) + len(failed_article_urls)}")
    print(f"# Successful Urls: {len(article_urls)}")
    print(f"# Failed Urls: {len(failed_article_urls)}")
    print(article_urls)
    return article_urls
