# ----------------------- TRACKING APP WITH GOOGLE SPREADSHEET ------------------ #
# THE PROJECT USES THE NUTRITIONIX API TO DETERMINE THE AMOUNT OF
# CALORIES BURNED BASED ON A USER PERIOD OF EXERCISE
# DEMOGRAPHICS LIKE AGE, GENDER AND WEIGHT ARE USED TO MAKE
# A MORE ACCURATE ESTIMATE FRO THE CALORIES BURNED
import json

import requests
import datetime as dt
import os


################################ MAKING REQUESTS TO NUTRITIONIX APO ###############################

# GET API KEY AND ID FROM NUTRITIONIX API WEBSITE AFTER REGISTERING
API_KEY = os.environ.get('NUTRI_KEY')

API_ID = os.environ.get('NUTRI_ID')


# USING THE NUTRITIONIX "NATURAL LANGUAGE FOR EXERCISE" ENDPOINT
api_exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

# ENDPOINT HEADERS
headers = {
    "x-app-id" : API_ID,
    "x-app-key" : API_KEY,
    "Content-Type" : "application/json"
}

# CREATING THE CONSTANT CONSTANT VARIABLE FOR THE DEMOGRAPHY
age = int( input( "How Old Are You? " ) )
gender = input( "What is Your Gender? " )
weight = float( input( "What is Your weight (in KG)? " ) )
height = float( input( "what is Your Height (in cm)? " ) )

# PERIOD OF EXERCISE
exercise_type = input( "Tell Me The Type of Exercise You Engaged in And How Long: " )

# QUERY PARAMETERS
parameters = {"query" : exercise_type,
              "gender" : gender,
              "weight_kg" : weight,
              "height_cm" : height,
              "age" : age
              }

# MAKING A POST REQUEST TO THE API END POINT
response = requests.post( api_exercise_endpoint, headers=headers, json=parameters )
result = response.json()

print( result )


############################ USING SHEETY AND GOOGLE SHEET AS API ENDPOINT #################################

# SHEET END POINT
sheet_endpoint = os.environ.get('SHEETY_ENDPOINT')


# GETTING THE NEEDED PARAMETERS FROM NUTRITIONIX RESPONDED JSON FILE
for exercise in result['exercises']:
    sheety_parameters = {
        'sheet1': {
            'date': dt.datetime.now().strftime('%d-%m-%Y'),
            'time': dt.datetime.now().strftime('%X'),
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }


# HEADERS FOR SHEETY
token_bearer = os.environ.get('SHEETY_TOKEN')

sheety_headers = {
    "Authorization": f"Bearer {token_bearer}",
    'Content-Type': 'application/json'
}


# MAKING A POST REQUEST TO SHEETY
sheety_response = requests.post(sheet_endpoint, json=sheety_parameters, headers=sheety_headers)
                                                                                             
print(sheety_response.text)






