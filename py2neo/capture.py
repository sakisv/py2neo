
import json

import py2neo.packages.httpstream.http as http

capture_file = None
capture_methods = None


def start(file_name, methods=("PUT", "POST", "DELETE")):
    global capture_file, capture_methods
    capture_file = open(file_name, "w")
    capture_methods = methods


def stop():
    global capture_file
    capture_file.close()
    capture_file = None


def capture(method, uri, body):
    global capture_file, capture_methods
    if method == "POST" and uri.startswith("index/node/"):
        index_name = uri[11:]
        key = body["key"]
        value = body["value"]
        node_id = int(body["uri"].rpartition("/")[2])
        capture_file.write('({0})<=|{1} {2}|\n'.format(node_id, index_name, json.dumps({key: value}, separators=",:")))


http.capture = capture