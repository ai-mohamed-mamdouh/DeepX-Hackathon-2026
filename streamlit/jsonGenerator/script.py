import pandas as pd
import json

df = pd.read_excel("../val.xlsx")

rows_array = []

def send_to_model (text):
    return {
        "aspects": ["delivery", "service"],
        "aspect_sentiments": {
            "delivery": "positive",
            "service": "negative"
        }
    }
    

def prepare_json (review_id, text):
    aspects_and_sentiments = send_to_model(text)
    return {
        "review_id": review_id,
        "aspects": aspects_and_sentiments["aspects"],
        "aspect_sentiments": aspects_and_sentiments["aspect_sentiments"]
    }

results_arr = []
for index, row in df.iterrows():
    row_res = prepare_json(row['review_id'], row['review_text'])
    results_arr.append(row_res)

with open('results.json', 'w') as json_file:
    json.dump(results_arr, json_file, indent=4)