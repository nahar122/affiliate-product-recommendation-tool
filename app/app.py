import uuid
import json
from flask import Flask, request, render_template, redirect, url_for, session, jsonify, abort
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
from db.models import DatabaseManager, URL, Domain
import crochet
from helpers.funcs import extract_domain
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

@app.route('/api/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'urls' not in request.files:
            return 'No file part', 400
        file = request.files['urls']
        if file.filename == '':
            return 'No selected file', 400
        if file and file.filename.endswith('.csv'):
            article_urls = get_urls_from_csv(file)
            domain_id = request.form.get("domain_id")
            current_dir = pathlib.Path(__file__).parent
            unique_id = uuid.uuid4()
            output_path = current_dir / f'data/article_{unique_id}.json'  
            # Run spider and add callback for process_articles
            finished_event = Event()

            Thread(target=run_spider_with_urls, args=(article_urls, output_path, finished_event)).start()

            def wait_and_process():
                finished_event.wait()
                logging.info("Event set, running process_articles")
                process_articles(unique_id, domain_id)
            
            Thread(target=wait_and_process).start()

            return jsonify({'success': True})

@app.route('/api/process-article', methods=['POST'])
def process_single_article():
    unique_id = uuid.uuid4()
    current_dir = pathlib.Path(__file__).parent
    article_path = current_dir / f'data/article_{unique_id}.json'
    data = request.json
    if 'url' in data and 'title' in data and 'paragraph' in data and "domain_id" in data:
        try:
            json.dump([request.json], open(article_path, "w", encoding="utf-8"))
            process_articles(unique_id, data.get("domain_id"))       
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": e})

    return jsonify({"success": False, "error": "Missing required data in request body."})

@app.route('/api/retrieve-url-data', methods=['POST'])
def retrieve_url_data():
    try:
        db_manager = DatabaseManager(db_uri=db_uri)
        data = request.get_json()
        url_to_find = data.get('url')

        # Query the database
        url_entry = db_manager.session.query(URL).filter_by(url=url_to_find).first()
        excluded_url = db_manager.get_excluded_url(url_to_find)
        db_manager.close_session()
        if url_entry:
            return jsonify({
                'url': url_entry.url,
                'article_title': url_entry.article_title,
                'initial_article_paragraph': url_entry.initial_article_paragraph,
                'injected_article_paragraph': url_entry.injected_article_paragraph,
                'excluded': False
            }), 200
        elif excluded_url:
            return jsonify({
                'url': excluded_url.url,
                'excluded': True
            }), 200
        else:
            extracted_domain = extract_domain(url_to_find)
            domain = db_manager.session.query(Domain).filter_by(domain=extracted_domain).first()
            if domain:
                return jsonify({
                    'url': None,
                    'article_title': None,
                    'initial_article_paragraph': None,
                    'injected_article_paragraph': domain.universal_passback_paragraph,
                    'excluded': False
                }), 200
            return jsonify({'message': 'URL and/or domain not found'}), 404
    except Exception as e:
        return jsonify({'sucess': False, 'error': str(e)}), 500


#database routes
@app.route('/api/get-domains', methods=['GET'])
def get_all_domains():
    db_manager = DatabaseManager(db_uri=db_uri)
    try:
        domains = db_manager.get_all_domains()
        db_manager.close_session()
        return jsonify([{'sucess': True, 'id': domain.id, 'domain': domain.domain, "universal_passback_paragraph": domain.universal_passback_paragraph} for domain in domains])
    except Exception as e:
        return jsonify({'sucess': False, 'error': str(e)}), 500

@app.route('/api/add-excluded-urls', methods=['POST'])
def upload_excluded_urls():
    data = request.json
    print(data)
    excluded_urls = data.get("excludedUrls")
    domain_id = data.get("domainId")
    print(f"excluded_urls: {excluded_urls}")

    if not domain_id:
        return jsonify({'success': False, 'error': "Key 'domain_id' missing from request."})
    if not excluded_urls:
        return jsonify({'success': False, 'error': "Key 'excludedUrls' missing from request."})

    try:
        db_manager = DatabaseManager(db_uri=db_uri)
        db_manager.batch_add_excluded_url(excluded_urls, domain_id)
        db_manager.close_session()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({'sucess': False, 'error': str(e)}), 500


@app.route('/api/add-domain', methods=['POST'])
def add_domain():

    db_manager = DatabaseManager(db_uri=db_uri)
    data = request.json
    if 'domain' not in data:
        return jsonify({"success": False, "error": "Missing 'domain' key from request."})
    if 'universal_passback_paragraph' not in data:
        return jsonify({"success": False, "error": "Missing 'universal_passback_paragraph' key from request."})
    
    try:
        new_domain_id = db_manager.add_domain(data['domain'], data['universal_passback_paragraph']).id
        db_manager.close_session()
        return jsonify({"success": True, 'domain_id': new_domain_id})
    except Exception as e:
        return jsonify({'sucess': False, 'error': str(e)}), 500
    
@app.route('/api/get-urls/<int:domain_id>', methods=['GET'])
def get_urls(domain_id):
    db_manager = DatabaseManager(db_uri=db_uri)
    try:
        urls = db_manager.get_all_urls_by_domain_id(domain_id)
        db_manager.close_session()
        if not urls:
            abort(404, description=f"No URLs found for domain ID {domain_id}")

        return jsonify([{
            'sucess': True,
            'id': url.id,
            'url': url.url,
            'article_title': url.article_title,
            'initial_article_paragraph': url.initial_article_paragraph,
            'injected_article_paragraph': url.injected_article_paragraph,
            'domain_id': url.domain_id
        } for url in urls])
    
    except Exception as e:
        return jsonify({'sucess': False, 'error': str(e)}), 500

@app.route('/api/edit-url/<int:url_id>', methods=['PATCH'])
def edit_url(url_id):
    db_manager = DatabaseManager(db_uri)
    data = request.json
    print(data)
    try:
        db_manager.update_url(url_id, data)
        db_manager.close_session()
        return {'success': True}
    except Exception as e:
        return jsonify({'sucess': False, 'error': str(e)}), 500

@app.route('/api/edit-domain/<int:domain_id>', methods=['PATCH'])
def edit_domain(domain_id):
    db_manager = DatabaseManager(db_uri)
    data = request.json
    print(data)
    try:
        db_manager.update_domain(domain_id, data)
        db_manager.close_session()
        return {'success': True}
    except Exception as e:
        return jsonify({'sucess': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)