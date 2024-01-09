from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session 
import logging
# Define the base class

Base = declarative_base()

class Domain(Base):
    __tablename__ = 'domains'
    id = Column(Integer, primary_key=True)
    domain = Column(String(255), unique=True, nullable=False)
    universal_passback_paragraph = Column(Text, nullable=False)

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

class ExcludedUrl(Base):
    __tablename__ = 'excluded_urls'
    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False, unique=True)
    domain_id = Column(Integer, ForeignKey('domains.id'), nullable=False)




logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    _instance = None

    def __new__(cls, db_uri=None):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            if db_uri is None:
                raise ValueError("Database URI must be provided")

            # Initialize the database engine
            cls._instance.engine = create_engine(db_uri)

            # Create all tables if they don't exist
            try:
                Base.metadata.create_all(cls._instance.engine)
                logging.info("All tables created or verified successfully.")
            except Exception as e:
                logging.error(f"An error occurred while creating tables: {e}")
                raise

            # Initialize the session
            cls._instance.session = cls.create_session(cls._instance.engine)
        return cls._instance

    @staticmethod
    def create_engine(db_uri):
        if db_uri is None:
            raise ValueError("Database URI must be provided")
        # Replace with your database connection details
        return create_engine(db_uri)

    @staticmethod
    def create_session(engine):
        # Assuming you are using SQLAlchemy
        Session = sessionmaker(bind=engine)
        return Session()

    def add_domain(self, domain_name, universal_passback_paragraph):
        try:
            existing_domain = self.session.query(Domain).filter_by(domain=domain_name).first()
            if existing_domain:
                logging.info(f"Domain '{domain_name}' already exists in the database.")
                return existing_domain
            else:
                new_domain = Domain(domain=domain_name, universal_passback_paragraph=universal_passback_paragraph)
                self.session.add(new_domain)
                self.session.commit()
                logging.info(f"New domain '{domain_name}' added to the database.")
                return new_domain
        except Exception as e:
            self.session.rollback()
            logging.error(f"An error occurred while adding domain '{domain_name}': {e}")
            raise
    def batch_add_excluded_url(self, excluded_url_list, domain_id):
        try:
            domain = self.session.query(Domain).filter_by(id=domain_id).first()
            if not domain:
                raise Exception(f"Domain with ID '{domain_id}' not found.")
            for url in excluded_url_list:
                excluded_url = ExcludedUrl(url=url, domain_id=domain.id)
                self.session.add(excluded_url)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logging.error(f"An error occurred while during batch add excluded URLs: {e}")
            raise


    def add_excluded_url(self, url, domain_id):
        try:
            domain = self.session.query(Domain).filter_by(id=domain_id).first()
            if not domain:
                raise Exception(f"Domain with ID '{domain_id}' not found.")
            excluded_url = ExcludedUrl(url=url, domain_id=domain.id)
            self.session.add(excluded_url)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logging.error(f"An error occurred while adding an excluded URL: {e}")
            raise

    def add_url(self, url, domain_id, article_title=None, initial_article_paragraph=None, injected_article_paragraph=None):
        try:
            new_url = URL(
                url=url,
                domain_id=domain_id,
                article_title=article_title,
                initial_article_paragraph=initial_article_paragraph,
                injected_article_paragraph=injected_article_paragraph
            )
            self.session.add(new_url)
            self.session.commit()
            logging.info(f"New URL '{url}' added to the database.")
            return new_url
        except Exception as e:
            self.session.rollback()
            logging.error(f"An error occurred while adding URL '{url}': {e}")
            raise
    
    def update_url(self, url_id, options):
        try:
            url = self.session.query(URL).filter_by(id=url_id).first()
            if not url:
                raise Exception(f"URL with ID '{url_id}' does not exist.")
            if options.get('article_title'):
                url.article_title = options.get('article_title')
            if options.get('initial_article_paragraph'):
                url.initial_article_paragraph = options.get('initial_article_paragraph')
            if options.get('injected_article_paragraph'):
                url.injected_article_paragraph = options.get('injected_article_paragraph')
            self.session.commit()
            logging.info(f"Finished updating URL with ID: {url_id}.")

        except Exception as e:
            self.session.rollback()
            logging.error(f"An error occurred: {e}. Rolling back.")
            raise
    
    def update_domain(self, domain_id, options):
        try:
            domain = self.session.query(Domain).filter_by(id=domain_id).first()
            if not domain:
                raise Exception(f"Domain with ID '{domain_id}' does not exist.")
            if options.get('universal_passback_paragraph'):
                domain.universal_passback_paragraph = options.get('universal_passback_paragraph')
            self.session.commit()
            logging.info(f"Finished updating URL with ID: {domain_id}.")

        except Exception as e:
            self.session.rollback()
            logging.error(f"An error occurred: {e}. Rolling back.")
            raise
    

    def batch_add_url(self, url_data_list):
        try:
            for data in url_data_list:
                existing_url = self.session.query(URL).filter_by(url=data.get('url')).first()
                if existing_url:
                    logging.info(f"URL '{data.get('url')}' already exists in the database, updating record.")
                    existing_url.initial_article_paragraph = data.get('initial_article_paragraph')
                    existing_url.article_title = data.get('article_title')
                    existing_url.injected_article_paragraph = data.get('injected_article_paragraph')
                else:
                    new_url = URL(
                        url=data.get('url'),
                        domain_id=data.get('domain_id'),
                        article_title=data.get('article_title', None),
                        initial_article_paragraph=data.get('initial_article_paragraph', None),
                        injected_article_paragraph=data.get('injected_article_paragraph', None)
                    )
                    self.session.add(new_url)
                    self.session.flush()  # Flush to assign an ID without committing
                    logging.info(f"URL '{data.get('url')}' added to the database.")

                    # Add products associated with the new URL
                    products = data.get("products")
                    if products:
                        for product in products:
                            new_amazon_product = AmazonProduct(
                                product_link=product['product_link'],
                                product_name=product['product_name'],
                                url_id=new_url.id
                            )
                            self.session.add(new_amazon_product)
                            logging.info(f"Amazon Product '{product['product_name']}' prepared for addition.")

            self.session.commit()
            logging.info("Batch URL addition and update completed.")
        except Exception as e:
            self.session.rollback()
            logging.error(f"An error occurred: {e}. Batch operation rolled back.")
            raise
    
    def get_all_domains(self):
        try:
            return self.session.query(Domain).all()
        except Exception as e:
            self.session.rollback()
            logging.error(f"An error occurred while retrieving domains: {e}")
            raise
    
    def get_all_urls_by_domain_id(self, domain_id):
        try:
            return self.session.query(URL).filter_by(domain_id=domain_id).all()
        except Exception as e:
            self.session.rollback()
            logging.error(f"An error occurred while retrieving URLs for domain_id={domain_id}: {e}")
            raise
    
    def is_url_excluded(self, url):
        try:
            # Query the ExcludedUrl table to check if the URL exists
            excluded_url = self.session.query(ExcludedUrl).filter_by(url=url).first()
            if excluded_url:
                logging.info(f"The URL '{url}' is excluded.")
                return excluded_url
            else:
                logging.info(f"The URL '{url}' is not excluded.")
                return None
        except Exception as e:
            self.session.rollback()
            logging.error(f"An error occurred while checking if the URL '{url}' is excluded: {e}")
            raise

    def close_session(self):
        try:
            self.session.close()
            logging.info("Database session closed.")
        except Exception as e:
            logging.error(f"An error occurred while closing the session: {e}")
            raise
