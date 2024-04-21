from flasterisk.Prop import Prop
from flask import request
import re

class RuleCheck():
    """
    Rule Check result for variables with defined rules in the function.
    - result: dict with the results for each variable
        - url_<var>:  var passed by the URL
        - post_<var>: var passed by POST
    
    - __bool__: boolean value set to the value of the check as a whole
    """

    def __init__(self,flasterisk_instance,req,route,kwdefaults):
        result = {}
        # Get URL variables
        def clean_regex_list(result):
            # re.findall returns a list of tuples if multiple instances are found,
            # So we convert it to a list
            if type(result[0]) == tuple:
                return list(result[0])
            # Otherwise, it's a normal list with one string
            else:
                return result
        
        # Replacing <var_name> with the string '(.*?)', so it can be extracted
        url_expression = re.sub(r'<.*?>','(.*?)',route)
        url_vars = {
            var: clean_regex_list(re.findall(url_expression, request.base_url))[index]
            for index, var in enumerate(re.findall(r'<(.*?)>',route))
        }
        
        for kw in kwdefaults:
            # Getting _regex rules and extracing the results
            if type(kwdefaults[kw]) == Prop:
                flprop = kwdefaults[kw]
                if kw.endswith("_opts"):
                    var = kw.replace("_opts","")
                    if var in url_vars:
                        result["url_"+var] = flprop.check(url_vars[var],flasterisk_instance)
                    elif var in req:
                        result["url_"+var] = flprop.check(req[var],flasterisk_instance)
                pass
            
            else:
                if kw.endswith("_regex"):
                    var = kw.replace("_regex","")
                    if var in url_vars:
                        result["url_"+var] = bool(re.match("^"+kwdefaults[kw]+"$",url_vars[var]))
                    elif var in req:
                        result["post_"+var] = bool(re.match("^"+kwdefaults[kw]+"$",req[var]))
                
                elif kw.endswith("_opts"):
                    var = kw.replace("_opts","")
                    if var in url_vars:
                        result["url_"+var] = url_vars[var] in kwdefaults[kw]
                    elif var in req:
                        result["url_"+var] = req[var] in kwdefaults[kw]
        self.result = result

    def __bool__(self):
        """Sets boolean value to the general check result"""
        ok = True
        for res in self.result:
            if self.result[res] == False:
                ok = False
        return ok
