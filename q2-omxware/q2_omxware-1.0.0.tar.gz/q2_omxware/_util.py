
import getpass
import os
import omxware

from pathlib import Path

# Read OMXWare token from token file:
#       - Token file is saved in .omxware folder in user's home directory
#       - Check if that folder and file exists, if not return None
#       - If the token file exists, read data from that file
#       - Right now, token for only one account is saved in token file
#       - Token file contains data in following format: <username> + '\t' + <token>
#       - Read data from token file and if token is present in that file, return OMXWare token
def read_token_from_file():
    home_dir = str(Path.home())
    token_file = home_dir + "/.omxware/token"
    if os.path.isfile(token_file):
        token = None
        with open(token_file) as f:
            token_line = f.readline().strip().split('\t')
            if token_line and len(token_line) == 2:
                print("Retrieved omxware token for {}\n".format(token_line[0]))
                token = token_line[1]
        return token
    return None

# Save OMXWare token in token file:
#       - Token file is saved in .omxware folder in user's home directory
#       - Check if that folder and file exists, if not create .omxware folder and token file in user's home directory
#       - Right now, token for only one account is saved in token file
#       - Token file contains data in following format: <username> + '\t' + <token>
#       - Save OMXWare username and token in token file in proper format
def save_token_to_file(username, token):
    home_dir = str(Path.home())
    omxware_path = home_dir + "/.omxware/"
    if not os.path.exists(omxware_path):
        os.makedirs(omxware_path)
    with open(omxware_path + "token", 'w') as f:
        f.write(username + '\t' + token)
    print("OMXWare token for {}'s account is saved in {}\n".format(username, omxware_path + "token")) 

# Get OMXWare token required to connect to OMXWare
#       - Check if OMXWare token is present in token file
#       - If token is available from token file, return that
#       - Otherwise, prompt for OMXware username and password
#       - Get OMXware token using the username and password
#       - Save token to token file
#       - And return token
def get_token():
    saved_token = read_token_from_file()
    if saved_token:
        return saved_token
    else:
        username = input("OMXWare username: ")
        passwd = getpass.getpass("Password: ")
        token = omxware.get_token(username, passwd)
        del passwd
        save_token_to_file(username, token)
        return token

# Connect to OMXWare
#       - Get OMXware token from token file or using OMXWare username and password
#       - Instantiate omxware object using the token
#       - Return omxware object  
def connect_to_omxware():
    omx_token = get_token()
    omx = omxware.omxware(omx_token, env='dev')
    return omx