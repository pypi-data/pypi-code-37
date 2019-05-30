import os
import string
import random
from constant import CONSTANT
from random import randint
import io



class OpsbotHelper:
    current_dir = None
    target_os = "ubuntu"
    target_os_version = "18.04"
    password_length = 32
    admin = ""
    auto_backup = 0

    user_passwords = {}
    last_script = []

    hour = 0

    def __init__(self):
        self.current_dir =  os.path.dirname(os.path.realpath(__file__))

    def template(self, path):
        f = io.open("{}/template/{}".format(self.current_dir, path), "r")
        text = f.read()
        f.close()
        return text

    def opsbot_setting(self, params):
        scripts = []
        command = "".join(params)
        segs = command.split("=")
        field = segs[0]
        value = segs[1]
        
        if field == "password_length": 
            self.password_length = int(value)
            if self.password_length < 8 or self.password_length > 64 :
                print("Setting Password Fail!")
                print("Password length need >= 8 and <= 64")
                quit()
            scripts.append("echo 'password generated with length = {}'".format( self.password_length))            
        elif field == "target_os_version":
            self.target_os_version = value            
            if self.target_os_version not in ["16.04", "17.10", "18.04"]:
                print("Build Fail!")
                print("{} version {} not support".format(self.target_os, self.target_os_version))
                quit()
            
            # scripts.append("#Check os version {}...OK".format(self.target_os_version))
            scripts.append("echo 'work on os version :{} {}'".format(self.target_os, self.target_os_version))

        elif field =="target_os":
            self.target_os = value
            if  self.target_os != "ubuntu":
                print("Build Fail!")
                print("OS {} not support".format(self.target_os))
                quit()
            # scripts.append("#Check os {}...OK".format(self.target_os))
            scripts.append("echo 'this script write for os {}'".format(self.target_os))
        elif field == "admin":
            self.admin = value
            scripts.append("echo 'Admin : {}'".format(self.admin))
        elif field == "auto_backup":
            self.auto_backup = int(value)
            scripts.append("echo Auto Backup : {}".format(["OFF","ON"][self.auto_backup]))
        
        return scripts

    def opsbot_env(self, params):
        env_name = params[0]
        scripts = []
        text = self.template("env/{}.sh".format(env_name))
        scripts.append(text)

        if(env_name == "lamp"):
            #TODO : gen password.
            #TODO: set password & auth-type
            self.user_passwords['root'] = {}
            self.user_passwords['root']['mysql'] = self.random_password()

            self.user_passwords['phpmyadmin'] = {}
            self.user_passwords['phpmyadmin']['mysql'] = self.random_password()


            if self.target_os_version == "18.04":
                text = self.template("fix/mysql-change-root-auth-type.sh")
                scripts.append(text)
            
            if self.target_os_version == "18.04":
                text = self.template("fix/phpmyadmin-upgrade-48.sh")
                scripts.append(text)
            self.last_script.append("echo \"restart apache2 after job done\"")
            self.last_script.append("service apache2 restart")
        elif(env_name == "mongodb"):
            self.user_passwords['root']['mongodb'] = self.random_password()
            self.last_script.append("echo \"restart mongo after job done\"")
            self.last_script.append("service mongodb restart")
        return scripts
    

    def random_password(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(self.password_length))

    def opsbot_account(self):
        scripts = []

        for user in self.user_passwords:
            for service in self.user_passwords[user]:
                varname = "{}_{}_password".format(user, service)
                scripts.append("./passwordgenerated.sh {varname}".format(varname=varname))
        return scripts
    
    def opsbot_user_unix(self, username):
        scripts = []
        text = self.template("user/unix.sh").format(username = username)
        scripts.append(text)
        return scripts

    def opsbot_user_mysql(self, username, prefix):
        scripts = []
        text = self.template("user/mysql.sh").format(username=username, prefix=prefix)
        scripts.append(text)
        return scripts


    def opsbot_user_mongodb(self, username, prefix):
        scripts = []
        text = self.template("user/mongodb.sh").format(username=username, prefix=prefix)
        scripts.append(text)
        return scripts
    
    def opsbot_user(self, params):
        scripts = []
        username = params[0]
        self.user_passwords[username] = {}
        self.user_passwords[username]['unix'] = self.random_password()
        scripts.extend(self.opsbot_user_unix(username))

        #TODO: parse param here
        mongo_enabled = False
        mysql_enabled = False
        database_prefix = username

        #print(params)
        for param in params:
            if param == "--mongodb" or param == "--mongo":
                mongo_enabled = True
            elif param == "--mysql":
                mysql_enabled = True
            elif str(param).startswith("--database-prefix="):
                database_prefix = str(param).split("=")[1]
        #prin("mongo_enable {} mysql_enable {} database_prefix {}".format(mongo_enabled, mysql_enable, database_prefix))

        if mysql_enabled:
            self.user_passwords[username]['mysql'] = self.random_password()
            scripts.extend(self.opsbot_user_mysql(username, database_prefix))

        if mongo_enabled:
            self.user_passwords[username]['mongodb'] = self.random_password()
            scripts.extend(self.opsbot_user_mongodb(username, database_prefix))

        return scripts

    def opsbot_site(self, params):
        scripts = []

        site = params[0]
        owner = params[1]
        public_directory = ""
        valid_domains = ["dev."+site]
        include_domains_array = []
        include_domains=""
        source_git=""
        database_git=""

        #nodejs config
        node_express = False
        port = 0
        
        for param in params:
            if str(param).startswith("--public-directory="):
                public_directory = str(param).split("=")[1]
            elif param.startswith("--include-domain="):
                include_domains = str(param).split("=")[1]
                include_domains_array = include_domains.split(",")
                valid_domains.extend(include_domains_array)
            elif param.startswith("--source-git"):
                source_git = str(param).split("=")[1]
            elif param.startswith("--database-git"):
                database_git = str(param).split("=")[1]
            elif param.startswith("--node-express"):
                node_express = True
            elif param.startswith("--port"):
                port = str(param).split("=")[1]
        
        text = self.template("site/mkdir.sh").format(site = site, owner=owner)
        scripts.append(text)

        vhost_template = "site/vhost.sh"
        if node_express == True : 
            vhost_template = "site/vhost-proxy.sh"

        text = self.template(vhost_template).format(
            site=site, 
            domains=" ".join(valid_domains), 
            public_directory = public_directory,
            port = port)

        scripts.append(text)

        #tool dbimport 
        text = self.template("site-tool/dbimport.sh" ).format(
            site=site, 
            db_username=owner
        )
        scripts.extend(self.make_site_tool(site, "dbimport.sh", text, owner ))

        #tool dbexport 
        text = self.template("site-tool/dbexport.sh" ).format(
            site=site, 
            db_username=owner
        )
        scripts.extend(self.make_site_tool(site, "dbexport.sh", text, owner ))


        #tool backup.
        if self.auto_backup == 1 and source_git != "" :             
            scripts.extend(self.opsbot_make_contab_daily("HOME=$HOME /usr/local/bin/sourcebackup {site}".format(site=site)))
        if source_git != "" : 
            comment_line_1 = ""
        else :
            comment_line_1 = "#"
        
        if self.auto_backup == 1 and database_git != "" :
            scripts.extend(self.opsbot_make_contab_daily("HOME=$HOME /usr/local/bin/dbbackup {site}".format(site=site)))
        
        if database_git != "" :
            comment_line_2 = ""
        else:
            comment_line_2 = "#"

        #tool deploysite.                
        text = self.template("site-tool/deploysite.sh" ).format(
            site=site, 
            source_git= source_git,
            database_git=database_git,
            comment_line_1 = comment_line_1,
            comment_line_2 = comment_line_2
        )
        scripts.extend(self.make_site_tool(site, "deploysite.sh", text, owner))


        text = self.template("site-tool/configgenerated" ).format(
            site=site,
            db_username = owner
        )
        scripts.extend(self.make_site_tool(site, "configgenerated", text, owner))


        #tool resetowner.                
        text = self.template("site-tool/resetowner.sh" ).format(
            site=site, 
            owner=owner)        
        scripts.extend(self.make_site_tool(site, "resetowner.sh", text, owner))
        scripts.extend(self.make_owner_can_sudo_site_tool(site, "resetowner.sh", owner))
        return scripts
        

    def opsbot_begin_block(self, params):
        scripts = []
        return scripts

    def human_readable_to_bytes(self, size):
        """Given a human-readable byte string (e.g. 2G, 10GB, 30MB, 20KB),
            return the number of bytes.  Will return 0 if the argument has
            unexpected form.
        """
        if (size[-1] == 'B' or size[-1] == 'b' ):
            size = size[:-1]
        if (size.isdigit()):
            bytes = int(size)
        else:
            bytes = size[:-1]
            unit = size[-1]
            if (bytes.isdigit()):
                bytes = int(bytes)
                if (unit == 'G'):
                    bytes *= 1073741824
                elif (unit == 'M'):
                    bytes *= 1048576
                elif (unit == 'K'):
                    bytes *= 1024
                else:
                    bytes = 0
            else:
                bytes = 0
        return bytes

    def opsbot_tool(self, params):
        cmd = params[0]
        scripts = []
        if cmd == "certbotsafe":
            #make tool safe_certbot.
            source = self.template("global-tool/certbotsafe.sh").format(admin = self.admin).replace("$","\\$").replace("`","\\`")
            scripts.extend(self.make_tool_available_global(source,CONSTANT.TOOL_SAFE_CERTBOT_NAME))
            scripts.extend(self.make_all_normal_user_can_sudo_global_tool(CONSTANT.TOOL_SAFE_CERTBOT_NAME))
        elif cmd == "dbbackup":
            source = self.template("global-tool/dbbackup.sh").replace("$","\\$").replace("`","\\`")
            scripts.extend(self.make_tool_available_global(source, "dbbackup"))
            scripts.extend(self.make_all_normal_user_can_sudo_global_tool( "dbbackup"))
        elif cmd == "sourcebackup":
            source = self.template("global-tool/sourcebackup.sh").replace("$","\\$").replace("`","\\`")
            scripts.extend(self.make_tool_available_global(source, "sourcebackup"))
            scripts.extend(self.make_all_normal_user_can_sudo_global_tool( "sourcebackup"))
        elif cmd == "dbdump":
            source = self.template("global-tool/dbdump.sh").replace("$","\\$").replace("`","\\`")
            scripts.extend(self.make_tool_available_global(source, "dbdump"))
        
        return scripts

    def make_site_tool(self, site, tool_file, command, owner):
        scripts = []
        text = self.template("util/make_site_tool.sh").format(site=site, tool_file = tool_file, command = command, owner=owner)
        scripts.append(text)
        return scripts
    def make_owner_can_sudo_site_tool(self, site, tool_file, owner):
        scripts = []
        site_nodot = site.replace(".","-")
        text = self.template("util/make_owner_can_sudo_site_tool.sh").format(site=site, tool_file = tool_file, owner=owner, site_nodot=site_nodot)
        scripts.append(text)
        return scripts

    def make_tool_available_global(self, tool_sh, tool_name):        
        scripts = []

        scripts.append(self.template("util/make_global_tool.sh").format(command=tool_sh, tool_name = tool_name))
        return scripts
    
    def make_all_normal_user_can_sudo_global_tool(self, tool_name):
        scripts = []
        text = self.template("util/make_all_normal_user_can_sudo_global_tool.sh").format(tool_name = tool_name)
        scripts.append(text)
        return scripts

    
    def opsbot_make_contab_daily(self, command):
        scripts = []
        self.hour = (self.hour+1) % 24
        minute = randint(0,59)
        scripts.append(self.template("util/make_run_daily.sh").format(hour=self.hour, minute=minute, command = command))
        return scripts

    def compile(self, commands):      
        commands.append({'command':"tool", 'params':['certbotsafe']})
        commands.append({'command':"tool", 'params':['sourcebackup']})
        commands.append({'command':"tool", 'params':['dbbackup']})
        commands.append({'command':"tool", 'params':['dbdump']})