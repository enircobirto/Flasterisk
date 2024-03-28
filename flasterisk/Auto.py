from flasterisk import Flasterisk
from flask import request, jsonify

class Auto(Flasterisk):
    def __init__(self):
        Flasterisk.__init__(self,"auto")

    def hello(self):
        return "Hello!", 200

    def olleh(self, *, methods=['POST','GET']):
        if request.method == 'POST':
            req = request.get_json()
            return jsonify(result=f"{req.get('message','Hello!')[::-1]}", status=200)
        elif request.method == 'GET':
            return jsonify(result="!olleH", status=200)

    def olleh2(self, backwards, normal):
        return jsonify(result=backwards[::-1]+" "+normal, status=200)

