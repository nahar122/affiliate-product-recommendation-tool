from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import relationship
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()


class Domain(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    url = db.Column(db.String(500), unique=True, nullable=False)
    title = db.Column(db.String(300), nullable=False)
    paragraph = db.Column(Text, nullable=False)
    injected_paragraph = db.Column(Text, nullable=True)

    # Establish a relationship to AffiliateLinks
    affiliate_links = relationship('AffiliateLinks', backref='domain', lazy=True)



class AffiliateLinks(db.Model):
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'), primary_key=True)
    link = db.Column(db.String(500), primary_key=True)
    name = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return '<AffiliateLinks %r>' % self.link
    

def create_app():
    app = Flask(__name__)
    CORS(app)
    DB_HOST = os.environ.get("DB_HOST")
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()
        # pass
    
    return app

app = create_app()



@app.route('/')
def index():
    return "<h1 id='test'>Hello World</h1>"

@app.route('/filter-new-domains', methods=['POST'])
def check_domains():
        data = request.json  # Expecting a list of objects

        # Validate input
        if not isinstance(data, list):
            return jsonify({'success': False, 'message': 'Invalid input, expecting a list of objects', "data": []}), 400

        # Filter out objects with URLs already in the database
        new_domains = [obj for obj in data if not Domain.query.filter_by(url=obj['url']).first()]

        return jsonify({"success": True, "message": "Successfuly retrieved domains currently not in database.", "data": new_domains}), 200

@app.route('/retrieve-injection-paragraph', methods=['POST'])
@cross_origin()
def retrieve_injection_paragraph():
    data = request.get_json()

    # Validate that URL is provided
    if 'url' not in data:
        return jsonify({'success': False, 'message': 'URL is required.', 'data': None}), 400

    # Fetch the domain by URL
    domain = Domain.query.filter_by(url=data['url']).first()

    # Check if domain exists
    if not domain:
        return jsonify({'success': False, 'message': 'Domain not found.', 'data': None}), 404

    # Return the injected_paragraph
    injected_paragraph = domain.injected_paragraph if hasattr(domain, 'injected_paragraph') else None

    return jsonify({'success': True, 'message': 'Paragraph retrieved successfully.', 'data': injected_paragraph})


@app.route('/add-domain', methods=['POST'])
def add_domain():
    domain_data = request.get_json()

    if not domain_data or 'url' not in domain_data or 'title' not in domain_data or 'paragraph' not in domain_data:
        return jsonify({'success': False, 'error': 'Missing data! url, title, and paragraph are required.'}), 400
    
    # Create a new Domain instance
    new_domain = Domain(url=domain_data['url'], title=domain_data['title'], paragraph=domain_data['paragraph'])

    # Add and commit to the database
    db.session.add(new_domain)
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': 'Domain added successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'An error occurred: {e}'}), 500
    
@app.route('/add-domains', methods=['POST'])
def create_domains():
    domains_data = request.get_json()

    # Check if data is a list
    if not isinstance(domains_data, list):
        return jsonify({'success': False, 'message': 'Input data should be a list of domains.'}), 400

    new_domains = []
    for data in domains_data:
        # Validate each domain data
        if 'url' not in data or 'title' not in data or 'paragraph' not in data:
            return jsonify({'success': False, 'message': 'Missing data in one or more domains. url, title, and paragraph are required.'}), 400

        new_domain = Domain(url=data['url'], title=data['title'], paragraph=data['paragraph'])
        new_domains.append(new_domain)

    db.session.add_all(new_domains)
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': 'Domains added successfully.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'An error occurred: {e}'}), 500

@app.route('/update-domain', methods=['POST'])
def update_domain():
    data = request.get_json()

    # Validate that URL is provided
    if 'url' not in data:
        return jsonify({'success': False, 'error': 'URL is required for updating a domain.'}), 400

    # Fetch the domain by URL
    domain = Domain.query.filter_by(url=data['url']).first()

    # Check if domain exists
    if not domain:
        return jsonify({'success': False, 'error': 'Domain not found.'}), 404

    # Update fields if they are in the request
    if 'title' in data:
        domain.title = data['title']
    if 'paragraph' in data:
        domain.paragraph = data['paragraph']
    if 'injected_paragraph' in data:
        domain.injected_paragraph = data['injected_paragraph']

    # Commit changes to the database
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': 'Domain updated successfully.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'An error occurred: {e}'}), 500

@app.route('/update-domains', methods=['POST'])
def update_domains():
    domains_data = request.get_json()

    # Check if data is a list
    if not isinstance(domains_data, list):
        return jsonify({'success': False, 'message': 'Input data should be a list of domains.'}), 400

    for data in domains_data:
        if 'url' not in data:
            return jsonify({'success': False, 'message': 'Each domain must include a URL.'}), 400

        domain = Domain.query.filter_by(url=data['url']).first()
        if domain:
            if 'title' in data:
                domain.title = data['title']
            if 'paragraph' in data:
                domain.paragraph = data['paragraph']
            if 'injected_paragraph' in data:
                domain.injected_paragraph = data['injected_paragraph']

    try:
        db.session.commit()
        return jsonify({'success': True, 'message': 'Domains updated successfully.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'An error occurred: {e}'}), 500

@app.route('/add-link', methods=['POST'])
def add_link():
    data = request.get_json()

    # Validate that both URL and link are provided
    if 'url' not in data or 'link' not in data:
        return jsonify({'success': False, 'message': 'Both URL and link are required.'}), 400

    # Fetch the domain by URL
    domain = Domain.query.filter_by(url=data['url']).first()

    # Check if domain exists
    if not domain:
        return jsonify({'success': False, 'message': 'Domain not found.'}), 404

    # Create a new AffiliateLinks instance
    new_affiliate_link = AffiliateLinks(domain_id=domain.id, link=data['link'])

    # Add and commit to the database
    db.session.add(new_affiliate_link)
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': 'Affiliate link added successfully.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'An error occurred: {e}'}), 500

@app.route('/add-links', methods=['POST'])
def add_links():
    data_list = request.get_json()

    # Validate that the input is a list
    if not isinstance(data_list, list):
        return jsonify({'success': False, 'message': 'Input data must be a list of objects.'}), 400

    for data in data_list:
        # Validate that each object includes 'url' and 'products'
        if 'url' not in data or 'products' not in data:
            return jsonify({'success': False, 'message': 'Each object must include a URL and products list.'}), 400

        # Validate that 'products' is a list
        if not isinstance(data['products'], list):
            return jsonify({'success': False, 'message': 'The products field should be a list.'}), 400

        # Fetch the domain by URL
        domain = Domain.query.filter_by(url=data['url']).first()

        # Check if domain exists
        if not domain:
            return jsonify({'success': False, 'message': f'Domain not found for URL: {data["url"]}'}), 404

        new_affiliate_links = []
        for product in data['products']:
            # Validate that each product has 'product_link' and 'product_name'
            if 'product_link' not in product or 'product_name' not in product:
                return jsonify({'success': False, 'message': 'Each product must include a product_link and a product_name.'}), 400

            # Create a new AffiliateLinks instance and add to the list
            new_affiliate_link = AffiliateLinks(domain_id=domain.id, link=product['product_link'], name=product['product_name'])
            new_affiliate_links.append(new_affiliate_link)

        # Add all new affiliate links to the database for this domain
        db.session.add_all(new_affiliate_links)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'An error occurred: {e}'}), 500

    return jsonify({'success': True, 'message': 'Affiliate links added successfully.'})
if __name__ == '__main__':
    app.run(debug=True)