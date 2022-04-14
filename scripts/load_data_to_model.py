from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm.session import sessionmaker
from source.model import Base


set_logger()

load_dotenv()

DB_URI = os.environ['MODEL_DB_URI']
engine = create_engine(DB_URI)

Base.metadata.create_all(engine) # here we create all tables
Session = sessionmaker(bind=engine)
session = Session()
