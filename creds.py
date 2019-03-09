import json

with open("creds.json") as c:
    credentials = json.load(c)

if __name__ == '__main__':
    for key, value in credentials.items():
        print(key, ": ", value)