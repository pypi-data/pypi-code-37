 #!/usr/bin/python
 # -*- coding: utf-8 -*-
  
import argparse
import os
import shutil
import pprint
from constant import CONSTANT
from devopshelper import OpsbotHelper
import time
import io

def init():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    templateFile =  io.open(dir_path+"/template/"+".opsbot.template", "r")
    templateText = templateFile.read()
    templateFile.close()

    devopsFile = io.open(CONSTANT.DEFAULT_OPSBOT_PLAN,"w", newline='\n')
    devopsFile.write(unicode(templateText))
    devopsFile.close()

    print("File {} created".format(CONSTANT.DEFAULT_OPSBOT_PLAN))
    print("Please open this file to write out your devops plan.")
    return 0

def build():    
    dir_path = os.path.dirname(os.path.realpath(__file__))

    if not os.path.exists(CONSTANT.DEFAULT_OPSBOT_PLAN):
        print ("File config.opsbot not found.")
        print ("Run opsbot init to init a new config file.")
        quit()
    devopsFile = io.open(CONSTANT.DEFAULT_OPSBOT_PLAN, "r")
    lines = devopsFile.readlines()
    current_block = ""
    
    commands = []

    previousline=""

    for line in lines:
        currentline = line.strip()
        currentline = previousline + currentline

        if currentline.endswith("\\"):
            previousline = currentline[0:len(currentline)-1] + " "
            continue        
        if currentline.startswith("#"):
            continue
        if currentline == "":
            continue
        
        if currentline.startswith("["):
            current_block = currentline[1:len(currentline)-1]
            previousline = ""
        else:
            params = currentline.split(" ")
            commands.append({"command": current_block, "params":params})
            previousline = ""
       


    #TODO : Check valid commands.

    opsbot = OpsbotHelper()

    if opsbot.compile(commands) == 0:
        exit

    pp = pprint.PrettyPrinter(indent=2, width=120)
    #pp.pprint(commands)
    builddir = "./build"
    if os.path.exists(builddir) and os.path.isdir(builddir):
        shutil.rmtree(builddir)
    os.mkdir(builddir, 0o700)    
    scriptblocks = []
    for command in commands:
        functionName = "opsbot_" + command['command']
        method_to_call = getattr(opsbot, functionName)
        scripts = method_to_call(command['params'])
        if scripts != None and len(scripts) > 0 :
            heading = "#> {} > {}".format(command['command'], (" ").join(command['params']))#.upper()
            print(heading)
            # heading = "\n" + heading +"\n"
            time.sleep(.050)            
            #write build file.
            if command['command'] != "setting":
                buildFile = "./build/{}-{}.sh".format(command['command'], command['params'][0])

                #swap code
                scriptinc = ["source {}".format(buildFile)]
                scriptseperated =  [
                    '#!/bin/bash',
                    'if [ "$EUID" -ne 0 ]; then echo "Please run as sudo.";  exit; fi',
                    'if [ ! -f configgenerated ]; then echo "configgenerated not found!"; exit; fi',
                    "source configgenerated",
                    ''
                ]
                scriptseperated.extend(scripts)
                scripts = scriptinc
                # pp.pprint(scriptseperated)
                #write seperated files
                f = io.open(buildFile,"w", newline='\n')
                f.write(unicode("\n".join(scriptseperated)))
                f.close()

                os.chmod(buildFile, 0o700)
                
                print ("- {} created".format(buildFile))
            
            scriptblocks.append(heading)  
            scriptblocks.extend(scripts)
        else:
            print("???", command)

    #passwords.
    account_block_sh = "\n".join(opsbot.opsbot_account())

    # print scriptblocks[29]
    #scripts
    script_block_sh = "\n".join(scriptblocks)

    #last script
    final_block_sh  = "\n".join(opsbot.last_script)

    #
    f =  io.open(dir_path+"/template/"+"opsbot_generated.sh.template", "r")
    full_script = f.read().format(account_block=account_block_sh, 
        script_block=script_block_sh,
        final_block = final_block_sh,
        admin = opsbot.admin )
    f.close()

    f = io.open(CONSTANT.DEFAULT_OUTPUT_BASH, "w", newline='\n')
    f.write(unicode(full_script))
    f.close()

    print ("- {} created".format(CONSTANT.DEFAULT_OUTPUT_BASH))

    os.chmod(CONSTANT.DEFAULT_OUTPUT_BASH, 0o700)
    
    #begin run

    #copy password.
    shutil.copyfile(dir_path+"/template/passwordgenerated.sh","passwordgenerated.sh")
    os.chmod("passwordgenerated.sh", 0o700)
    print("- passwordgenerated.sh created")

    #write config if not exit.
    if (not os.path.exists("configgenerated")):
        f = io.open("configgenerated", "w", newline='\n')
        f.write(unicode("EMAIL_ADMIN={}\n".format(opsbot.admin)))
        f.close()
        print("- configgenerated created")


    print("Build complete! ")
    print( "Type ./{} to run automatically devops ".format(CONSTANT.DEFAULT_OUTPUT_BASH))
    
    return 0

def main():
    parser = argparse.ArgumentParser(description=u'I\'m Opsbot. I can help you build the best devops scripts.')
    subparsers = parser.add_subparsers(help='Avaiable commands',  dest='command')

    subparsers.add_parser('init', help='Create .opsbot file, where you will write devops plan')

    build_parser = subparsers.add_parser('build', help='Build .opsbot file. export devops scripts')
    build_parser.add_argument('--output', '-o', help='The output bash script file path')    

    PARSER = parser.parse_args()
    if PARSER.command == "init" :
        init()
    elif PARSER.command == "build":
        build()

if __name__ == "__main__":
    main()