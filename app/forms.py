# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

from flask.ext.wtf import Form, TextField, TextAreaField, DateTimeField, PasswordField, HiddenField
from flask.ext.wtf import Required

class ExampleForm(Form):
    title = TextField(u'Título', validators = [Required()])
    content = TextAreaField(u'Conteúdo')
    date = DateTimeField(u'Data', format='%d/%m/%Y %H:%M')
    #recaptcha = RecaptchaField(u'Recaptcha')

class LoginForm(Form):
    user = TextField(u'Usuário', validators = [Required()])
    password = PasswordField(u'Senha', validators = [Required()])

class BeerForm(Form):
    """" 
        Form for Beer 
    """
    beer_id = HiddenField(u'beer_id')
    beer_name = TextField(u'beer_name', validators = [Required()])
    beer_brewery = TextField(u'beer_brewery', validators = [Required()])
    beer_style = TextField(u'beer_style', validators = [])
    beer_abv = TextField(u'beer_abv', validators = [])
    beer_ibu = TextField(u'beer_ibu', validators = [])
    beer_srm = TextField(u'beer_srm', validators = [])
    beer_og = TextField(u'beer_og', validators = [])
    beer_rating = TextField(u'beer_rating', validators = [])
    #beer_brewery = FormField(u'beer_brewery', validators = [])
    def __str__(self):
        return "< " + str(self.beer_id) + ", " + str(self.beer_name) + ", " + str(self.beer_brewery) + " " +">"

class BrewForm(Form):
    """" 
        Form for Brews
        Brews are personal beer recipes 
    """
    brew_id = HiddenField(u'beer_id')
    #brew_name = TextField('brew_name', validators = [Required()])
    #brew_brew_date = DateTimeField('brew_brew_date', format='%d/%m/%Y %H:%M')
    brew_brew_date = TextField('brew_brew_date', validators = [])
    #brew_second_ferm_date = DateTimeField('brew_second_ferm_date', format='%d/%m/%Y %H:%M')
    brew_second_ferm_date = TextField('brew_second_ferm_date', validators = [])
    #brew_bottle_date = DateTimeField('brew_bottle_date', format='%d/%m/%Y %H:%M')
    brew_bottle_date = TextField('brew_bottle_date', validators = [])
    brew_volume = TextField('brew_volume', validators = [])
    brew_abv = TextField('brew_abv', validators = [])
    brew_ingredients = TextField('brew_ingredients', validators = [])
    brew_notes = TextField('brew_notes', validators = [])
    #brew_rating = TextField('brew_rating', validators = [])
    def __str__(self):
        return "< " + str(self.brew_id) + ", " + " >"

class BreweryForm(Form):
    brewery_id = HiddenField(u'brewery_id')
    brewery_name = TextField(u'brewery_name', validators = [Required()])
    brewery_url = TextField(u'brewery_url', validators = [])
    brewery_information = TextField(u'brewery_information', validators = [])
    def __str__(self):
        return "< " + str(self.brewery_id) + " , " + str(self.brewery_name) + " >"
    
    
    