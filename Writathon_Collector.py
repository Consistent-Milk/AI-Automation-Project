with open('Writathon Participants.txt') as f:
    lines = f.readlines()


def writathon():
    writathon_list = []
    for link in lines:
        fiction_id = link.split('/')[4]
        writathon_list.append(fiction_id)
    return writathon_list
