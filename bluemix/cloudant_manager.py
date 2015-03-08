__author__ = 'fer'

import cloudant

username = '99a11a6d-a3f0-4eb1-ae45-2992471c52d5-bluemix'
passwd = '8f6a9a6af3ddc4b7d596b942e30fa4f4cd1d96d109dbeceaf6d6c94f753908a0'

# Auth

account = cloudant.Account(username)
login = account.login(username, passwd)
assert login.status_code == 200
