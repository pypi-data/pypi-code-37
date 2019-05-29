# Version 3.0
def __cmd__(command):
    try:
        import os
        os.system(command)
    except Exception as e:
        print("Something went wrong in accessing the command line. This feature was well tested on Windows OS.\n This part belongs to importing of modules if they are not installed in your computer yet.\nTry installing matplotlib and pyserial manually via pip.\nAutomatic installation fail due to unaccessable command line !\n")
        print(e)

def __installationCheck__():
    try:
        import serial
        Module_1=True
    except Exception:
        Module_1=False
        print("pyserial module not found.\nDon't worry, we'll install it in your pc automatically.\nJust make sure you have good internet connection !!")
    try:
        import matplotlib
        Module_2=True
    except Exception:
        Module_2=False
        print("matplotlib module not found.\nDon't worry, we'll install it in your pc automatically.\nJust make sure you have good internet connection !!")

    return(1 if (Module_1 & Module_2)==True else 0)

def __installModules__():
    try:
        __cmd__("pip install pyserial")
        __cmd__("pip install matplotlib")
    except Exception as e:
        print(e)

def __modulesInitialization__():
    n=1
    while(__installationCheck__()!=1):
        __installModules__()
        if(n>3):
            print("This module consists auto-pip package installation yet unable to download 'matplotlib' and 'pyserial'")
            print("Try switching on your internet connection or download those two modules via pip manually")
            raise ModuleNotFoundError
            break
        n+=1
    return

__modulesInitialization__()
import time
from itertools import zip_longest as zip_longest
import serial
from serial import *
import matplotlib.pyplot as plt
from matplotlib import style
# You know what I do
def __elements(g_string):
    try:
        gstring=str(g_string)
        ng=len(gstring)-1
        lg=list()
        ig=0
        while(ig<=ng):
            lg.append(gstring[ig])
            ig+=1
        return(lg)
    except Exception as e:
        print(str(e)+'\n ERROR ID - elements')

# Checks if all the elements in the given list are unique
def __isunique(Data):
    try:
        nData=len(Data)
        nSet =len(list(set(Data)))
        if(nData==nSet):
            return(True)
        else:
            return(False)
    except Exception as e:
        print(str(e)+'\nERROR ID - isunique')

# draws a line parallel to y axis
def horizontal(y,lbl='marker',start=0,end=10):
    try:
        plt.plot([start,end],[y,y],label=lbl,linewidth=2,color='black')
    except Exception as e:
        print(str(e)+'\nERROR ID - yline')

# draws a line parallel to x axis.
def vertical(x,lbl='marker',start=0,end=10):
    try:
        plt.plot([x,x],[start,end],label=lbl,linewidth=2,color='black')
    except Exception as e:
        print(str(e)+'\nERROR ID - xline')

# Creates a marker:
def marker(x,y,limit=1,lbl="marker"):
    vertical(x,lbl=lbl,start=y-limit,end=y+limit)
    horizontal(y,lbl=lbl,start=x-limit,end=x+limit)

# Converts two lists into a dictionary
def __liDict(li1,li2):
    try:
        dictionary = dict(zip(li1,li2))
        return(dictionary)
    except Exception as e:
        print(str(e)+'ERROR ID - lidict')

# Assigns a value to a string
def assignValue(str_list):
    try:
        key=list(set(str_list))
        n=len(list(set(str_list)))//2
        retLi=[]
        if(len(list(set(str_list)))%2==0):
            for i in range(-n+1,n+1):
                retLi.append(i)
            return(__liDict(key,retLi))
        else:
            for i in range(-n,n+1):
                retLi.append(i)
            return(__liDict(key,retLi))
    except Exception as e:
        print(str(e)+'ERROR ID - assignValue')

#finds the difference between two numbers
def __diff(x,y):
    try:
        return(abs(x-y))
    except Exception as e:
        print(str(e)+'ERROR ID - diff')

# Converts all the elements of the list to integers
def __numlist(li):
    try:
        retlist=[]
        for a in range(len(li)):
            retlist.append(float(li[a]))
        return(retlist)
    except Exception as e:
        print(str(e)+'ERRO ID - numlist')

