import requests

def get_end_status():
    r = requests.get("http://54.208.68.184/api/trip-records")
    r = r.json()
    r = r[-1]['records']

    if len(r) == 2:
        if (r[1]['action'] == 'end'):
            return 1
    else:
        return 0

def get_start_status():
    r = requests.get("http://54.208.68.184/api/trip-records")
    r = r.json()
    r = r[-1]['records']

    if len(r) == 1:
        if (r[0]['action'] == 'start'):
            return 1
    else:
        return 0
