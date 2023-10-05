class Success:
    def __init__(self, *msgs):
        self.msgs = msgs
    
    def log(self, logger):
        for msg in self.msgs:
            logger.log(msg)
        
class Bundle:
    def __init__(self, *logs):
        self.logs = logs
    
    def log(self, logger):
        for log in self.logs:
            log.log(logger)

class Warn:
    def __init__(self, *msgs):
        self.msgs = msgs
    
    def log(self, logger):
        for msg in self.msgs:
            # logger.warn(msg)
            logger.log(msg)

class Error(Exception):
    def __init__(self, *msgs):
        super().__init__(*msgs)

class Exit(Exception):
    def __init__(self):
        super().__init__()
    
class Table:
    def __init__(self, array, maximum=float('inf'), blank=' ', indent=4, log_length=False, msg=None):
        self.array = array
        self.maximum = maximum
        self.blank=blank
        self.indent=indent
        self.log_length=log_length
        self.msg=msg
    
    def log(self, logger):
        if self.msg:
            logger.log(self.msg)
        if len(self.array)==0:
            return ""
        fields = list(self.array[0].keys())
        array = [{k:k for k in fields}]+self.array
        maximum_val = [len(i) for i in fields]
        for item in array:
            for i, key in enumerate(fields):
                maximum_val[i]=max(maximum_val[i], len(str(item[key])))
        maximum_id = len(str(len(array)))
        output = []
        fields.append('#')
        for num, item in enumerate(array):
            line = [(string:=str(num))+' '*(len(string)-maximum_id)]
            if num==0:
                line=['#'+' '*(maximum_id-1)]
            for i, key in enumerate(item.keys()):
                if (length:=len((string:=str(item[key]))))>self.maximum:
                    line.append(string[:self.maximum-3]+'...')
                    continue
                line.append(string+(min(self.maximum, maximum_val[i])-length)*self.blank)
            output.append((' '*self.indent).join(line))
        output.insert(1, '')
        output = '\n'.join(output)
        if self.log_length:
            logger.log('found %s events\n'%len(self.array))
        logger.log(output)

class Obj:
    def __init__(self, obj, msg=None):
        self.obj = obj
        self.msg = msg

    def log(self, logger):
        if self.msg:
            logger.log(self.msg)
        maximum = max([len(key) for key in self.obj]) if self.obj else 0
        for key, value in self.obj.items():
            logger.log(key+':'+(maximum-len(key)+2)*' '+str(value))
        