from flasterisk import Flasterisk
from flasterisk.Prop import Prop
from flask import request, jsonify

class Example2(Flasterisk):
    def __init__(self):
        self.abouts = {}
        Flasterisk.__init__(self, "example")

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

    def get_user_about(self, name, *, alias="about", name_opts = Prop("abouts:keys")):
        del alias, name_opts
        
        if request.method == 'GET':
            if not self._check():
                print(self._check().result)
                return jsonify(info = f"Unable to see about!",status = 200)
            return jsonify(about = self.abouts.get(name,""), status = 200)
        
    def set_user_about(
        self,name, 
        *, alias="about", methods=['POST'],
        name_regex=r'[a-z]+', about_regex=r'[a-z|A-Z]+'
    ):
        del alias,methods,name_regex,about_regex
        if request.method == 'POST':
            req = request.get_json()
            if not self._check():
                print(self._check().result)
                return jsonify(info = f"Unable to update about!",status = 200)
            
            else:
                self.abouts.update({name: req['about']})
                return jsonify(info = f"{name}'s about field is now '{req['about']}'.",status = 200)
