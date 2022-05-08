with open('Links.txt') as f:
    lines = f.readlines()


def april_thread_collector():
    april_thread = []
    for link in lines:
        fiction_id = link.split('/')[4]
        april_thread.append(fiction_id)
    return april_thread
