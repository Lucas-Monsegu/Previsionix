import requests
import json
from Tools.tools import log

def IsOpened():
    url = 'https://www.parcasterix.fr/webservices/api/horaires_parc.json?lang=fr'
    headers={
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; HTC One_M8 Build/MRA58K',
            'Host': 'www.parcasterix.fr',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
    try:
        res = json.loads(requests.get(url, headers=headers).text)
    except Exception as e:
        log('error while asking is parc opened', str(e))
        return False
    return res['result']['parc_ouvert']

def Get():
    url = 'http://www.parcasterix.fr/webservices/api/attentix.json?lang=fr' 
    headers={
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; HTC One_M8 Build/MRA58K',
            'Host': 'www.parcasterix.fr',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
    try:
        res = json.loads(requests.get(url, headers=headers).text)
        cleanRes = {}
        with open('codeTable.json', 'r') as f:
            table = json.load(f)
            if not res.get('latency') or res.get('code') != 0:
                return None
            cleanRes = {table[attr['attractionid']]: attr['latency'] for attr in res['latency']['latency'] if 'latency' in attr.keys() and attr['attractionid'] in table.keys()}
        #print(json.dumps(cleanRes, indent=4, sort_keys=True))
        return cleanRes
    except Exception as e:
        log('Error while GET', str(e))

Get()
