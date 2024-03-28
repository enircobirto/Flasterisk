from flask_auto_router import AutoRouter
from flask import request, jsonify

import json

class Auto(AutoRouter):
    def __init__(self):
        AutoRouter.__init__(self,"auto")

    def hello(self):
        return "Hello!", 200

    def olleh(self, *, methods=['POST','GET']):
        if request.method == 'POST':
            req = request.get_json()
            return jsonify(result=f"{req.get('message','Hello!')[::-1]}", status=200)
        elif request.method == 'GET':
            return jsonify(result="!olleH", status=200)

    def olleh2(self, backwards, normal, *, route="/olleh2/",methods=['GET']):
        return jsonify(result=backwards[::-1]+" "+normal, status=200)

