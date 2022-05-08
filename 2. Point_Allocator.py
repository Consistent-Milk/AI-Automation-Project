from API import RoyalApi
import pandas as pd
import spacy
from spacy.matcher import Matcher
from pathlib import Path
from Get_ID import get_id
from Date_List_Creator import date_list
from Theme_Info import april_thread, may_thread, allowed_themes
from Writathon_Collector import writathon
from Winner_Collector import winner

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
pattern = [{"LOWER": "writathon"}]
matcher.add("participant in writathon", [pattern])

submitted_names, review_id_list = get_id()

allowed_dates = date_list(2022, 4, 1, 2022, 5, 13)
allowed_themes = allowed_themes()
april_thread = april_thread()
may_thread = may_thread()
writathon_list = writathon()
winner_list = winner()


df5 = pd.DataFrame([],
                   columns=[
                       'Reviewer', 'Total Reviews', 'Total Themes Detected',
                       'Total Points', 'Max Points', 'Final Points'
                   ])

index = 0
for review_id in review_id_list:
    user = ""
    API_instance = RoyalApi(review_id)
    user_reviews = API_instance.user_reviews()

    data = user_reviews['data']
    total_reviews = len(data)

    review_count = 0
    total_themes = []
    Points = 0
    wr_count = 0
    winner_count = 0
    wr_list = []
    for i in range(total_reviews):
        date = data[i]['reviewDate'].split('T')[0]

        if str(date) in allowed_dates:
            fiction_info = API_instance.fiction_info(i)
            reviewer = data[i]['username']
            user = reviewer

            table3 = list(map(str, fiction_info['tags'].split(',')))
            table3.append(fiction_info['status'])

            detected_themes = []
            for k in table3:
                if k in allowed_themes:
                    detected_themes.append(k)
            if str(data[i]['fictionId']) in april_thread:
                detected_themes.append('april_thread')

            doc = nlp(fiction_info['description'])
            matches = matcher(doc)

            if len(matches) >= 1:
                detected_themes.append('writathon')

            if str(data[i]['fictionId']) in may_thread:
                detected_themes.append('may_thread')

            if (str(data[i]['fictionId']) in writathon_list) and (wr_count < 2):
                wr_count = wr_count + 1
                wr_list.append(str(data[i]['fictionId']))
                detected_themes.append(f'writathon_list_{wr_count}')

            if (str(data[i]['fictionId']) in winner_list) and (str(data[i]['fictionId'] not in wr_list)) and (
                    winner_count < 6):
                winner_count = winner_count + 1
                detected_themes.append(f'writathon_winner_{winner_count}')

            if len(detected_themes) == 0:
                continue

            for theme in detected_themes:
                total_themes.append(theme)

            if data[i]['isAdvanced']:
                Points = Points + 2
            else:
                Points = Points + 1

            review_count = review_count + 1

    total_themes = len(set(total_themes))

    if review_count > total_themes:
        max_points = total_themes * 2
    else:
        if review_count > 21:
            temp = 21
            max_points = temp * 2
        else:
            max_points = review_count * 2

    final_points = min(Points, max_points)

    index = index + 1
    print(f'Point Allocated: {index}')
    df6 = pd.DataFrame([[
        user, review_count, total_themes, Points,
        max_points, final_points
    ]],
        columns=[
            'Reviewer', 'Total Reviews',
            'Total Themes Detected', 'Total Points',
            'Max Points', 'Final Points'
        ])
    df5 = pd.concat([df5, df6])

*Further codes omitted*

