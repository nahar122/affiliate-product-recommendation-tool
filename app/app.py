from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from helpers.funcs import get_urls_from_csv
from main import process_articles
from scrapy.crawler import CrawlerProcess
from article_crawler.spiders.article_spider import ArticleSpider
import pathlib
import crochet
from threading import Thread, Event
import logging
crochet.setup()
load_dotenv()

USERNAME = 'admin'
PASSWORD = 'admin'
logging.basicConfig(level=logging.INFO)

# @crochet.run_in_reactor
def run_spider_with_urls(urls, form, outputfile, finished_event):
    settings = {
        'USER_AGENT': 'your_user_agent',
        'FEED_FORMAT': 'json',
        'FEED_URI': outputfile,
        # other settings
    }

    process = CrawlerProcess(settings)
    ArticleSpider.urls_to_scrape = urls
    # attribute_type = form.get("attributeType")
    # if attribute_type == "class":
    #     ArticleSpider.extract_by = "class"
    # elif attribute_type == "id":
    #     ArticleSpider.extract_by = "id"
    # ArticleSpider.title_value = form.get("title")
    # ArticleSpider.paragraph_value = form.get("paragraph")

    logging.info("Spider started")
    deferred = process.crawl(ArticleSpider)
    deferred.addBoth(lambda _: finished_event.set())
    return deferred
    # deferred = process.start(stop_after_crawl=True)
    # deferred.addBoth(lambda _: finished_event.set())
    # finished_event.set()

def create_app():
    app = Flask(__name__)
    CORS(app)
    # DB_HOST = os.environ.get("DB_HOST")
    # DB_NAME = os.environ.get("DB_NAME")
    # DB_USER = os.environ.get("DB_USER")
    # DB_PASS = os.environ.get("DB_PASS")
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
    app.secret_key = "my-secret-key"
    
    
    return app

app = create_app()

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
            output_path = current_dir / 'data/articles.json'
            
            # Run spider and add callback for process_articles
            finished_event = Event()

            Thread(target=run_spider_with_urls, args=(article_urls, request.form, output_path, finished_event)).start()

            def wait_and_process():
                finished_event.wait()
                logging.info("Event set, running process_articles")
                process_articles()

            Thread(target=wait_and_process).start()

            return "<h1>Upload successful</h1>"

    return render_template('upload.html')

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=80, debug=True)