import json
import urllib
import requests

where = urllib.parse.quote_plus("""
{
    "Year": {
        "$lt": 2032
    }
}
""")
url = 'https://parseapi.back4app.com/classes/Car_Model_List_Acura?limit=10&where=%s' % where
headers = {
    'X-Parse-Application-Id': 'hlhoNKjOvEhqzcVAJ1lxjicJLZNVv36GdbboZj3Z',
    'X-Parse-Master-Key': 'SNMJJF0CZZhTPhLDIqGhTlUNV9r60M2Z5spyWfXW'
}
data = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) # Here you have the data that you need
print(json.dumps(data, indent=2))