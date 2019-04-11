import json


def pull_ip_src():

    ip_list = []

    with open('data/ti.json') as f:
        data = json.load(f)

        for entry in data['response']['Attribute']:
            if (entry['type'] == "ip-src"):
                ip_list.append(entry['value'])

    return ip_list