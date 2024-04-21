from flasterisk import Flasterisk
from flask import request, jsonify

class Example(Flasterisk):
    def __init__(self):
        Flasterisk.__init__(self,"example")

    def hello(self):
        return jsonify(msg="Hello!",status=200)

    def url_shout(self, msg, *, alias='shout'):
        del alias
        return jsonify(msg=msg,status=200)

    def post_put_shout(self, *, methods=['POST','PUT'], alias='shout'):
        del methods, alias
        
        if request.method == 'POST':
            req = request.get_json()
            return jsonify(msg=req['msg'],status=200)
        else:
            return jsonify(msg="aaaa",status=200)
    
    def get_shout(self, *, alias='shout'):
        del alias
        return jsonify(msg="Hello! aAAAAAA",status=200)
