import os
from kivy.app import App
from kivy.event import EventDispatcher
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class CocktailDataModel(Base):
    __tablename__ = 'cocktails'

    def __init__(self, name):
      self.name = name

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ingredients = relationship("IngredientDataModel", back_populates="cocktail")

class IngredientDataModel(Base):
    __tablename__ = 'ingredients'

    def __init__(self, name, quantity, cocktail_id):
      self.name = name
      self.quantity = quantity
      self.cocktail_id = cocktail_id

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    cocktail_id = Column(Integer, ForeignKey('cocktails.id'))
    cocktail = relationship("CocktailDataModel", back_populates="ingredients")

class CocktailDatabase():
    def __init__(self, database):
        self.engine = create_engine(database, echo=True)
        self.session_factory = sessionmaker(bind=self.engine)
        self.session = self.session_factory()

        if not os.path.exists('cocktails.sqlite3'):
            Base.metadata.create_all(self.engine)
            self.create_example_data()

    def get_cocktails(self):
        cocktail_data = self.session.query(CocktailDataModel).all()
        return [x.name for x in cocktail_data]

    def get_ingredients(self, cocktail_name):
        cocktail_id = self.session.query(CocktailDataModel).filter_by(name=cocktail_name).first().id
        ingredient_data = self.session.query(IngredientDataModel).filter_by(cocktail_id=cocktail_id).all()
        ingredients = [{'name': x.name, 'quantity': x.quantity} for x in ingredient_data]
        print(ingredients)
        return ingredients
    
    def create_example_data(self):
        margarita = CocktailDataModel("Margarita")
        self.session.add(margarita)
        self.session.commit()

        margarita_ingredients = [
            IngredientDataModel("Tequila", "2 oz", margarita.id),
            IngredientDataModel("Lime Juice", "1 oz", margarita.id),
            IngredientDataModel("Cointreau", "1 oz", margarita.id)
        ]

        for ingredient in margarita_ingredients:
            self.session.add(ingredient)
        
        self.session.commit()

        martini = CocktailDataModel("Martini")
        self.session.add(martini)
        self.session.commit()

        martini_ingredients = [
            IngredientDataModel("Gin", "2 oz", martini.id),
            IngredientDataModel("Dry Vermouth", "1 oz", martini.id)
        ]

        for ingredient in martini_ingredients:
            self.session.add(ingredient)
        
        self.session.commit()

        mojito = CocktailDataModel("Mojito")
        self.session.add(mojito)
        self.session.commit()

        mojito_ingredients = [
            IngredientDataModel("White Rum", "2 oz", mojito.id),
            IngredientDataModel("Lime Juice", "1 oz", mojito.id),
            IngredientDataModel("Mint Leaves", "6", mojito.id),
            IngredientDataModel("Simple Syrup", "1 oz", mojito.id),
            IngredientDataModel("Club Soda", "1 oz", mojito.id)
        ]

        for ingredient in mojito_ingredients:
            self.session.add(ingredient)
        
        self.session.commit()

class ViewModel(EventDispatcher):
    def __init__(self, cocktail_database):
        self.cocktails = cocktail_database.get_cocktails()
        self.ingredients = [{'name': 'Select a cocktail', 'quantity': ''}]

    ingredients = ListProperty([])

class CustomItem(BoxLayout):
    name = StringProperty("")
    quantity = StringProperty("")

class CocktailApp(App):
    DATABASE = 'sqlite:///cocktails.sqlite3'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database = CocktailDatabase(self.DATABASE)
        self.view_model = ViewModel(self.database)

    def build(self):
        return self.root
    
    def selection_changed(self, value):
        self.view_model.ingredients = self.database.get_ingredients(value)


if __name__ == '__main__':
    CocktailApp().run()