# Filters based on max deviation allowed
def maxDev(li,avg,max_deviation):
    try:
        retli=[]
        li=__numlist(li)
        for ele in range(len(li)):
            d=__diff(li[ele],avg)
            if(d<=max_deviation):
                retli.append(li[ele])
            else:
                pass
        return(retli)
    except Exception as e:
        print(str(e)+'ERROR ID - maxDev')

#checks if a parameter is of numtype
def __isnum(var):
    try:
        float(var)
        return(True)
    except:
        return(False)
    pass

#Filters data according to type
def __type_filter(Data,Type):
    try:
        ret_data=[]
        if(Type=='all'):
            return(Data)
        if(Type!='num'):
            for i in range(len(Data)):
                if(type(Data[i])==Type):
                    ret_data.append(Data[i])
            return(ret_data)
        else:
            for j in range(len(Data)):
                if(__isnum(Data[j])==True):
                    ret_data.append(Data[j])
            return(ret_data)
    except Exception as e:
        print(str(e)+'ERROR ID - type_filter')

#filters a list based on a list of values or a single value
def __value_filter(Data,Expected):
    try:
        if type(Expected) != type([]):
            expected=[]
            expected.append(Expected)
            Expected=expected
        pass
        ret_data=[]
        for i in range(len(Data)):
            if(Data[i] in Expected):
                ret_data.append(Data[i])
        return(ret_data)
    except Exception as e:
        print(str(e)+'ERROR ID - value_filter')

#Removes all the '' from a code
def __remnull__(li):
    try:
        retli=[]
        for i in range(len(li)):
            if (li[i]!=''):
                retli.append(li[i])
        return(retli)
    except Exception as e:
        print(str(e)+'ERROR ID - remnull')

# Used to set the data within limits
def __limits(Data,s,e):
    try:
        retli=[]
        for i in range(len(Data)):
            if (Data[i]<=e) and (Data[i]>=s):
                retli.append(Data[i])
        return(retli)
    except Exception as e:
        print(str(e)+'ERROR ID - limits')

# Filters data recieved from arduino
def filter(data,expected=[],expected_type=None,max_deviation=None,closeTo=None,numeric=True,limit=[]):

    data=list(data)
    if(numeric==True):
        new_data=[]
        for i in range(len(data)):
            try:
                new_data.append(float(data[i]))
            except:
                pass
        data=new_data
        if (limit!=[]):
            data=__limits(data,limit[0],limit[1])
    pass
    if closeTo!=None:
        average=closeTo
    elif __isunique(data)==False:
        average=most_frequent(data)
        print(f'Average is most_frequent data = {average}')
    elif(numeric==True) and (limit!=[]):
        average=sum(data)/len(data)
        print(f'Average is calculated as {average}')
    else:
        if (numeric==True):
            print("""
            Not enough information to filter !!
            Pass either limit , closeTo , expected or max_deviation""")
            raise BaseException
    # Average obtained
    if expected!=[] :
        data=__value_filter(data,expected)
    pass
    if expected_type!=None :
        data=__type_filter(data,expected_type)
    pass
    if max_deviation!=None :
        data=maxDev(data,average,max_deviation)
    pass
    if max_deviation==None and closeTo!=None :
        data=maxDev(data,average,1)
    pass
    return(data)

#Most frequent piece of data
def most_frequent(List):
    try:
        return (max(set(List), key = List.count))
    except Exception as e:
        print(str(e)+'ERROR ID - most_frequent')

#Least frequent piece of data
def least_frequent(List):
    try:
        return (min(set(List), key = List.count))
    except Exception as e:
        print(str(e)+'ERROR ID - least_frequent')

#Compresses data
def compress(li):
    try:
        return([i for i,j in zip_longest(li,li[1:]) if i!=j])
    except Exception as e:
        print(str(e)+'ERROR ID - compress')

#Escapes from the escape Characters
def escape(string):
    try:
        li=__elements(string)
        remli=['\b','\n','\r','\t']
        retli=[]
        for i in range(len(string)):
            if((string[i] in remli)==False):
                retli.append(string[i])
        return("".join(retli))
    except Exception as e:
        print(str(e)+'ERROR ID - escape')

