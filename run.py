from flasterisk.Example import Example
from flask import Flask

app = Flask(__name__)

def main():
    example = Example()
    app.register_blueprint(example.blueprint)
    
    print(example.blueprint)

if __name__ == '__main__':
    main()
    app.run(host="0.0.0.0", port=5300, debug=False)
    
