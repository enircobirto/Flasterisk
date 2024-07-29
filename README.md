# Flasterisk

Flasterisk is a class-based auto-router for Flask, with many configuration options. By using it, you avoid annotations entirely and the code becomes easier to maintain and divide into files.

## Installation

`
pip install flasterisk
`
(Coming soon)

## Getting started

- Create a file named run.py:

``` python
from Example import Example
from flask import Flask


def main():
    # Creates the Flask app
    app = Flask(__name__)
    
    # Instantiates the Example class and registers its blueprints
    example = Example()
    app.register_blueprint(example.blueprint)
    
    # Runs the app
    app.run()

if __name__ == '__main__':
    main()
```

- Create a file named Example.py:
```python
from flasterisk import Flasterisk
from flask import request, jsonify

class Example(Flasterisk):
    def __init__(self):
    	# Inits the Flasterisk class, giving "example" as the route prefix
        Flasterisk.__init__(self,"example")

    def hello(self):
        return jsonify(status=200,message="Hello!")
```
- Requesting on /example/hello:
```
$ curl http://localhost:5000/example/hello
{"message":"Hello!","status":200}
```


## Route configuration options

### Variables
To add a variable, simply declare it at the method, and it'll be instantly added:
```python
    def say_hello(self, name):
        return jsonify(status=200,message=f"Hello, {name}!")
```
```
$ curl http://localhost:5000/example/henirq/say_hello
{"message":"Hello, henirq!","status":200}
```

### HTTP Methods
This is where the asterisk, which gives name to the module, has to be used for the first time. Let's create a method that reverses text. If the request given is GET, it'll return "!olleH", and if it's POST, it'll return the reversed content:
```python
    def olleh(self, *, methods=['POST','GET']):
        del methods
        if request.method == 'POST':
            req = request.get_json()
            return jsonify(result=f"{req.get('message','Hello!')[::-1]}", status=200)
        elif request.method == 'GET':
            return jsonify(result="!olleH", status=200)
```
```
$ curl http://localhost:5000/example/olleh
{
  "result": "!olleH",
  "status": 200
}
$ curl -X POST http://localhost:5000/example/olleh \
  -d '{"message":"This is a message."}' \
  -H 'Content-Type: application/json'
{
  "result": ".egassem a si sihT",
  "status": 200
}
```
"del methods" is called to prevent the unused variable warning. Flasterisk is using the \_\_kwdefaults\_\_ property to configure your route, and the _" *, "_ forces that behavior. It won't work if you remove the _" *, "_.

### Alias
The alias is simply a way to overwrite the original name of the method:
```
    def internal_method_name(self, *, alias="hello"):
        del alias
        return jsonify(result="Hello!", status=200)
```
```bash
$ curl http://localhost:5000/example/hello
{"message":"Hello!","status":200}
```

## Experimental configuration options
Since this \_\_kwdefaults\_\_ technique offers such potential, I decided to play around with some possibilities. Everything past this point might not be extremely useful. For this, we'll create a simple user status manager.
```python
class Example(Flasterisk):
    def __init__(self):
        self.statuses = {}
        Flasterisk.__init__(self, "example")

```
### Regex (+ _check)
When a variable is set (in this example, "name"), and one of the \_\_kwdefaults\_\_ parameters is the same name + _regex (in this example, "usr_regex"), you can call the function _check(), which will return the result of a rule check with all the available rules.
```python
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
```
In this case, "name" will be limited to the regex '\^[a-z]+$', which means only lowercase letters. (^ and $ are added within the _check method to avoid polluting the code too much. If the check fails, _check() will return False with a list of all the available checks.

It will also work for keys _within_ the POST request!

### Opts (+ _check)
If you want to limit the variable to a list of items, use {variable_name}_opts:
```python
	def get_user_status(self, usr, *, alias="about", usr_opts = ["John","Alice","Bob"]):
   		...
```
In this example, a fixed list is made, but it isn't useful for our status app. Let's make it dynamic with our next concept:

### Prop (+ Opts and _check)
What if we could set `usr_opts = self.about.keys()`? It's not possible inside the declaration of a function, unless...
```python
from flasterisk.Prop import Prop
...
    def get_usr_status(
        self, usr, *, 
        alias="status", 
        usr_opts = Prop("statuses:keys")
    ):
        del alias, usr_opts
        
        if not self._check():
            print(self._check().result)
            return jsonify(info = f"Unable to see status!",status = 200)
        return jsonify(usr_status = self.statuses.get(usr,""), status = 200)
```
As you can imagine, every time the _check() function is called, Flasterisk will basically run self.statuses.keys() and compare it to the variable. This concept can be endlessly expanded, with the potential to be some sort of internal query mini language of some sort. For now, dict keys is all it can do.

The final status app class is in Example.py, which you can run and test it out on your own. For example:

```bash
curl http://localhost:5000/users/statuses
curl -X POST http://localhost:5000/users/john/status \
	-d '{"usr_status":"This is my status."}' \
	-H 'Content-Type: application/json'
curl http://localhost:5000/users/statuses
curl http://localhost:5000/users/john/status
curl http://localhost:5000/users/alice/status
curl -X POST http://localhost:5000/users/john123/status \
	-d '{"usr_status":"This is my status."}' \
	-H 'Content-Type: application/json'
```