#Graphs the data
def Graph(y=None,xlabel='dataPiece',ylabel='Amplitude',label='myData',color='red',title='Graph',markersize=7,stl='ggplot',d={},mark='x'):
    try:
        style.use(stl)
        if d!={} and y==None:
            replacementX=[]
            replacementY=[]
            for ele in d:
                replacementX.append(ele)
                replacementY.append(d[ele])
            x=replacementX
            y=replacementY
        else:
            x=[i for i in range(len(y))]
        plt.plot(x,y,label=label,color=color, marker=mark,markersize=markersize)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend()
        plt.show()
    except Exception as e:
        print(str(e)+'ERROR ID - Graph')

# Used to compare two graphs
def compGraph(y=None,y2=None,xlabel='dataPiece',ylabel='Amplitude',label1='myData-1',label2='myData-2',color1='red',color2='blue',title='Graph',markersize=7,stl='ggplot',fit=True,d1={},d2={}):
    try:
        style.use(stl)
        if d1!={} or d2!={}:
            fit=False
        if d1!={}:
            replacementX=[]
            replacementY=[]
            for ele1 in d1:
                replacementX.append(ele1)
                replacementY.append(d1[ele1])
            x=replacementX
            y=replacementY
        if d2!={}:
            replacementX=[]
            replacementY=[]
            for ele in d2:
                replacementX.append(ele)
                replacementY.append(d2[ele])
            x2=replacementX
            y2=replacementY
        if fit == True:
            def Map(a_value,frm,to):
                percent=(a_value/frm) * 100
                ret_value=(percent*to)/100
                return(ret_value)
            x=[i for i in range(len(y))]
            x2=[j for j in range(len(y2))]
            if(len(x)>=len(x2)):
                nli=[]
                for p in range(len(x2)):
                    x2[p]=Map(x2[p],len(x2),len(x))
            else:
                nli=[]
                for p in range(len(x)):
                    x[p]=Map(x[p],len(x),len(x2))
            plt.plot(x,y,label=label1,color=color1, marker="o",markersize=markersize,linewidth=2)
            plt.plot(x2,y2,label=label2,color=color2, marker="x",markersize=markersize,linewidth=2)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(f"{title}\nWith Fit Enabled")
            plt.legend()
            plt.show()
        else:
            x=[i for i in range(len(y))]
            x2=[j for j in range(len(y2))]
            plt.plot(x,y,label=label1,color=color1, marker="o",markersize=markersize)
            plt.plot(x2,y2,label=label2,color=color2, marker="x",markersize=markersize)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(f"{title}\nWith Fit Disabled")
            plt.legend()
            plt.show()
    except Exception as e:
        print(str(e)+'ERROR ID - compGraph')


# What this function does is it gets certain lines of data from a com port and removes the repeated values and also the escape sequence characters !!!
def ardata(COM,lines=50,baudrate=9600,timeout=1,squeeze=True,dynamic=False,msg='a',dynamicDelay=0.5):
    try:
        i=0
        all=list()
        if(type(COM)==type(1)):
            ser=serial.Serial('COM{}'.format(COM),baudrate = baudrate, timeout=timeout)
        else:
            ser=serial.Serial('{}'.format(COM),baudrate = baudrate, timeout=timeout)
        while(i<=lines):
            if(dynamic==True):
                ser.write(bytearray(msg,'utf-8'))
                time.sleep(dynamicDelay)
            all.append(escape(ser.readline().decode('ascii')))
            time.sleep(0.1)
            i+=1
        all=__remnull__(all)
        if(squeeze==False):
            return(all)
        else:
            return(compress(all))
        pass
    except Exception as e:
        print(str(e)+'ERROR ID - ardata')

#reads only one line of data from a comport:
def readSerial(COM,baudrate=9600,timeout=1):
    try:
        data=ardata(COM,1,baudrate,timeout)
        return(data)
    except Exception as e:
        print(str(e)+'\nERROR ID - readSerial')

# writes only one line to a com port !
def writeSerial(COM,baudrate=9600,timeout=1,msg=""):
    try:
        ardata(COM,1,baudrate,timeout,dynamic=True,msg=msg)
    except Exception as e:
        print(str(e)+'\nERROR ID - writeSerial')

# to get a single dynamic communication between arduino and python !
def dynamicSerial(COM,baudrate=9600,timeout=1,msg="a",dynamicDelay=0.5):
    try:
        return(ardata(COM,1,baudrate,timeout,squeeze=False,dynamic=True,msg=msg,dynamicDelay=dynamicDelay))
    except Exception as e:
        print(str(e)+"\nERROR ID - dynamicSerial")
