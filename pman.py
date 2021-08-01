#!/usr/bin/env python3

import os, json # Used for interacting with files
import sys # Used for exiting with status codes
import urllib # Used for downloading files

def is_url_secure(url):
    if not(url.startswith("https://")): # SFTP isn't a thing here either
        return False
    return True

def download_file_to_cache(url):
    if(is_url_secure(url)):
        filedata = urllib.request.urlopen(url)
        data = filedata.read()
        with open("packages/cache.zip", "wb") as outfile:
            outfile.write(data)
    else:
        print("===================")
        print(" !!!  WARNING  !!! ")
        print(" Trying to download non-secure file at " + url)
        print(" Please update your repos.json and package-list.json files to use HTTPS.")
        print(" Downloading non-secure files is not supported. Exiting.")
        print("===================")
        sys.exit(-1)

# Init argparse
import argparse

parser = argparse.ArgumentParser(description='Install and manage packages.')
parser.add_argument('operation', metavar='operation', type=str, nargs=1, help='refresh, install, or uninstall. install will update by default')
args = parser.parse_args()

# Init repos
global repos
if(os.path.exists("repos.json")):
    with open("repos.json") as repo_file:
        repos = json.load(repo_file)
else:
    print("Couldn't find repos.json, creating...")
    with open("repos.json", "w") as repo_file:
        repo_file.write("[\n\n]")
    repos = []
    
# Make sure we don't load an empty repo list
if(repos == []):
    print("Error: Repos list empty. Exiting...")
    sys.exit(-1)

# Init package list
global packagelist
if(os.path.exists("package-list.json")):
    with open("package-list.json") as packagelist_file:
        packagelist = json.load(packagelist_file)
else:
    print("Couldn't find package-list.json, creating...")
    with open("package-list.json", "w") as packagelist_file:
        packagelist_file.write("{\"installed\":[],\"sources\":{}}")
    packagelist = {"installed": {}, "sources": {}}

# This will probably need to be used by multiple operations so I'm defining it here
def refresh_sources():
    global repos, packagelist
    print("Package refresh is not implemented yet.")
    sys.exit(-1)

# Make sure we don't have an empty package list
if(packagelist["sources"] == {}):
    print("Source package list empty. Refreshing...")
    refresh_sources()

# Do whatever user wanted
if(parser.operation == "install"):
    pass
elif(parser.operation == "uninstall"):
    pass
elif(parser.operation == "refresh"):
    refresh_sources()
else:
    print("Invalid operation. See \"pman -h\" for more info.")
    sys.exit(-1)