from flask_auto_router.Auto import Auto
from flask import Flask, jsonify

app = Flask(__name__)

import json

def main():
    auto = Auto()
    app.register_blueprint(auto.blueprint)
    
    print(auto.blueprint)

@app.route("/routes", methods=["GET"])
def getRoutes():
    """Lista as rotas da API."""
    routes = {}
    for r in app.url_map._rules:
        routes[r.rule] = {}
        routes[r.rule]["description"] = app.view_functions[r.endpoint].__doc__
        # routes[r.rule]["functionName"] = r.endpoint
        methodList = list(r.methods)
        try:
            methodList.remove('OPTIONS')
        except:
            ...
        try:
            methodList.remove('HEAD')
        except:
            ...
        routes[r.rule]["methods"] = methodList

    routes.pop("/static/<path:filename>")

    return jsonify(routes=json.loads(json.dumps(routes).replace("<","[").replace(">","]")), status=202)

if __name__ == '__main__':
    main()
    app.run(host="0.0.0.0", port=5300, debug=False)
    
