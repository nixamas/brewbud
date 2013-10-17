# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

from app import db

class ModelExample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime)

class BeerModel(db.Model):
    __tablename__ = 'beers'
    beer_id = db.Column(db.Integer, primary_key=True)
    beer_name = db.Column(db.Text)
    #beer_brewery = db.Column(db.Text, unique = True)
    fk_brewery_id = db.Column(db.Integer, db.ForeignKey('breweries.brewery_id'))
    brewery = db.relationship('BreweryModel', backref=db.backref('breweries',lazy='dynamic'))
    beer_style = db.Column(db.Text)
    beer_abv = db.Column(db.Text)
    beer_ibu = db.Column(db.Text)
    beer_srm = db.Column(db.Text)
    beer_og = db.Column(db.Text)
    beer_rating = db.Column(db.Text)
    def __init__(self,form=None,brewery_mod=None):
        if form != None:
            print("BeerModel :: BeerForm -- " + str(form))
            self.beer_name = form.beer_name.data
            #self.beer_brewery = form.beer_brewery.data
            self.brewery = brewery_mod
            self.beer_style = form.beer_style.data
            self.beer_abv = form.beer_abv.data
            self.beer_ibu = form.beer_ibu.data
            self.beer_srm = form.beer_srm.data
            self.beer_og = form.beer_og.data
            self.beer_rating = form.beer_rating.data
    
    def __str__(self):
        return "<" + str(self.beer_id) + ", " + str(self.beer_name) + ", " + str(self.brewery) + ", " +">"

class BrewModel(db.Model):
    __tablename__ = 'brews'
    brew_id = db.Column(db.Integer, primary_key=True)
    fk_beer_id = db.Column(db.Integer, db.ForeignKey('beers.beer_id'))
    beer = db.relationship('BeerModel', backref=db.backref('brews',lazy='dynamic'))
    #brew_name = db.Column(db.Text)
    #brew_brew_date = db.Column(db.DateTime)
    brew_brew_date = db.Column(db.Text)
    #brew_second_ferm_date = db.Column(db.DateTime)
    brew_second_ferm_date = db.Column(db.Text)
    #brew_bottle_date = db.Column(db.DateTime)
    brew_bottle_date = db.Column(db.Text)
    brew_volume = db.Column(db.Text)
    brew_abv = db.Column(db.Text)
    brew_ingredients = db.Column(db.Text)
    brew_notes = db.Column(db.Text)
    #brew_rating = db.Column(db.Text)
    def __init__(self,beer_mod=None,form=None):
        if form != None and beer_mod != None:
            self.beer = beer_mod
            #self.brew_name = form.brew_name.data
            self.brew_brew_date = form.brew_brew_date.data
            self.brew_second_ferm_date = form.brew_second_ferm_date.data 
            self.brew_bottle_date = form.brew_bottle_date.data 
            self.brew_volume = form.brew_volume.data
            self.brew_abv = form.brew_abv.data
            self.brew_ingredients = form.brew_ingredients.data
            self.brew_notes = form.brew_notes.data
            #self.brew_rating = form.brew_rating.data
    
class BreweryModel(db.Model):
    __tablename__ = 'breweries'
    brewery_id = db.Column(db.Integer, primary_key=True)
    brewery_name = db.Column(db.Text)
    brewery_url = db.Column(db.Text)
    brewery_information = db.Column(db.Text)
    def __init__(self, form=None):
        if form != None:
            self.brewery_name = form.brewery_name.data
            self.brewery_url = form.brewery_url.data
            self.brewery_information = form.brewery_information.data
    def __str__(self):
        return "< " +str(self.brewery_id) + ", " + str(self.brewery_name) + "> "
    
class GravityReadingModel(db.Model):
    __tablename__ = 'gravityreadings'
    gravity_reading_id = db.Column(db.Integer, primary_key=True)
    fk_brew_id = db.Column(db.Integer, db.ForeignKey('brews.brew_id'))
    gravity_reading_date = db.Column(db.DateTime)
    gravity_reading_value = db.Column(db.Text)

class ReadingModels(db.Model):
    __tablename__ = 'readings'
    reading_id = db.Column(db.Integer, primary_key=True)
    fk_brew_id = db.Column(db.Integer, db.ForeignKey('brews.brew_id'))
    reading_time = db.Column(db.DateTime)
    reading_brew_temp = db.Column(db.Text)
    reading_amb_temp = db.Column(db.Text)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(500))
    name = db.Column(db.String(500))
    email = db.Column(db.String(120), unique = True)
    # posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)
