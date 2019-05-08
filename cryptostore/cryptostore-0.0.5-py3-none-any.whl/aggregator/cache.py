'''
Copyright (C) 2018-2019  Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''
class Cache:
    def read(self, exchange, dtype, pair):
        raise NotImplementedError
    
    def delete(self, *args):
        raise NotImplementedError
