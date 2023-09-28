import requests
import json
from datetime import datetime
from credentials import NUTRITIONIX_APP_ID, NUTRITIONIX_API_KEY, SHEETY_USERNAME, SHEETY_SHEET_NAME, SHEETY_PROJECT_NAME, SHEETY_BEARER_TOKEN

def get_exercise_stats(query):
    nutritionix_exercise_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'
    nutritionix_exercise_headers = {
        'x-app-id': NUTRITIONIX_APP_ID,
        'x-app-key': NUTRITIONIX_API_KEY,
        'Content-Type': 'application/json'
    }
    nutritionix_exercise_body = {
        'query': query,
        'gender': 'male',
        'weight_kg': 97,
        'height_cm': 194.00,
        'age': 42
    }

    response = requests.post(url=nutritionix_exercise_endpoint, headers=nutritionix_exercise_headers, json=nutritionix_exercise_body)
    response.raise_for_status()
    return response.text

def save_data_to_google_sheets(exercise_stats):
    sheety_api_url = f'https://api.sheety.co/{SHEETY_USERNAME}/{SHEETY_PROJECT_NAME}/{SHEETY_SHEET_NAME}'
    sheety_api_headers = {
        "Authorization": f"Bearer {SHEETY_BEARER_TOKEN}"
    }
    for exercise in exercise_stats['exercises']:
        sheety_data = {
            "workout": {
                "date": datetime.now().strftime('%d/%m/%Y'),
                "time": datetime.now().strftime("%I:%M %p"),
                "exercise": exercise['name'].title(),
                "duration": exercise['duration_min'],
                "calories": exercise['nf_calories']
            }
        }
        response = requests.post(url=sheety_api_url, json=sheety_data, headers=sheety_api_headers)
        response.raise_for_status()
        print(response.text)
    
    return response.text

exercise_stats = get_exercise_stats(input("Tell me which exercises you did: "))
save_data_to_google_sheets(json.loads(exercise_stats))
