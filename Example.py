from flasterisk import Flasterisk
from flasterisk.Prop import Prop
from flask import request, jsonify

class Example(Flasterisk):
    def __init__(self):
        self.statuses = {}
        Flasterisk.__init__(self, "users")

    def usrs_statuses(self, *, alias="statuses"):
        del alias
        return jsonify(statuses = self.statuses, status = 200)

    def get_usr_status(
        self, usr, *, 
        alias="status", 
        usr_opts = Prop("statuses:keys")
    ):
        del alias, usr_opts
        
        if request.method == 'GET':
            if not self._check():
                print(self._check().result)
                return jsonify(info = f"Unable to see status!",status = 200)
            return jsonify(usr_status = self.statuses.get(usr,""), status = 200)
        
    def set_usr_status(
        self,usr,
        *, alias="status", methods=['POST'],
        usr_regex=r'[a-z]+'
    ):
        del alias,methods,usr_regex
        if request.method == 'POST':
            req = request.get_json()
            if not self._check():
                print(self._check().result)
                return jsonify(info = f"Unable to update status!",status = 200)
            
            else:
                self.statuses.update({usr: req['usr_status']})
                return jsonify(info = f"{usr}'s status is now '{req['usr_status']}'.",status = 200)
