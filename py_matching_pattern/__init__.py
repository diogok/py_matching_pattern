
from threading import Lock
from copy import deepcopy
from uuid import uuid4

class InvalidKeySize(Exception):
    pass

class InvalidKeyCount(Exception):
    pass

class KeyNotFound(Exception):
    pass

class PatternMatchStore:

    default =None

    def __init__(self,keysize=1,raise_notfound=False):
        if keysize < 1:
            raise InvalidKeySize

        self.__db = {}
        self.__stage = {}
        self.__keysize=keysize
        self.__lock = Lock()

        self.raise_notfound = raise_notfound

        self.default=uuid4()

    def put(self,keys=[],value=None):
        if(len(keys)<self.__keysize):
            raise InvalidKeyCount

        node=self.__stage
        for n in range(self.__keysize):
            key=keys[n]
            if n == self.__keysize - 1:
                node[key]=value
            else:
                if key not in node:
                    node[key]={}
                node=node[key]
                
    def clean(self):
        self.__stage={}

    def commit(self):
        dbcopy=deepcopy(self.__stage)
        self.__lock.acquire(blocking=True,timeout=-1)
        self.__db=dbcopy
        self.__lock.release()
    
    def get(self,keys=[]):
        if(len(keys)<self.__keysize):
            raise InvalidKeyCount

        self.__lock.acquire(blocking=True,timeout=-1)
        value = self.__get(keys=keys)
        self.__lock.release()

        if value is None and self.raise_notfound:
            raise KeyNotFound

        return value

    def __default_filled(self,keys,key_mask):
        # TODO: there is a better solution
        new_keys=[]
        for n in range(self.__keysize):
            mask = key_mask[n]
            if mask == "1":
                new_keys.append(keys[n])
            else:
                new_keys.append(self.default)
        
        return new_keys

    def __get(self,keys=[]):
        int_limit = pow(2,self.__keysize)
        current=1
        
        while current <= int_limit:
            key_mask = format(int_limit - current,f"0{self.__keysize}b")
            current_keys = self.__default_filled(keys=keys,key_mask=key_mask)

            node=self.__db

            for n in range(self.__keysize):
                key=current_keys[n]

                if key in node:
                    if n+1 == self.__keysize:
                        return node[key]
                    node=node[key]
                    continue
                else:
                    current = current + 1
                    break

        return None
