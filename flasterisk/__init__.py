from flask import Blueprint

class Flasterisk():
    def __init__(self,name,subchannels=[],exceptions=[]):
        self.blueprint = Blueprint(name,__name__)
        self.name = name
        self.subchannels = subchannels
        self.exceptions = exceptions
        self.defineroutes()
        return

    def defineroutes(self):
        # Gets all properties
        for propName in dir(self):
            # Separates methods, excluding 'defineroutes' and any function starting with '_'
            if callable(getattr(self,propName)) and propName!='defineroutes' and not propName.startswith('_'):
                method = getattr(self,propName)
                func = method.__func__
                if func.__kwdefaults__ is not None:
                    kwdefaults = func.__kwdefaults__
                else:
                    kwdefaults = {}
                
                # Default config
                config = {
                    "route": f"/{propName}",
                    "methods": ['GET'],
                    "vars": []
                }
                
                # If there are extra configs in the function declaration
                config.update(kwdefaults)
                
                # co_varnames, sliced from the argcount and excluding 'self'
                config['vars'] = [v for v in func.__code__.co_varnames[:func.__code__.co_argcount] if v != 'self']
                
                # Routing the vars backwards
                for var in config['vars'][::-1]:
                    config['route'] = f"/<{var}>/{config['route']}".replace("//","/")
                
                # If it's not a custom route, add the method name as a prefix
                if not kwdefaults.get("route"):
                    config['route'] = "/"+self.name+config['route']
                
                print(config['route'])
                
                self.blueprint.add_url_rule(
                    config['route'],
                    propName,
                    getattr(self,propName),
                    methods = config['methods'],
                )

    def _clean(self,*args):
        for kw in args:
            delattr(self,kw)
        return
