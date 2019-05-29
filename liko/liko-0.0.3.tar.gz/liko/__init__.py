import os
import multiprocessing as mp
import liko

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] for i in range(wanted_parts) ]

def raker(dt):
    resp = []
    func = dt['func']
    for x in dt['data']:
        resp.append(func(x))
    return resp 

def multi(func,param,multiple=mp.cpu_count()):
    result = []
    total_param = len(param)
    datas = liko.split_list(param,multiple)
    datas = [{'func':func ,'data':x} for x in datas]
    maper = mp.Pool(mp.cpu_count())

    result = maper.map(liko.raker,datas)
    maper.close()
    return result


if(__name__ == "__main__"):
    print('Believe in Future.')