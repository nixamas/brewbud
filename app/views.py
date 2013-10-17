# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

from app import app, lm, db, configuration
from app.models import BeerModel
from flask import url_for, redirect, render_template, flash, g, session
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from flask.ext.wtf import Form
from flask.globals import request
from forms import ExampleForm, LoginForm, BeerForm, BrewForm, BreweryForm
from models import User, BeerModel, BrewModel, BreweryModel
from werkzeug.utils import secure_filename
from wtforms.ext.appengine.db import model_form
from PIL import Image
import flask.globals
import os
from utils import getBreweryLinkForBeer, getImagesForBeerOrBrew, getStylesFromXML, \
    copyBeerModelDataToNewBeerModel, copyBrewModelDataToNewBrewModel

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new/')
@login_required
def new():
    form = ExampleForm()
    return render_template('new.html', form=form)

@app.route('/beers/', methods = ['GET', 'POST'])
def beers():
    beerModel = BeerModel(None)
    beers = beerModel.query.all()
    print("showing BEERS :: " + str(beers))
    return render_template('beers.html', beers=beers, getBreweryLinkForBeer=getBreweryLinkForBeer)

@app.route('/newbeer/')
def newbeer():
    form = BeerForm()
    form.beer_id.data = ""
    breweries = BreweryModel.query.all()
    return render_template('beer.html', form=form, breweries=breweries, beer_styles=getStylesFromXML())

@app.route('/savebeer/', methods = ['GET', 'POST'])
def savebeer():
    print("/savebeer/")
    form = BeerForm(request.form)
    print("/savebeer/")
    print(str(form))
    if not form.validate():
        print("Beer Form Data is invalid")
        flash("Beer data is invalid, A Name and Brewery is required!!")
        return redirect(url_for("newbeer", form=form))
    if form.beer_id.data == None or form.beer_id.data == "":
        print("Saving a new beer")
        print("views :: BeerForm -- " + str(form))
        print("beer_id :: " + str(form.beer_id.data))
        brewery_picked = BreweryModel.query.filter_by(brewery_id=form.beer_brewery.data).first()
        print("brewery picked --- >  " + str(brewery_picked) )
        #brewery_model = BreweryModel(brewery_picked)
        #brewery_model.brewery_name = form.beer_brewery.data
        print("brewery_model :: " + str(brewery_picked))
        db.session.add(brewery_picked)
        print("Brewery Saved")
        beer_model = BeerModel(form,brewery_picked)
        print("views :: BeerModel -- " + str(beer_model))
        db.session.add(beer_model)
        db.session.commit()
        print("****************************************************************")
        saveFileAndReturnFilePaths(request.files.getlist('beer_images[]'), beer_model.beer_id, "beer")
        print("****************************************************************")
        if request.method == 'POST' and form.validate():
            print("form validated!!!")
        return redirect(url_for('beer', beer_id=beer_model.beer_id))
    elif form.beer_id.data != None and form.beer_id.data != "":
        print("updating beer :: " + str(form.beer_id.data))
        beer_model = BeerModel(form)
        print("Updating beer model with :: " + str(beer_model))
        beer_found = BeerModel.query.filter_by(beer_id=form.beer_id.data).first()
        copyBeerModelDataToNewBeerModel(beer_model, beer_found)
        #beer_found.beer_name = beer_model.beer_name
        ##beer_found.brewery = beer_model.brewery
        #beer_found.beer_style = beer_model.beer_style
        #beer_found.beer_abv = beer_model.beer_abv
        #beer_found.beer_ibu = beer_model.beer_ibu
        #beer_found.beer_srm = beer_model.beer_srm
        #beer_found.beer_og = beer_model.beer_og
        #beer_found.beer_rating = beer_model.beer_rating
        db.session.commit()
        return redirect(url_for('beer', beer_id=form.beer_id.data))

@app.route('/beer/<int:beer_id>', methods = ['GET'])
def beer(beer_id=None):
    print("/beer/"+str(beer_id))
    beer_found = BeerModel.query.filter_by(beer_id=beer_id).first_or_404()
    form = BeerForm(obj=beer_found)
    form.beer_brewery.data = beer_found.brewery.brewery_name
    breweries = BreweryModel.query.all()
    imgs_list = getImagesForBeerOrBrew("beer",beer_id)
    print("showing these breweries ::: " + str(breweries))
    print("showing beer :: " + str(beer_id))
    print("printing beer id -- " + str(form.beer_id.data))
    return render_template('beer.html', form=form, breweries=breweries, images_list=imgs_list, beer_styles=getStylesFromXML())

@app.route('/deletebeer/<int:beer_id>', methods = ['GET','POST'])
def deletebeer(beer_id):
    print("/deletebeer/" + str(beer_id) )
    print("DELECTE BEER FORM ::: " + str(request.form))
    beer_found = BeerModel.query.filter_by(beer_id=beer_id).all()
    for beer in beer_found:
        db.session.delete(beer)
    db.session.commit()
    remaining_beers = BeerModel(None).query.all();
    return redirect(url_for('beers', beers=remaining_beers))
    

