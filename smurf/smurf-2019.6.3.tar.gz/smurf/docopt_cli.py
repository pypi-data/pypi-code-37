#!/usr/bin/env python3                       
#123456789012345678901234567890123456789012 #
import random                                 
import time                                  
import sys                                   
from docopt import docopt                    
#123456789012345678901234567890123456789012 #
def myclear():  #copy from click.clear      #
 '''Clears the terminal screen.  This will  #
 have the effect of clearing'''             #
 sys.stdout.write('\033[2J\033[1;1H')       #
#123456789012345678901234567890123456789012 #
_docopt="""smurf                            
 Usage:                                     
  smurf from <from> to <to> [delay <delay>] 
  smurf demo                                
  smurf -h | --help                         
  smurf --version                           
Options:                                    
  -h --help          Show this screen.      
  --version          Show version.          
  --debug            Show debug messages,   
                     for nerdy geeks        
  -b  --bare         only show morfing      
"""                                         
#123456789012345678901234567890123456789012 #
ri=random.randint                           #
def pcs(s,t=0.2):                           #
 myclear()                                  #
 print(s)                                   #
 time.sleep(t)                              #
T=0.7                                       #
#123456789012345678901234567890123456789012 #
_msg='''{m}'''                              #
_msg='''{f}{m}{t}'''                        #
_msg='''smurfing...                         #
from: '{from}'                              #
morf: '{morf}'                              #
  to: '{to}'                                #
'''                                         #
_msg='''{m}'''                              #
def ms(f,m,t):                              #
 d={}                                       #
 d['f']=d['from']=f                         # 
 d['m']=d['morf']=m                         #
 d['t']=d['to']=t                           #
 return _msg.format(**d)                    #
#123456789012345678901234567890123456789012 #
def m(f,t,d):                               #
 '''for morfing a string randomly from a    #
    source string to a random string        #
    for example,try:                        #
    set t 'merhaba:)'                       #
    set e '(:hello'                         #
    $ smurf from $t to $e d 0.3             #
              /todos:multiline              #
             /feedback welcome:)            #
            /colors >>>smurfing:blue        #
           /        -:red                   #
          /         +:green                 #
         /          ~:orange                #
        /            fade back              #
       /streams mqtt,kafka,strapi           #
      /within pipes, make safe share        #
     /use within hexy, simphex, cells       #
    /use within bu3 as hiding in foam       #
   /use for partly safe sharing a string    #
  /recognize of a random step from smurf    #
 /calculate edit distances/entropy diffing  #
/use perl style string a..z:abcdefghi...xyz #
 '''                                        #
#123456789012345678901234567890123456789012 #
 global T                                   #
 T=d                                        #
 if f==t:                                   #
  pcs('''sorry, refusing to smurf,          #
  there is no path to follow''')            #
  return                                    #
 msg=ms(f,f,t)                              #
 pcs(msg,T)                                 #
 of=f                                       #
 ot=t                                       #
 lf=len(f)                                  #
 lt=len(t)                                  #
 if lf>lt:                                  #
  while lf>lt:                              #
   r=ri(0,lf-1)                             #
   f=f[:r]+f[r+1:]                          #
   pcs(ms(of,f,t),T)                        #
   lf=len(f)                                #
 if lf<lt:                                  #
  while lf<lt:                              #
   r=ri(0,lf-1)                             #
   f=f[:r]+t[-r]+f[r:]                      #
   pcs(ms(of,f,t),T)                        #
   lf=len(f)                                #
 n=0                                        #
 l=[0 for i in range(lt)]                   #
 while n<lt:                                #
  r=ri(0,lt-1)                              #
  if l[r]:continue                          #
  n+=1                                      #
  l[r]=1                                    #
  c=t[r]                                    #
  #t=t[:r]+t[r+1:]                          #
  f=f[:r]+c+f[r+1:]                         #
  pcs(ms(of,f,t),T)                         #
  lt=len(t)                                 #
 pcs(ms(of,f,t),T)                          #
                                            #
                                            #
 #thnx='''\nthats all folks!                #
 #thanks for watching:)'''                  #
 #pcs(msg+f+thnx,T)                         #
                                            #
#123456789012345678901234567890123456789012 #
def go(n,d):                                #
 if n in d and d[n]:                        #
  return d['<'+n+'>']                       #
#123456789012345678901234567890123456789012 #
DEBUG=True                                  #
def debug(**k):                             #
 print(**k)                                 #
deb=debug                                   #
#123456789012345678901234567890123456789012 #
def main():                                 #
 ad = docopt(_docopt,                       #
             version='smurf 2019.05.19')    #
 #deb({'a':ad})                             #
 #deb(a=ad)                                 #
 f=go('from',ad)                            #
 t=go('to',ad)                              #
 bare=go('bare',ad)                         #
 d=go('delay',ad)                           #
 #o=go('options',ad)                        #
 if d:d=float(d)                            #
 if not d:d=T                               #
                                            #
 #t='merhaba dünya:)'                       #
 #e='hello world:)'                         #
 #if demo:i.m(f=t,t=e,d=0.2)                #
 m(f=f,t=t,d=d)                             #
#123456789012345678901234567890123456789012 #
if __name__ == '__main__':                  #
 main()
#123456789012345678901234567890123456789012 #
