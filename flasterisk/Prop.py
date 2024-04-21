class Prop():
    def __init__(self,opts_string):
        self.prop = opts_string.split(":")[0]
        self.action = opts_string.split(":")[1]
        return
    def check(self, check_string, flasterisk_instance):
        instance_prop = getattr(flasterisk_instance,self.prop)
        if self.action == 'keys':
            return check_string in instance_prop.keys()

