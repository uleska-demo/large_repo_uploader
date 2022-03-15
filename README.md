# large_repo_uploader

This is a utility script for working with large repos (over 500MB) and the Uleska Platform.  This script:

* Removes files that are typically large and not useful in scans (suffixs ending in .zip, .ZIP, .bin, .so, .so.2, .dylib, .jpg, .JPEG, .wmv, .dll)
* Zips the repo up
* Uploads the repo to the Uleska Platform for the application and version specified

You will need an account to the Uleska Platform, an auth token, and an application/version to upload to.

Usage is as follows:

    usage: large_repo_uploader.py [-h] --uleska_host ULESKA_HOST --token TOKEN
                              [--application_name APPLICATION_NAME]
                              [--version_name VERSION_NAME] [--path PATH]

    Uleska 'Large Repo Uploader'. Removes typically large files and uploads to the
    project/pipeline to test (you can specify either --application_name and
    --version_name, or --application and --version (passing GUIDs))

    optional arguments:
      -h, --help            show this help message and exit
      --uleska_host ULESKA_HOST
                            URL to the Uleska host (e.g. https://s1.uleska.com/)
                            (note final / is required)
      --token TOKEN         String for the authentication token
      --application_name APPLICATION_NAME
                            Name for the application to reference
      --version_name VERSION_NAME
                            Name for the version/pipeline to reference
      --path PATH           path to the local code repo to trim, zip, and upload
