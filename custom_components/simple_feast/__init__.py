import requests
import json
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "simple_feast"
# meals.concepts[1].mealPlans[0].mealPlanVariations[0].box.meals[0].websiteTitle


def getGlasses(arr):
    return getConcept(arr, "GLASS")

def getFeasts(arr):
    return getConcept(arr, "MISE_EN_PLACE")

def getConcept(arr, which):
    return getKey(arr, "concept", which)

def getKey(arr, key, val):
    for row in arr:
        if row[key] == val:
            return row

def getGreenFeast(arr):
    return getKey(arr, "title", "Green Feast")

def getFamilyFeast(arr):
    return getKey(arr, "title", "Family Feast")

def getPlanVariationVegetarian(arr, persons):
    for row in arr:
        if row["diet"] == "VEGETARIAN" and row["people"] == persons:
            return row

def getPlanVariationVegetarian2persons(arr):
    return getPlanVariationVegetarian(arr, 2)

def getPlanVariationVegetarian4persons(arr):
    return getPlanVariationVegetarian(arr, 4)

def getPlanVariationVegan(arr, persons):
    for row in arr:
        if row["diet"] == "VEGAN" and row["people"] == persons:
            return row

def getPlanVariationVegan2persons(arr):
    return getPlanVariationVegan(arr, 2)

def getPlanVariationVegan4persons(arr):
    return getPlanVariationVegan(arr, 4)


CONF_FEAST = "feast"
CONF_VARIATION = "variation"
CONF_PERSONS = "persons"

# Validation of the user's configuration
# CONFIG_SCHEMA = vol.Schema({
#     DOMAIN: vol.Schema({
#         vol.Optional(CONF_FEAST, default='Green Feast'): cv.string,
#         vol.Optional(CONF_VARIATION, default='VEGETARIAN'): cv.string,
#         vol.Optional(CONF_PERSONS, default='2'): cv.string,
#     })
# })
CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_FEAST, default='Green Feast'): vol.In(['Green Feast', 'Family Feast']),
        vol.Optional(CONF_VARIATION, default='VEGETARIAN'): vol.In(['VEGETARIAN', 'VEGAN']),
        vol.Optional(CONF_PERSONS, default=2): vol.In([2, 4]),
    })
}, extra=vol.ALLOW_EXTRA)



def setup(hass, config):
    """Setup our skeleton component."""
    # feastType = config[CONF_FEAST]
    # variationType = config[CONF_VARIATION]
    # persons = config[CONF_PERSONS]

    print(config[DOMAIN][CONF_FEAST])

    url = "https://api.simplefeast.com/api/web/meals?v=2&language=da&region=DK"

    myResponse = requests.get(url)
    
    if(myResponse.ok):

        jData = myResponse.json()
        
        # glass = getGlasses(jData['concepts'])
        feast = getFeasts(jData['concepts'])
        mealPlans = getGreenFeast(feast["mealPlans"])
        mealPlanVariations = getPlanVariationVegetarian2persons(mealPlans["mealPlanVariations"])
        meals = mealPlanVariations["box"]["meals"]


        for meal in meals:
            print(DOMAIN + ".green_day" + str(meal["day"]))
            print(meal["websiteTitle"] + "\n")
            hass.states.set(DOMAIN + ".green_day" + str(meal["day"]), meal["websiteTitle"])
                
    else:
    # If response code is not ok (200), print the resulting http error code with description
        myResponse.raise_for_status()

    # Return boolean to indicate that initialization was successfully.
    return True