from flasterisk import Flasterisk
from flask import Flask, jsonify

class Example(Flasterisk):
    def __init__(self):
        Flasterisk.__init__(self,"example")
    def hello(self):
        return "AAAAAAAAAAAAAAAAAA", 200
