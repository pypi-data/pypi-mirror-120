from Tea.model import TeaModel


class Context:
    config:dict = None
    def __init__(self,config):
        self.config = config.__dict__
    def get_config(self,key):
        print(self.config[key])
        if(self.config[key] is None  or str(self.config[key]) == ''):
            return ''
        else:
            return str(self.config[key])
