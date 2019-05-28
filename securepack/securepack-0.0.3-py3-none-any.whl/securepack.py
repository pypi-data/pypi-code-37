# Author: Ruturaj Kiran Vaidya

# This is the main file
# can be used with npm
from subprocess import call
import sys
import json
import requests
from datetime import date

# To match the strings
import fuzzyset
# fuzzywuzzy can be used, but fuzzyset is faster
#from fuzzywuzzy import process

class SecurePack:
    def __init__(self, usrin):
        # Gets the user input
        self.usrin = usrin

    def __usage__(self):
        print("....\nUsage:\n\n$ python main.py npm options\n....")

    # Checks the command and returns usage if false
    def __check__(self):
        # if not npm then usage
        try:
            self.usrin[0]
        except:
            return 0
        else:
            return self.usrin[0] == "npm"

    # Calls the command
    def __call__(self):
        call(" ".join(self.usrin), shell=True)

    # returns false if match and true if otherwise
    def match(self):
        try:
            # Opens the file containing top 1000 packages
            matchlist = requests.get('https://ruturaj4.github.io/downloads/npm_download_counts.json').json()
        except:
            print("Something went wrong, try again")
            return False
        # if the package is not popular
        if self.usrin[2] not in matchlist and len(self.usrin[2]) != 1:
            # Extract first two closely matched strings
            matchlist = fuzzyset.FuzzySet(matchlist)
            match = "-- " + "\n-- ".join([x[1] for x in matchlist.get(self.usrin[2])])
            # if using fuzzywuzzy
            #match = ", ".join([i[0] for i in process.extract(usrin[2], li, limit=2)])
            print(f"Following are the closely matched popular packages:\n{match}")
            return False
        return True

    # Gives the last modified year
    @property
    def abandoned(self):
        try:
            r = requests.get('https://replicate.npmjs.com/'
                + self.usrin[2]).json()["time"]["modified"][:4]
            return int(r)
        except:
            print("Something went wrong, try again")
            return 0

    # Gives the download counts
    @property
    def downloadCounts(self):
        today = date.today().strftime('%Y-%m-%d')
        try:
            r = requests.get('https://api.npmjs.org/downloads/point/last-month/'
                + self.usrin[2]).json()["downloads"]
            return r
        except:
            print("Something went wrong, try again")
            return 0
    # Gives the package maintainers
    @property
    def maintainers(self):
        try:
            r = requests.get('https://replicate.npmjs.com/'
                + self.usrin[2]).json()["maintainers"]
            return r
        except:
            print("Something went wrong, try again")
            return [{}]
    # Gives the project repo, if present
    @property
    def repository(self):
        try:
            r = requests.get('https://replicate.npmjs.com/'
                + self.usrin[2]).json()["repository"]["url"]
            return r
        except:
            print("Something went wrong, try again")
            return [{}]

# Decisition function
def decide():
    # Keep asking
    while True:
        decision = input("Do you still want to continue?(y/n) ")
        if decision == "y":
            return True
        elif decision == "n":
            return False

# Starts here
def securepack():
    # Gets the user input
    usrin = SecurePack(sys.argv[1:])
    # Checks if the input command is valid
    if not usrin.__check__():
        usrin.__usage__()
    else:
        if usrin.usrin[1] == "--help":
            print("Help needed")
        # Matches with the top 1000 packages
        # If the option is install
        elif usrin.usrin[1] == "--install":
            if usrin.match():
                usrin.__call__()
            elif decide():
                # Calls the command if yes
                usrin.__call__()
        # Tells if the package is abandoned
        elif usrin.usrin[1] == "--abandoned":
            # Sets the date as 2018, so packages which are not
            # modified before 2018 are considered abandoned
            if (usrin.abandoned) < 2018:
                print("The package is abandoned")
            else:
                print("The package is being maintained frequently")
        # Gets the download counts
        elif usrin.usrin[1] == "--download-counts":
            print(f"Total downloads (last month) - {usrin.usrin[2]}: {usrin.downloadCounts}")
        # Gets the list of maintainers in json
        elif usrin.usrin[1] == "--maintainers":
            print(usrin.maintainers)
        # Gets the package repository
        elif usrin.usrin[1] == "--repository":
            print(usrin.repository)
