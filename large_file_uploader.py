import requests
import os
import shutil
import argparse
import sys
import json
import subprocess
import time

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
    
    results: list = []
    results.append(application_and_versions_info)

    for content in results:
        
        for application in content['content']:

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

arg_options.add_argument('--application_name', help="Name for the application to reference", required=True, type=str)
arg_options.add_argument('--version_name', help="Name for the version/pipeline to reference", required=True, type=str)
arg_options.add_argument('--path', help="Path to the local code repo or directory to trim, zip, and upload", type=str)


args = arg_options.parse_args()

host = ""
application_name = ""
application = "" #id
version_name = ""
version = ""  # id
token = ""
path = ""

max_repo_upload_size = 512000 # 500MB
max_repo_upload_text = "500 MB"

# Grab the host from the command line arguments
if args.uleska_host is not None:
    host = args.uleska_host

    # add trailing / onto the host if it's not there
    if host[-1] != '/':
        host = host + "/"

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

# get the sizes of the repo path directory, both as number of kb, and in human readable form.
# NOTE: using -sk instead of -s as we've seen variance across linux dists as to how -s reports
presize_int = 0
presize_int = int( subprocess.check_output(['du','-sk', path]).split()[0].decode('utf-8') )

presize_text = ""
presize_text = subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')

# report on the  size of the repo
print("Pre-check size of repo is " + presize_text + " (" + str(presize_int) + ")")


# if the repo is less then 500MB, then we don't need to trim, we can upload
if presize_int > max_repo_upload_size:

    print("\nAs repo is above " + max_repo_upload_text + " we will remove ZIPs and images that are not scanned by security tools...\n")

    # remove typically large files which are completelly unused
    for dirpaths, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".zip"):
                print("Removing file " + os.path.join(dirpaths,file))
                os.remove(os.path.join(dirpaths,file))
            if file.endswith(".ZIP"):
                print("Removing file " + os.path.join(dirpaths,file))
                os.remove(os.path.join(dirpaths,file))
            if file.endswith(".png"):
                print("Removing file " + os.path.join(dirpaths,file))
                os.remove(os.path.join(dirpaths,file))
            if file.endswith(".PNG"):
                print("Removing file " + os.path.join(dirpaths,file))
                os.remove(os.path.join(dirpaths,file))
            if file.endswith(".gif"):
                print("Removing file " + os.path.join(dirpaths,file))
                os.remove(os.path.join(dirpaths,file))
            if file.endswith(".GIF"):
                print("Removing file " + os.path.join(dirpaths,file))
                os.remove(os.path.join(dirpaths,file))
            if file.endswith(".avif"):
                print("Removing file " + os.path.join(dirpaths,file))
                os.remove(os.path.join(dirpaths,file))
            if file.endswith(".AVIF"):
                print("Removing file " + os.path.join(dirpaths,file))
                os.remove(os.path.join(dirpaths,file))
            if file.endswith(".svg"):
                print("Removing file " + os.path.join(dirpaths,file))
                os.remove(os.path.join(dirpaths,file))
            if file.endswith(".SVG"):
                print("Removing file " + os.path.join(dirpaths,file))
                os.remove(os.path.join(dirpaths,file))
            if file.endswith(".tiff"):
                print("Removing file " + os.path.join(dirpaths,file))
                os.remove(os.path.join(dirpaths,file))
            if file.endswith(".TIFF"):
                print("Removing file " + os.path.join(dirpaths,file))
                os.remove(os.path.join(dirpaths,file))
            if file.endswith(".pdf"):
                print("Removing file " + os.path.join(dirpaths,file))
                os.remove(os.path.join(dirpaths,file))
            if file.endswith(".PDF"):
                print("Removing file " + os.path.join(dirpaths,file))
                os.remove(os.path.join(dirpaths,file))
            if file.endswith(".eps"):
                print("Removing file " + os.path.join(dirpaths,file))
                os.remove(os.path.join(dirpaths,file))
            if file.endswith(".EPS"):
                print("Removing file " + os.path.join(dirpaths,file))
                os.remove(os.path.join(dirpaths,file))
            if file.endswith(".ai"):
                print("Removing file " + os.path.join(dirpaths,file))
                os.remove(os.path.join(dirpaths,file))
            if file.endswith(".AI"):
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

    print("Finished ZIP and image removal.")

    # check if we're under 500MB yet, if not, we'll need to remove libraries which might degrade the scanning
    # as SCA tools can use them to highlight issues.  But some testing is better than none.
    size_check_int = int( subprocess.check_output(['du','-sk', path]).split()[0].decode('utf-8') )
    size_check_text = subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')

    if size_check_int > max_repo_upload_size:

        print("\nRepo is still above " + max_repo_upload_text + " (it's " + size_check_text + " [" + str(size_check_int) + "]) so we will have to remove binaries.  Note this means 3rd party library scanners won't be able to scan existing libraries, however they will still be able to scan your 3rd party config files (e.g. NPM, maven, etc).\n")

        # remove libs
        for dirpaths, dirs, files in os.walk(path):
            for file in files:
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
                if file.endswith(".dll"):
                    print("Removing file " + os.path.join(dirpaths,file))
                    os.remove(os.path.join(dirpaths,file))

    # check if we're under 500MB yet, if not, we'll need to remove the .git library (which can be big)
    # which is a pity as some git secret scanners can check it.  But some testing is better than none.
    size_check_int = int( subprocess.check_output(['du','-sk', path]).split()[0].decode('utf-8') )
    size_check_text = subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')

    if size_check_int > max_repo_upload_size:

        print("\nRepo is still above " + max_repo_upload_text + " (it's " + size_check_text + " [" + str(size_check_int) + "]) so we will have to remove the .git directory.  Note this means secrets scanners that check the git won't be able to check historical git pushes.\n")

        #remove the .git directory encase this is huge.
        for dirpaths, dirs, files in os.walk(path):
            for dir in dirs:
                if dir.endswith(".git"):
                    print("Removing directory " + path + "/" + dir)
                    shutil.rmtree(path + "/" + dir)

    print("\nRemoved all unnecessary files...\n")

    final_size_check_int = int( subprocess.check_output(['du','-sk', path]).split()[0].decode('utf-8') )
    final_size_check_text = subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')

    if final_size_check_int > max_repo_upload_size:
        print("We've removed all files we can, but the repo size is still above " + max_repo_upload_text + " (it's " + final_size_check_text + " [" + str(final_size_check_int) + "]).  Therefore we cannot upload this repo or it will fail the Uleska size checks.  Try working on a sub directory, or removing other non-code files to reduce the size of the repo for upload.")
        print("\nExiting as we could not reduce the repo size to under " + max_repo_upload_text + "...")
        exit(1)

    # report on the new size of the directory
    print("Reduced repo size is now " + final_size_check_text)