""" *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* """
@app.route('/brews/', methods = ['GET'])
def brews():
    brewModel = BrewModel(None)
    brews = BrewModel.query.all()
    print("showing BREWS :: " + str(brews))
    return render_template('brews.html', brews=brews)

@app.route('/newbrew/')
def newbrew():
    return render_template('brew.html', brewform=BrewForm(prefix="brew"), beerform=BeerForm(prefix="beer"), breweries=BreweryModel.query.all(), beer_styles=getStylesFromXML())

@app.route('/savebrew/', methods = ['GET', 'POST'])
def savebrew():
    print("/savebrew/")
    beer_form = BeerForm(request.form, prefix="beer")
    brew_form = BrewForm(request.form, prefix="brew")
    brewery_model = BreweryModel()
    brewery_model.brewery_name = beer_form.beer_brewery.data
    print("searching for brewery -- " + str(beer_form.beer_brewery.data))
    brewery_picked = BreweryModel.query.filter_by(brewery_name=beer_form.beer_brewery.data).first()
    print("brewery_model :: " + str(brewery_picked))
    beer_model = BeerModel(beer_form, brewery_picked)
    brew_model = BrewModel(beer_model, brew_form)
    print("beer model --- > " + str(beer_model))
    print("brew model --- > " + str(brew_model))
    print("brew_validate :: " + str(brew_form.validate()))
    print("beer_validate :: " + str(beer_form.validate()))
    if beer_form.beer_name == None or beer_form.beer_name == "":    #TODO : Probably need to change the logic here later
        print("Invalid data found in brew_form or beer_form)")
        flash("Brew data is invalid, A Name and Brewery is required!!")
        return redirect(url_for("newbrew", brewform=BrewForm(prefix="brew"), beerform=BeerForm(prefix="beer")))
    if brew_form.brew_id.data == None or brew_form.brew_id.data == "":
        print("Saving a new brew")
        print("brewery_model :: " + str(brewery_picked))
        db.session.add(beer_model)
        print("saved beer -- " + str(beer_model))
        db.session.add(brew_model)
        print("saved brew")
        db.session.commit()
        print("****************************************************************")
        saveFileAndReturnFilePaths(request.files.getlist('beer_images[]'), brew_model.brew_id, "brew")
        print("****************************************************************")
    elif brew_form.brew_id.data != None and brew_form.brew_id.data != "":
        print("updating brew :: " + str(brew_form.brew_id.data))
        #brew_model = BrewModel(brew_form)
        print("Updating brew model with :: " + str(brew_model))
        brew_found = BrewModel.query.filter_by(brew_id=brew_form.brew_id.data).first()
        brew_model.brew_id = brew_form.brew_id.data
        copyBeerModelDataToNewBeerModel(beer_model, brew_found.beer)
        copyBrewModelDataToNewBrewModel(brew_model, brew_found)
        #brew_found.brew_brewery = brew_model.brew_brewery
        #brew_found.brew_style = brew_model.brew_style
        #brew_found.brew_abv = brew_model.brew_abv
        #brew_found.brew_ibu = brew_model.brew_ibu
        #brew_found.brew_srm = brew_model.brew_srm
        #brew_found.brew_og = brew_model.brew_og
        ##brew_found.brew_rating = brew_model.brew_rating
        db.session.commit()
        
    return redirect(url_for('brew', brew_id=brew_model.brew_id))

@app.route('/brew/<int:brew_id>', methods = ['GET'])
def brew(brew_id):
    print("/brew/"+str(brew_id))
    brew_found = BrewModel.query.filter_by(brew_id=brew_id).first_or_404()
    print("found brew :: " + str(brew_found))
    print("found beer :: " + str(brew_found.beer))
    print("found brewery :: " + str(brew_found.beer.brewery))
    beer_form = BeerForm(obj=brew_found.beer)
    brew_form = BrewForm(obj=brew_found)
    beer_form.beer_brewery.data = brew_found.beer.brewery.brewery_name
    print("beer form :: " + str(beer_form))
    print("brew form :: " + str(brew_form))
    imgs_list = getImagesForBeerOrBrew("brew",brew_id)
    return render_template('brew.html', brewform=brew_form,beerform=beer_form, breweries=BreweryModel.query.all(), images_list=imgs_list, beer_styles=getStylesFromXML())

@app.route('/deletebrew/<int:brew_id>', methods = ['GET','POST'])
def deletebrew(brew_id):
    print("/deletebrew/" + str(brew_id))
    brew_found = BrewModel.query.filter_by(brew_id=brew_id).all()
    for brew in brew_found:
        db.session.delete(brew.beer)
        print("brew.beer was deleted")
        db.session.delete(brew)
        print("brew was deleted")
        db.session.commit()
    print("brew was deleted")
    remaining_brews = BrewModel.query.all()
    remaining_beers = BeerModel(None).query.all();
    #print("beer deleted :::    remaining beers -- " +str(remaining_beers))
    return redirect(url_for('beers', beers=remaining_beers))
    
