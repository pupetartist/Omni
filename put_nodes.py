#! /usr/bin/python
__author__ = 'fer'

import sys
import json
from bluemix.cloudant_manager import account


def main(args):
    if len(args) < 1:
        sys.exit(2)

    nodes_filepath = args[0]

    with open(nodes_filepath, 'r') as fin:
        route_json = fin.read()
    d = json.loads(route_json)

    db_name = 'omnimobi'
    db = account.database(db_name)

    for node in d:
        doc = db.document(node['_id'])
        resp = doc.put(params=node)
        print resp
        print resp.json()


if __name__ == "__main__":
    main(sys.argv[1:])
