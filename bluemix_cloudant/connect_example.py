"""
{
  "cloudantNoSQLDB": [
    {
      "name": "cloudant_linked_service",
      "label": "cloudantNoSQLDB",
      "plan": "Shared",
      "credentials": {
        "username": "99a11a6d-a3f0-4eb1-ae45-2992471c52d5-bluemix",
        "password": "8f6a9a6af3ddc4b7d596b942e30fa4f4cd1d96d109dbeceaf6d6c94f753908a0",
        "host": "99a11a6d-a3f0-4eb1-ae45-2992471c52d5-bluemix.cloudant.com",
        "port": 443,
        "url": "https://99a11a6d-a3f0-4eb1-ae45-2992471c52d5-bluemix:8f6a9a6af3ddc4b7d596b942e30fa4f4cd1d96d109dbeceaf6d6c94f753908a0@99a11a6d-a3f0-4eb1-ae45-2992471c52d5-bluemix.cloudant.com"
      }
    }
  ]
}
"""
import requests
import base64
import pprint

username = '99a11a6d-a3f0-4eb1-ae45-2992471c52d5-bluemix'
passwd = '8f6a9a6af3ddc4b7d596b942e30fa4f4cd1d96d109dbeceaf6d6c94f753908a0'


t_headers = {
    'Authorization': base64.b64encode('Basic {0}:{1}'.format(username, passwd))
}
t_url = 'https://{0}:{1}@99a11a6d-a3f0-4eb1-ae45-2992471c52d5-bluemix.cloudant.com/route_points'.format(username, passwd)

req = requests.get(t_url, headers=t_headers)


print (req.content)
