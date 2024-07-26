from flasterisk.RuleCheck import RuleCheck
from flask import Blueprint, request
import inspect
import re

class Flasterisk():
    def __init__(self,name):
        self.blueprint = Blueprint(name,__name__)
        self.name = name
        self.routes = {}
        self._defineroutes()
        return

    def _defineroutes(self):
        # Gets all properties
        for attr_name in dir(self):
            # Separates methods, excluding any function starting with '_'
            if callable(getattr(self,attr_name)) and not attr_name.startswith('_'):
                method_name = attr_name
                method = getattr(self,method_name)
                func = method.__func__
                if func.__kwdefaults__ is not None:
                    kwdefaults = func.__kwdefaults__
                else:
                    kwdefaults = {}
                
                # Default config
                name = method_name
                config = {
                    "route": f"/{name}",
                    "methods": ['GET'],
                    "vars": [],
                    "exclude": False,
                    "alias": name
                }
                
                # If there are extra configs in the function declaration
                config.update(kwdefaults)
                
                # If there is an alias config:
                if "alias" in kwdefaults:
                    name = kwdefaults['alias']
                    config.update({"alias":name,"route":f"/{name}"})
                
                # co_varnames, sliced from the argcount and excluding 'self'
                config['vars'] = [
                    v for v in func.__code__.co_varnames[:func.__code__.co_argcount]
                    if v != 'self'
                ]
                
                # Routing the vars backwards
                for var in config['vars'][::-1]:
                    config['route'] = f"/<{var}>/{config['route']}".replace("//","/")
                
                # If it's not a custom route, add the method name as a prefix
                if not kwdefaults.get("route"):
                    config['route'] = "/"+self.name+config['route']
                
                for stored_method_name,rt in self.routes.items():
                    if rt['route'] == config['route']:
                        for cfg_method in config['methods']:
                            if cfg_method in rt['methods']:
                                raise DuplicatedRoute(f"""
                                
                                Method "{cfg_method}" for the route "{config['route']}" is duplicated!
                                The server will not execute.
                                
                                Previous definition: {self.name} -> {stored_method_name}
                                Current definition:  {self.name} -> {method_name}
                                
                                Resolve the conflict before proceeding.
                                """.replace("    ",""))
                
                # Saving the route configuration, based on the method name
                self.routes[method_name] = {'route':config['route'],'methods':config['methods']}
                
                self.blueprint.add_url_rule(
                    config['route'],
                    method_name,
                    getattr(self,method_name),
                    methods = config['methods'],
                )

    def _check(self):
        try:
            req = request.get_json()
        except:
            req = {}
        
        func_name = inspect.stack()[1].function
        route = self.routes[func_name]['route']
        func = getattr(self, func_name).__func__
        kwdefaults = func.__kwdefaults__
        
        return RuleCheck(self,req,route,kwdefaults)

    def _show_routes(self):
        s = self.name+":\n"
        routes = sorted(self.routes.items(), key=lambda item:item[1]['route'])
        maxlength = max([len(r['route']) for _,r in routes])
        for method_name,route in routes:
            s+=f"  {method_name}:\n"
            s+=f"    {route['route'].ljust(maxlength+2)} {', '.join(route['methods'])}\n"
            s+="\n"
        return s

class DuplicatedRoute(Exception):
    """For when a route has two definitions for the same method."""
