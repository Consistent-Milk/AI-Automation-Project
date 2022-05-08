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

df1 = pd.DataFrame([],
                   columns=[
                       'Review Date', 'Review Index', 'Form Name', 'Reviewer',
                       'Review Link','Detected Themes', 'Fiction Name', 'Content', 'Meaningful Words'
                                                                     'Overall Score', 'Review Type'
                   ])

index = 0
for review_id in review_id_list:
    API_instance = RoyalApi(review_id)
    user_reviews = API_instance.user_reviews()

    data = user_reviews['data']
    total_reviews = len(data)

    wr_count = 0
    winner_count = 0
    review_count = 1
    wr_list = []
    for i in range(total_reviews):
        date = data[i]['reviewDate'].split('T')[0]

        if str(date) in allowed_dates:
            table = [date]
            if date in allowed_dates:
                table.append(f'Review - {i + 1}')
                table.append(submitted_names[index])
                table.append(data[i]['username'])

                fiction_info = API_instance.fiction_info(i)

                link = f"https://www.royalroad.com/fiction/{data[i]['fictionId']}/{fiction_info['slug']}?review={data[i]['id']}#review-{data[i]['id']}"

                table.append(link)

                table3 = list(map(str, fiction_info['tags'].split(',')))
                table3.append(fiction_info['status'])

                detected_themes = []
                for k in table3:
                    if k in allowed_themes:
                        detected_themes.append(k)
                if str(data[i]['fictionId']) in april_thread:
                    detected_themes.append('april_thread')

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

                doc = nlp(fiction_info['description'])
                matches = matcher(doc)

                if len(matches) >= 1:
                    detected_themes.append('writathon')

                if len(detected_themes) == 0:
                    continue

                table.append(detected_themes)

                table.append(fiction_info['title'])

                doc = nlp(data[i]['content'])
                text_no_useless = [token for token in doc if token.is_alpha]

                table.append(text_no_useless)

                table.append(len(text_no_useless))

                table.append(data[i]["overallScore"])

                if data[i]['isAdvanced']:
                    table.append(2)
                else:
                    table.append(1)

                df2 = pd.DataFrame([table],
                                   columns=[
                                       'Review Date', 'Review Index', 'Form Name', 'Reviewer',
                                       'Review Link','Detected Themes', 'Fiction Name',
                                       'Content', 'Meaningful Words', 'Overall Score', 'Review Type'
                                   ])
                df1 = pd.concat([df1, df2])

                review_count = review_count + 1
            else:
                continue
    index = index + 1
    print(f'Verified: {index}')
filepath = Path('F:/Python/Data Science/RR Contest Library/3. Review_Data.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
df1.to_csv(filepath)
