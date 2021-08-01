#!/usr/bin/env python3
#
#    pman - Small, cross-platform package manager.
#    Copyright (C) 2021 Johnny Stene
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

global VERSION_STRING
VERSION_STRING = "pman version 0.0.1-alpha"

import os, json # Used for interacting with files
import sys # Used for exiting with status codes
import urllib.request # Used for downloading files
import zipfile # Used for extracting packages

def is_url_secure(url):
    if("http://" in url):
        if(url.startswith("http://127.0.0.1/")): # Allow unsecure downloads from local machine only (used for testing)
            return True
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
parser.add_argument('packages', nargs='*', type=str, help="Packages to install or uninstall.")
parser.add_argument('--version', help='Print pman version.', action="store_true")
args = parser.parse_args()

if(args.version):
    print(VERSION_STRING + " - Copyright (C) 2021 Johnny Stene")
else:
    print("pman Copyright (C) 2021 Johnny Stene")

print("This program comes with ABSOLUTELY NO WARRANTY; for details see LICENSE.")
print("This is free software, and you are welcome to redistribute it")
print("under certain conditions; see LICENSE for details.)")

# Init packages folder
if not(os.path.exists("packages")):
    os.mkdir("packages")

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
    for repo in repos:
        print("Downloading package list from " + repo + "...")
        try:
            if(repo.endswith("/")):
                repo = repo[:-1]
            filedata = urllib.request.urlopen(repo + "/packages.json")
            data = filedata.read()
            packagelist["sources"][repo] = json.loads(data)
            print("Found " + str(len(packagelist["sources"][repo])) + " package(s).")
        except:
            print("ERROR: Failed to get package list from " + repo + ".")
    with open("package-list.json", "w") as outfile:
        json.dump(packagelist, outfile)

def get_package_and_depends(package):
    packages = {}
    found = None
    for source in packagelist["sources"]:
        if(package in packagelist["sources"][source]):
            found = packagelist["sources"][source][package]
            break
    if(found):
        for dependency in found["depends"]:
            if(dependency not in packagelist["installed"]):
                packages = {*packages, *get_package_and_depends(dependency)}
        packages[package] = found
    else:
        print("Couldn't find package " + package + ".")
        sys.exit(-1)
    return packages

def recursive_delete(path):
    if(os.path.exists(path)):
        if(os.path.isdir(path)):
            recursive_delete(path + "/" + os.listdir(path))
            os.rmdir(path)
        else:
            os.remove("packages/" + filename)

# Make sure we don't have an empty package list
if(packagelist["sources"] == {}):
    print("Source package list empty. Refreshing...")
    refresh_sources()

# Do whatever user wanted
if(args.operation[0] == "install"):
    packages_to_install = {}
    if(len(args.packages) > 0):
        for package in args.packages:
            packages_to_install.update(get_package_and_depends(package))
    else: # Update
        for package in packagelist.installed:
            packages_to_install.update(get_package_and_depends(package))
    for package in packages_to_install:
        if(package in packagelist["installed"]):
            if(packagelist["installed"][package]["version"] == packages_to_install[package]["version"]):
                print("Not updating " + package + ".")
                continue
            print("Updating " + package + "...")
        else:
            print("Installing " + package + "...")

        filelist = []
        try:
            download_file_to_cache(packages_to_install[package]["path"])
            cache_zip = zipfile.ZipFile("packages/cache.zip")
            cache_zip.extractall("packages")
            filelist = cache_zip.namelist()
            os.remove("packages/cache.zip")
        except:
            print("Error installing " + package + ".")
            # We've already probably installed some things, dump package list to disk.
            with open("package-list.json", "w") as outfile:
                json.dump(packagelist, outfile)
            sys.exit(-1)
        packagelist["installed"][package] = packages_to_install[package]
        packagelist["installed"][package]["files"] = filelist
    print("Saving installed packages to disk...")
    with open("package-list.json", "w") as outfile:
        json.dump(packagelist, outfile)
elif(args.operation[0] == "uninstall"):
    for package in args.packages:
        if(package in packagelist["installed"]):
            print("Uninstalling " + package + "...")
            try:
                for filename in packagelist["installed"][package]["files"]:
                    realpath = "packages/" + filename
                    recursive_delete(realpath)
                packagelist["installed"].pop(package)
                print("Uninstalled " + package + ".")
            except:
                print("Error uninstalling " + package + "...")
                # We've already probably uninstalled some things, dump package list to disk.
                with open("package-list.json", "w") as outfile:
                    json.dump(packagelist, outfile)
                sys.exit(-1)
        else:
            print(package + " not installed.")
    with open("package-list.json", "w") as outfile:
        json.dump(packagelist, outfile)
elif(args.operation[0] == "refresh"):
    refresh_sources()
else:
    print("Invalid operation. See \"pman -h\" for more info.")
    sys.exit(-1)