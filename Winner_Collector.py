with open('Winner.txt') as f:
    lines = f.readlines()


def winner():
    winner_list = []
    for link in lines:
        fiction_id = link.split('/')[4]
        winner_list.append(fiction_id[:-1])
    return winner_list
