#! /usr/bin/python
__author__ = 'fer'


import sys
import json
from bluemix.cloudant_manager import account


def main(args):
    if len(args) < 1:
        sys.exit(2)

    route_filepath = args[0]

    with open(route_filepath, 'r') as fin:
        route_json = fin.read()
    d = json.loads(route_json)
    print d
    db_name = 'omnimobi'
    db = account.database(db_name)
    doc = db.document(d['_id'])
    resp = doc.put(params=d)

    print resp
    print resp.json()


if __name__ == "__main__":
    main(sys.argv[1:])
