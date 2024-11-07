import os
from kivy.app import App
from kivy.properties import StringProperty
from kivy.event import EventDispatcher

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ViewModel(EventDispatcher):
   title = StringProperty("")
   description = StringProperty("")

   def __init__(self, title, description):
      self.title = title
      self.description = description

   def update(self, data_model):
      if data_model:
         self.title = data_model.db_title
         self.description = data_model.db_description

class DataModel(Base):
   __tablename__ = 'records'

   def __init__(self, db_title, db_description):
      self.db_title = db_title
      self.db_description = db_description

   id = Column(Integer, primary_key=True)
   db_title = Column(String, nullable=False)
   db_description = Column(String, nullable=False)

class MvvMExample(App):
   DATABASE = 'sqlite:///db.sqlite3'

   def __init__(self, **kwargs):
      super(MvvMExample, self).__init__(**kwargs)
      self.init_database()
      self.view_model = ViewModel("","")

   def init_database(self):
      engine = create_engine(self.DATABASE, echo=True)
      session_factory = sessionmaker(bind=engine)
      self.session = session_factory()

      if not os.path.exists('db.sqlite3'):
         Base.metadata.create_all(engine)

   def build(self):
      return self.root

   def read_values(self, instance):
      data_model = self.session.query(DataModel).filter_by(id=1).first()
      self.view_model.update(data_model)

   def write_values(self, instance):
      self.session.add(DataModel(db_title=self.view_model.title, db_description=self.view_model.description))
      self.session.commit()

if __name__ == '__main__':
    MvvMExample().run()
