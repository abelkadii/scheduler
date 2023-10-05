class InputDecoder:
    def __init__(self):
        pass

    @classmethod
    def decode(self, cin):
        args = []
        kwargs = {}
        cur=""
        applies=False
        cin+=' '
        kw=None
        for i in range(len(cin)):
            if applies:
                if cin[i]=='"':
                    applies=False
                    if kw is not None:
                        kwargs[kw]=cur
                        kw=None
                    else:
                        args.append(cur)
                    cur=""
                else:
                    cur+=cin[i]
                continue
            if cin[i]==' ':
                if cur:
                    if kw is not None:
                        if cur[0]=='-':
                            kwargs[kw]=True
                            kw=cur[1:]
                        else:    
                            kwargs[kw]=cur
                            kw=None
                    elif cur[0]=='-' and cur!='-':
                        kw=cur[1:]
                    else:
                        args.append(cur)
                cur=""
                continue
            if cin[i]=='"':
                applies=True
                continue
            cur+=cin[i]
        if kw:
            kwargs[kw]=True
        if len(args)>0:
            return args[0], args[1:], kwargs
        return '', [], kwargs