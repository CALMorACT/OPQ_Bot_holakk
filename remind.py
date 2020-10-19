import json
from remind_daka import remind_everyday

if __name__ == '__main__':
    with open("remind_daka/config.json") as config:
        config = json.load(config)
    while True:
        remind_everyday.remind_everyday(config)
