from sqlalchemy import create_engine
from models.base import Base
from sqlalchemy.orm import sessionmaker
engine = create_engine('mysql+mysqlconnector://root:root@localhost:8889/db_inventaris')

Session=sessionmaker(bind=engine)
session=Session()
