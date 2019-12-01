import json
import os

import numpy as np
import pandas as pd


# Required for ICLR 2020 since no numerical scores are present in the
# raw files.
experience_to_score = {
    'I have published in this field for several years.': 3,
    'I have published one or two papers in this area.': 2,
    'I have read many papers in this area.': 1,
    'I do not know much about this area.': 0
}
thoroughness_to_score = {
    "I read the paper at least twice and used my best judgement in assessing the paper.": 2,
    "I made a quick assessment of this paper.": 1,
    "N/A":0,
    "I read the paper thoroughly.": 3
}

def extract_data_from_review(review):

    rating = review['rating']
    rating = rating.split(':')[0]

    if 'confidence' in review.keys():
        confidence = review['confidence']
        confidence = confidence.split(':')[0]
    else:
        confidence = None

    if 'review_assessment:_thoroughness_in_paper_reading' in review:
        thoroughness = thoroughness_to_score[review['review_assessment:_thoroughness_in_paper_reading']]
    else:
        thoroughness = None

    if 'experience_assessment' in review:
        experience = experience_to_score[review['experience_assessment']]
    else:
        experience = None

    n_words = len(review['review'].split())


    result = {
        'rating': rating,
        'n_words': n_words,
    }

    if confidence is not None:
        result['confidence'] = confidence
        
    if thoroughness is not None:
        result['thoroughness'] = thoroughness

    if experience is not None:
        result['experience'] = experience

    return result


df = pd.DataFrame()

for root, dirs, files in os.walk('Data/2020'):
    for filename in files:
        if filename.endswith('.json'):
            with open(os.path.join(root, filename)) as f:
                review = json.load(f)
                row = extract_data_from_review(review)

                row['review_id'] = os.path.splitext(
                    os.path.basename(filename))[0]

                row['paper_id'] = os.path.basename(
                    os.path.dirname(
                        os.path.join(root, filename)))

                fname_initial = os.path.join(root.replace("2020","2020_initial"), filename)
                if(not os.path.isfile(fname_initial)):
                    continue
                with open(fname_initial) as f_init:
                    initial_review = json.load(f_init)
                    initial_row = extract_data_from_review(initial_review)
                    row['initial_rating'] = initial_row['rating']

                df = df.append(row, ignore_index=True)

df.to_csv('2020.csv', index=False)
