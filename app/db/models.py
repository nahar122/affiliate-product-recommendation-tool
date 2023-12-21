from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session 
import logging
# Define the base class

Base = declarative_base()

class Domain(Base):
    __tablename__ = 'domains'
    id = Column(Integer, primary_key=True)
    domain = Column(String(255), nullable=False)

class URL(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False, unique=True)
    article_title = Column(String(255))
    initial_article_paragraph = Column(Text)
    injected_article_paragraph = Column(Text)
    domain_id = Column(Integer, ForeignKey('domains.id'), nullable=False)

class AmazonProduct(Base):
    __tablename__ = 'amazon_products'
    id = Column(Integer, primary_key=True)
    product_link = Column(String(255), nullable=False)
    product_name = Column(String(500), nullable=False)
    url_id = Column(Integer, ForeignKey('urls.id'), nullable=False)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        self.db_session = scoped_session(sessionmaker(bind=self.engine))
        Base.metadata.create_all(self.engine)
        logging.info(f"Database connection established with {db_uri}")

    def add_domain(self, domain_name):
        existing_domain = self.db_session.query(Domain).filter_by(domain=domain_name).first()
        if existing_domain:
            logging.info(f"Domain '{domain_name}' already exists in the database.")
            return existing_domain
        else:
            new_domain = Domain(domain=domain_name)
            self.db_session.add(new_domain)
            self.db_session.commit()
            logging.info(f"New domain '{domain_name}' added to the database.")
            return new_domain

    def add_url(self, url, domain_id, article_title=None, initial_article_paragraph=None, injected_article_paragraph=None):
        new_url = URL(
            url=url,
            domain_id=domain_id,
            article_title=article_title,
            initial_article_paragraph=initial_article_paragraph,
            injected_article_paragraph=injected_article_paragraph
        )
        self.db_session.add(new_url)
        self.db_session.commit()
        logging.info(f"New URL '{url}' added to the database.")
        return new_url

    def batch_add_url(self, url_data_list):
        try:
            for data in url_data_list:
                existing_url = self.db_session.query(URL).filter_by(url=data.get('url')).first()
                if existing_url:
                    logging.info(f"URL '{data.get('url')}' already exists in the database.")
                    continue

                new_url = URL(
                    url=data.get('url'),
                    domain_id=data.get('domain_id'),
                    article_title=data.get('article_title', None),
                    initial_article_paragraph=data.get('initial_article_paragraph', None),
                    injected_article_paragraph=data.get('injected_article_paragraph', None)
                )
                self.db_session.add(new_url)
                self.db_session.flush()  # Flush to assign an ID without committing

                logging.info(f"URL '{data.get('url')}' added to the database.")

                products = data.get("products")
                if products:
                    for product in products:
                        new_amazon_product = AmazonProduct(
                            product_link=product['product_link'],
                            product_name=product['product_name'],
                            url_id=new_url.id
                        )
                        self.db_session.add(new_amazon_product)
                        logging.info(f"Amazon Product '{product['product_name']}' prepared for addition.")


            self.db_session.commit()
            logging.info("Batch URL addition completed.")
        except Exception as e:
            self.db_session.rollback()
            logging.error(f"An error occurred: {e}. Batch operation rolled back.")
            raise

    def close_session(self):
        self.db_session.remove()
        logging.info("Database session closed.")
