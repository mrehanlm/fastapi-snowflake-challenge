import os
import json


def get_clients_from_fixture():
    client_fixtures = os.path.join(os.path.dirname(__file__), "data/fixtures.json")
    with open(client_fixtures, "r") as clients_fs:
        return json.load(clients_fs)
