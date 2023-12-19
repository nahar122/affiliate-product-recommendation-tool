import csv
import unicodedata



def remove_special_characters(input_str):
    normalized_str = unicodedata.normalize('NFKD', input_str)
    ascii_str = normalized_str.encode('ASCII', 'ignore')
    return ascii_str.decode('ASCII')


def load_article_titles_from_csv(csv_path):
    article_titles = []
    failed_article_titles = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for index, row in enumerate(csvreader):
            try:
                title = row[0]
                if title.endswith(" - Linux Windows and android Tutorials"):
                    title = remove_special_characters(title[:-len(" - Linux Windows and android Tutorials")])
                    article_titles.append(title)
                else:
                    failed_article_titles.append(failed_article_titles)
            except UnicodeDecodeError:
                print(f"Error decoding row #{index + 1}: {row}")

    print(f"Number of failed articles: {len(failed_article_titles)}")

    return article_titles

def convert_article_titles_to_url(article_titles):
    article_titles_copy = article_titles.copy()
    for index, title in enumerate(article_titles_copy):
        title = "https://osradar.com/" + title.lower().replace(" ", "-")
        article_titles_copy[index] = title

    return article_titles_copy

def get_urls_from_csv(csv_path):

    article_urls = []
    failed_article_urls = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for index, row in enumerate(csvreader):
            try:
                article_urls.append(row[0])
            except UnicodeDecodeError:
                failed_article_urls.append(failed_article_urls)
                print(f"Error decoding row #{index + 1}: {row}")
    
    print(f"Total URL's: {len(article_urls) + len(failed_article_urls)}")
    print(f"# Successful Urls: {len(article_urls)}")
    print(f"# Failed Urls: {len(article_urls)}")
    print(article_urls)
    return article_urls
