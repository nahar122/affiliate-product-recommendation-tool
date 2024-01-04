import uuid
import json
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from helpers.funcs import get_urls_from_csv
from main import process_articles
from scrapy.crawler import CrawlerProcess
from article_crawler.spiders.article_spider import ArticleSpider
import pathlib
import os
from threading import Thread, Event
import logging
from db.models import DatabaseManager, URL
import crochet
crochet.setup()
load_dotenv()

USERNAME = 'admin'
PASSWORD = 'admin'
logging.basicConfig(level=logging.INFO)

# @crochet.run_in_reactor
def run_spider_with_urls(urls, outputfile, finished_event):
    settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'FEED_FORMAT': 'json',
        'FEED_URI': outputfile,
        # other settings
    }

    process = CrawlerProcess(settings)
    ArticleSpider.urls_to_scrape = urls
    logging.info("Spider started")
    deferred = process.crawl(ArticleSpider)
    deferred.addBoth(lambda _: finished_event.set())
    return deferred

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.secret_key = "$8AJ1MASnhas9KJl12n9Wis(@I)$*as"
    return app

app = create_app()

db_uri = f"mysql+pymysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('upload'))
        else:
            return render_template('login.html', error='Invalid Credentials. Please try again.')

    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        if file and file.filename.endswith('.csv'):
            article_urls = get_urls_from_csv(file)
            current_dir = pathlib.Path(__file__).parent
            unique_id = uuid.uuid4()
            output_path = current_dir / f'data/article_{unique_id}.json'  
            # Run spider and add callback for process_articles
            finished_event = Event()

            Thread(target=run_spider_with_urls, args=(article_urls, output_path, finished_event)).start()

            def wait_and_process():
                finished_event.wait()
                logging.info("Event set, running process_articles")
                process_articles(unique_id)
            
            Thread(target=wait_and_process).start()

            return "<h1>Upload successful</h1>"

    return render_template('upload.html')

@app.route('/process-article', methods=['POST'])
def process_single_article():
    unique_id = uuid.uuid4()
    current_dir = pathlib.Path(__file__).parent
    article_path = current_dir / f'data/article_{unique_id}.json'
    data = request.json
    if 'url' in data and 'title' in data and 'paragraph' in data:
        try:
            json.dump([request.json], open(article_path, "w", encoding="utf-8"))
            process_articles(unique_id)       
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": e})

    return jsonify({"success": False, "error": "Missing required data in request body."})




@app.route('/retrieve-url-data', methods=['POST'])
def retrieve_url_data():
    db_manager = DatabaseManager(db_uri=db_uri)
    data = request.get_json()
    url_to_find = data.get('url')

    # Query the database
    url_entry = db_manager.session.query(URL).filter_by(url=url_to_find).first()

    if url_entry:
        return jsonify({
            'url': url_entry.url,
            'article_title': url_entry.article_title,
            'initial_article_paragraph': url_entry.initial_article_paragraph,
            'injected_article_paragraph': url_entry.injected_article_paragraph
        })
    else:
        return jsonify({'message': 'URL not found'}), 404



#database routes
@app.route('/api/get-domains', methods=['GET'])
def get_all_domains():
    db_manager = DatabaseManager(db_uri=db_uri)
    try:
        domains = db_manager.get_all_domains()
        return jsonify([{'id': domain.id, 'domain': domain.domain} for domain in domains])
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)