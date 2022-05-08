from April_Thread_Collector import april_thread_collector
from May_Thread_Collector import may_thread_collector


def april_thread():
    fiction_id = april_thread_collector()

    return fiction_id


def may_thread():
    fiction_id = may_thread_collector()

    return fiction_id


def allowed_themes():
    themes = [
        'female_lead', 'space_opera', 'COMPLETED', 'one_shot',
        'villainous_lead', 'comedy', 'anti-hero_lead', 'cyberpunk',
        'Artificial_Intelligence', 'First_Contact'
    ]

    return themes
