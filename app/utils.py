import os
from app import db
import xml.etree.ElementTree as ET


def getBreweryLinkForBeer(beer):
    print("getBreweryLinkForBeerId")
    print(beer.brewery)
    return "TEST"
    

def getImagesForBeerOrBrew(type, type_id):
    img_path = "app/static/beerimages/" + str(type) + "/" + str(type_id) + "/"
    imgs_list = ""
    if os.path.exists( img_path ):
        imgs_list = os.listdir(img_path)
        for index, img in enumerate(imgs_list):
            imgs_list[index] = img_path.replace("app/static/", "") + img
            print("new image path :: " + str(img))
        print("image list --- " + str(imgs_list))
    print("getImagesForBeerOrBrew("+str(type)+", "+str(type_id)+") -- " + str(imgs_list))
    return imgs_list

def getStylesFromXML():
    style_xml_file = "app/static/beerstyles.xml"
    print(str(style_xml_file))
    if os.path.exists(style_xml_file):
        tree = ET.parse(style_xml_file)
        root = tree.getroot()
        idx = 0
        style_list = []
        for style in root:
            style_list.append(style[0].text)
            idx+=1
        return style_list
    else:
        return []
    
def copyBeerModelDataToNewBeerModel(orig_model, new_model):
    print("copyBeerModelDataToNewBeerModel");
    new_model.beer_name = orig_model.beer_name
    new_model.fk_brewery_id = orig_model.fk_brewery_id
    new_model.brewery = orig_model.brewery
    new_model.beer_style = orig_model.beer_style
    new_model.beer_abv = orig_model.beer_abv
    new_model.beer_ibu = orig_model.beer_ibu
    new_model.beer_srm = orig_model.beer_srm
    new_model.beer_og = orig_model.beer_og
    new_model.beer_rating = orig_model.beer_rating

def copyBrewModelDataToNewBrewModel(orig_model, new_model):
    print("copyBrewModelDataToNewBeerModel")
    #new_model.fk_beer_id = orig_model.fk_beer_id
    #new_model.beer = orig_model.beer
    new_model.brew_brew_date = orig_model.brew_brew_date
    new_model.brew_second_ferm_date = orig_model.brew_second_ferm_date
    new_model.brew_bottle_date = orig_model.brew_bottle_date
    new_model.brew_volume = orig_model.brew_volume
    new_model.brew_abv = orig_model.brew_abv
    new_model.brew_ingredients = orig_model.brew_ingredients
    new_model.brew_notes = orig_model.brew_notes

