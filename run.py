from Example import Example
from flask import Flask

def main():
    app = Flask(__name__)
    example = Example()
    app.register_blueprint(example.blueprint)
    app.run()

if __name__ == '__main__':
    main()
