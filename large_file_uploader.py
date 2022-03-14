import requests
import os
import shutil
import argparse
import sys
import json
import subprocess

class ids:
    application_id = ""
    version_id = ""
    
# mapper function to change app and version names into ids
def map_app_name_and_version_to_ids(host, application_name, version_name, token, print_json):
    s = requests.Session()

    s.headers.update({
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Authorization': "" + token
    })

    GetApplicationsURL = host + "SecureDesigner/api/v1/applications/"
    
    print ("ApplicationsURL is: " + GetApplicationsURL)

    try:
        StatusResponse = s.request("Get", GetApplicationsURL)
    except requests.exceptions.RequestException as err:
        print("Exception getting applications and versions\n" + str(err))
        sys.exit(2)

    if StatusResponse.status_code != 200:
        # Something went wrong, maybe server not up, maybe auth wrong
        print("Non 200 status code returned when getting applications and versions.  Code [" + str(
            StatusResponse.status_code) + "]")
        sys.exit(2)

    application_and_versions_info = {}

    try:
        application_and_versions_info = json.loads(StatusResponse.text)
    except json.JSONDecodeError as jex:
        print("Invalid JSON when extracting applications and versions.  Exception: [" + str(jex) + "]")
        print("Response: " + str(StatusResponse.content))
        sys.exit(2)

    application_id = ""
    version_id = ""

    for application in application_and_versions_info:

        if 'name' in application:

            if application['name'] == application_name:
                # We have found the application, record the GUID
                application_id = application['id']
                if not print_json:
                    print("Application ID found for [" + application_name + "]: " + application_id)

                # Now that we're in the right record for the application, find the version name
                if 'versions' in application:

                    for version in application['versions']:
                        if 'name' in version:

                            if version['name'] == version_name:
                                # We're in the right version, record the GUID
                                version_id = version['id']
                                if not print_json:
                                    print("Version ID found for [" + version_name + "]: " + version_id)

                                break

    # check ""
    if application_id == "" or version_id == "":
        # we didn't find one of the ids, so return a failure
        print(
            "Failed to find one or both ids: application name [" + application_name + "], id [" + application_id + "], version name [" + version_name + "] id [" + version_id + "]")
        sys.exit(2)

    results = ids()
    results.application_id = application_id
    results.version_id = version_id

    if not print_json:
        print(
            "Mapped names to ids: application name [" + application_name + "], id [" + results.application_id + "], version name [" + version_name + "] id [" + results.version_id + "]")

    return results




# Capture command line arguments
arguments = sys.argv

# Capture command line arguments
arg_options = argparse.ArgumentParser(
    description="Uleska 'Large Repo Uploader'. Removes typically large files and uploads to the project/pipeline to test (you can specify either --application_name and --version_name, or --application and --version (passing GUIDs))", )
arg_options.add_argument('--uleska_host',
                             help="URL to the Uleska host (e.g. https://s1.uleska.com/) (note final / is required)",
                             required=True, type=str)
arg_options.add_argument('--token', help="String for the authentication token", required=True, type=str)

arg_options.add_argument('--application_name', help="Name for the application to reference", type=str)
arg_options.add_argument('--version_name', help="Name for the version/pipeline to reference", type=str)
arg_options.add_argument('--path', help="path to the local code repo to trim, zip, and upload", type=str)


args = arg_options.parse_args()

host = ""
application_name = ""
application = "" #id
version_name = ""
version = ""  # id
token = ""
path = ""

# Grab the host from the command line arguments
if args.uleska_host is not None:
    host = args.uleska_host

# Grab the application id from the command line arguments
if args.application_name is not None:
    application_name = args.application_name
    
# Grab the version from the command line arguments
if args.version_name is not None:
    version_name = args.version_name

# Grab the token from the command line arguments
if args.token is not None:
    token = args.token

# Grab the path from the command line arguments
if args.path is not None:
    path = args.path
     
    
results = map_app_name_and_version_to_ids(host, application_name, version_name, token, False)

application = results.application_id
version = results.version_id
    
# report on the  size of the repo
print("Pre-check size of repo is " + subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8') )
      
# remove typically large files
for dirpaths, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".zip"):
            print("Removing file " + os.path.join(dirpaths,file))
            os.remove(os.path.join(dirpaths,file))
        if file.endswith(".ZIP"):
            print("Removing file " + os.path.join(dirpaths,file))
            os.remove(os.path.join(dirpaths,file))
        if file.endswith(".bin"):
            print("Removing file " + os.path.join(dirpaths,file))
            os.remove(os.path.join(dirpaths,file))
        if file.endswith(".so"):
            print("Removing file " + os.path.join(dirpaths,file))
            os.remove(os.path.join(dirpaths,file))
        if file.endswith(".so.2"):
            print("Removing file " + os.path.join(dirpaths,file))
            os.remove(os.path.join(dirpaths,file))
        if file.endswith(".dylib"):
            print("Removing file " + os.path.join(dirpaths,file))
            os.remove(os.path.join(dirpaths,file))
        if file.endswith(".jpg"):
            print("Removing file " + os.path.join(dirpaths,file))
            os.remove(os.path.join(dirpaths,file))
        if file.endswith(".JPEG"):
            print("Removing file " + os.path.join(dirpaths,file))
            os.remove(os.path.join(dirpaths,file))
        if file.endswith(".wmv"):
            print("Removing file " + os.path.join(dirpaths,file))
            os.remove(os.path.join(dirpaths,file))
        if file.endswith(".dll"):
            print("Removing file " + os.path.join(dirpaths,file))
            os.remove(os.path.join(dirpaths,file))

    #remove the .git directory encase this is huge.  It's not needed for many scanning tools
    for dir in dirs:
        if dir.endswith(".git"):
            print("Removing directory " + path + "/" + dir)
            shutil.rmtree(path + "/" + dir)
            
print("Removed all unnecessary files...\n")

# report on the new size of the directory
print("Reduced repo size is now " + subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8') )

# we've trimmed it as much as we can, now zip it
shutil.make_archive(path + "_zipped", 'zip', path)
print("Created zip file " + path + "_zipped.zip \n")

url = host + "SecureDesigner/api/v1/applications/" + application + "/versions/" + version + "/upload"

print ("Upload URL: " + url + "\n")

s = requests.Session()

s.headers.update({
        'Authorization': "" + token
    })

upload_file = open(path + "_zipped.zip", "rb")


try:
    StatusResponse = s.post(url, data={"name":"file"}, files = {"file": upload_file})
except requests.exceptions.RequestException as err:
    print("Exception uploading zip file\n" + str(err))
    sys.exit(2)

if StatusResponse.status_code != 200:
    # Something went wrong, maybe server not up, maybe auth wrong
    print("Non 200 status code returned when uploading zip file.  Code [" + str(
        StatusResponse.status_code) + "]")
    print("Response: " + str(StatusResponse.content))
    sys.exit(2)

print ("\nUpload successful\n")
