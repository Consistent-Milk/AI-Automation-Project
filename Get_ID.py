from Google_AI import GAI

google_AI = GAI()
worksheet = google_AI.spreadsheet('Participant List')


def get_id():
    submitted_names = []
    review_id_list = []
    for i in range(2, 48):
        values_list = worksheet.row_values(i)
        name = values_list[0]
        review_id = values_list[2]
        submitted_names.append(name)
        review_id_list.append(review_id)

    return submitted_names, review_id_list
