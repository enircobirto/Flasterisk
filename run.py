from flask import Flask
import json

app = Flask(__name__)

def main():
    pass

if __name__ == '__main__':
    main()
    app.run(host="0.0.0.0", port=5300, debug=False)
    