# now zip it
print("\nCreating zip file... ")
shutil.make_archive("Uleska_zipped", 'zip', path)
print("Created zip file Uleska_zipped.zip \n")

# We've got the repo into a state where it's ready for upload as a ZIP.  Update the version config to ensure
# it's accepting a ZIP file for upload, otherwise you'll get a failure.

s = requests.Session()

s.headers.update({
        'Authorization': "" + token
    })

config_url = host + "SecureDesigner/api/v1/applications/" + application + "/versions/" + version

print ("Setting version config to accept ZIP files, URL: " + config_url + "\n")

payload = '{"id":"' + version + '","name":"' + version_name + '","webPageList":[],"roles":[],"tools":[],"reports":[],"scmConfiguration":{"useUpload":true,"authenticationType":"UNAUTHENTICATED"}}'

payload_json = json.loads(payload)

try:
    StatusResponse = s.request("PUT", config_url, json=payload_json)
except requests.exceptions.RequestException as err:
    print("Exception setting version for ZIP upload\n" + str(err))
    sys.exit(2)

if StatusResponse.status_code != 200:
    # Something went wrong, maybe server not up, maybe auth wrong
    print("Non 200 status code returned when version setting version to use ZIP upload.  Code [" + str(StatusResponse.status_code) + "]")
    sys.exit(2)

print ("Version config now set to use ZIP upload.\n")

# Now upload the ZIP

print ("Uploading ZIP file.\n")

url = host + "SecureDesigner/api/v1/applications/" + application + "/versions/" + version + "/upload"

print ("Upload URL: " + url + "\n")

upload_file = open("Uleska_zipped.zip", "rb")

# let's measure how long it took to upload encase there's any issues
before_upload = time.time()

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

print ("\nUpload successful in " + str(time.time() - before_upload) + " seconds.\n")