""" *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* """
@app.route('/breweries', methods = ['GET'])
def breweries():
    print("showing /breweries")
    breweries = BreweryModel.query.all()
    print("showing Breweries :: " + str(breweries))
    return render_template('breweries.html', breweries=breweries)

@app.route('/newbrewery/')
def newbrewery():
    return render_template('brewery.html', form=BreweryForm())

@app.route('/savebrewery/', methods = ['GET', 'POST'])
def savebrewery():
    print("/savebrewery/")
    form = BreweryForm(request.form)
    if not form.validate():
        print("brewery Form Data is invalid")
        flash("Brewery data is invalid, A Name is required!!")
        return redirect(url_for("newbrewery", form=form))
    if form.brewery_id.data == None or form.brewery_id.data == "":
        print("Saving a new brewery")
        print("views :: breweryForm -- " + str(form))
        brewery_model = BreweryModel(form)
        print("brewery_model :: " + str(brewery_model))
        db.session.add(brewery_model)
        flash("Brewery Added")
        db.session.commit()
    elif form.brewery_id.data != None and form.brewery_id.data != "":
        print("updating beer :: " + str(form.brewery_id.data))
        brewery_model = BreweryModel(form)
        print("Updating beer model with :: " + str(brewery_model))
        brewery_found = BreweryModel.query.filter_by(brewery_id=form.brewery_id.data).first()
        brewery_found.brewery_name = brewery_model.brewery_name
        brewery_found.brewery_url = brewery_model.brewery_url
        brewery_found.brewery_information = brewery_model.brewery_information
        db.session.commit()
        flash("Save Successful")
        brewery_model.brewery_id = brewery_found.brewery_id
    return redirect(url_for('brewery', brewery_id=brewery_model.brewery_id))

@app.route('/brewery/<int:brewery_id>', methods = ['GET'])
def brewery(brewery_id=None):
    print("/brewery/"+str(brewery_id))
    brewery_found = BreweryModel.query.filter_by(brewery_id=brewery_id).first_or_404()
    form = BreweryForm(obj=brewery_found)
    print("showing brewery :: " + str(brewery_id))
    return render_template('brewery.html', form=form)

""" *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* """
@app.route('/save/', methods = ['GET','POST'])
@login_required
def save():
    form = ExampleForm()
    if form.validate_on_submit():
        print "salvando os dados:"
        print form.title.data
        print form.content.data
        print form.date.data
        flash('Dados salvos!')
    return render_template('new.html', form=form)

@app.route('/view/<id>/')
def view(id):
    return render_template('view.html')

# === User login methods ===

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    print("logging in...")
    if g.user is not None and g.user.is_authenticated():
        print("User is not authenticated!!!!")
        return redirect(url_for('index'))
    form = LoginForm()
    print("login form :: " + str(form))
    if form.validate_on_submit():
        print("Validated user!!!!")
        login_user(g.user)
    return redirect(url_for('index'))
#    return render_template('login.html', 
#       title = 'Sign In',
#        form = form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

# ====================




'''
    UTILITY FUNCTIONS
'''
def saveFileAndReturnFilePaths(imgs, beer_id, image_type):
    print("saving files :: " + str(imgs))
    imgFilenames = ""
    for myfile in imgs:
        print("this is what i found ::: " + str(myfile))
        if myfile and allowed_file(myfile.filename):
            filename = secure_filename(myfile.filename)
            imgFilenames = imgFilenames + "," + str(filename)
            print("image filename :: " + str(filename))
            print("making directory")
            if not os.path.exists( os.path.join(configuration.Config.UPLOAD_FOLDER, str(image_type), str(beer_id)) ):
                os.makedirs(os.path.join( configuration.Config.UPLOAD_FOLDER, str(image_type), str(beer_id)) )
            resize_image(myfile).save(os.path.join(configuration.Config.UPLOAD_FOLDER, str(image_type), str(beer_id), filename))
    imgFilenames = imgFilenames + ";"
    print("adding image filenames :: " + str(imgFilenames))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in configuration.Config.ALLOWED_EXTENSIONS

def resize_image(image):
    FINAL_IMG_WIDTH = 325   
    print("resizing image...")
    img = Image.open(image)  # @UndefinedVariable
    width, height = img.size
    print("original size :: width - " + str(width) + " :::: height - " + str(height) )
    wpercent = (FINAL_IMG_WIDTH / float(width))
    hsize = int((float(height) * float(wpercent)))
    img = img.resize((FINAL_IMG_WIDTH, hsize), Image.ANTIALIAS)  # @UndefinedVariable
    return img