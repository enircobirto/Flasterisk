from flasterisk.Example import Example
from flasterisk._Example import _Example
from flask import Flask
import json

app = Flask(__name__)

def main():
    example = _Example()
    print(example._show_routes())
    app.register_blueprint(example.blueprint)
    

if __name__ == '__main__':
    main()
    app.run(host="0.0.0.0", port=5300, debug=False)
    
