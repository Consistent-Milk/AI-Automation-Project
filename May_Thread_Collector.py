with open('May_Links.txt') as f:
    lines = f.readlines()


def may_thread_collector():
    may_thread = []
    for link in lines:
        fiction_id = link.split('/')[4]
        may_thread.append(fiction_id)
    return may_thread
