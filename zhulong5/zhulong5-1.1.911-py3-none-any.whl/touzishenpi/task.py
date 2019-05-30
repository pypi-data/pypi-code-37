import time

from zhulong5.touzishenpi import touzishenpi



from lmf.dbv2 import db_command


from zhulong5.util.conf import get_conp

#1
def task_touzishenpi(**args):
    conp=get_conp(touzishenpi._name_)
    touzishenpi.work(conp,**args)



def task_all():
    bg=time.time()

    try:
        task_touzishenpi()
    except:
        print("part1 error!")


    ed=time.time()
    cos=int((ed-bg)/60)

    print("共耗时%d min"%cos)


def create_schemas():
    conp=get_conp('touzishenpi')
    arr=['touzishenpi']
    for diqu in arr:
        sql="create schema if not exists %s"%diqu
        db_command(sql,dbtype="postgresql",conp=conp)




