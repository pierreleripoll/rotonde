
from sqlalchemy import *

engine = create_engine('sqlite:///base.db', echo=True)



metadata = MetaData()

valeurs = Table('valeurs',metadata,
            Column( 'val',Integer,primary_key=True))

metadata.create_all(engine)
connection=engine.connect()

connection.close()
