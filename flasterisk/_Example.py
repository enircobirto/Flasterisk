from flasterisk import Flasterisk
from flask import request, jsonify

class _Example(Flasterisk):
    def __init__(self):
        self.abouts = {}
        Flasterisk.__init__(self,"example")

    def hello(self):
        msg = "Hello! This route was created simply by being declared inside the class!"
        return jsonify(message = msg, status = 200)

    def shout(self, msg):
        return jsonify(
            message = msg,
            info = "The variable was included in the route simply by being declared in the function!",
            status = 200
        )

    def about(self):
        return jsonify(abouts = self.abouts, status = 200)

    def group_about(self, group, *, alias="about"):
        del alias, group
        return jsonify(abouts = self.abouts, status = 200)

    def user_about(self, name, *, alias="about", methods=['GET','POST'], name_regex=r'[a-z]+'):
        del methods, name_regex, alias
        
        if request.method == 'GET':
            return jsonify(about = self.abouts.get(name,""), status = 200)
        
        elif request.method == 'POST':
            req = request.get_json()
            if not self._check_rules()['ok']:
                return jsonify(info = f"Unable to update status!",status = 200)
            
            else:
                self.abouts.update({name: req['about']})
                return jsonify(info = f"{name}'s about field is now '{req['about']}'.",status = 200)
