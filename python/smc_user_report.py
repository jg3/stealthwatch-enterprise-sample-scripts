#!/usr/bin/env python3

"""
This script will get all users and groups in Stealthwatch using the REST API.

For more information on this API, please visit:
https://developer.cisco.com/docs/stealthwatch/

 -

Script Dependencies:
    requests
Depencency Installation:
    $ pip install requests

System Requirements:
    Stealthwatch Version: 7.0.0 or higher

Copyright (c) 2019, Cisco Systems, Inc. All rights reserved.
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import requests
import json
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
import sys
from datetime import datetime

QUIET = 0

# Enter all authentication info
SMC_USER = "admin"
SMC_PASSWORD = "C1sco12345"
SMC_HOST = "localhost"
SMC_TENANT_ID = "123"
# For Tenant ID on your system run: 'ls /lancope/var/smc/config/domain_*'

if(SMC_HOST == "localhost"):
    OUTPUT_FILE = "/lancope/var/smc/tmp/UserReport.csv"
    # when running local to SMC output to https://<SMC_HOST>/smc/files/smc/tmp
else:
    OUTPUT_FILE = "./UserReport.csv"
    # Note:  output file is TAB SEPARATED, can be opened by Microsoft Excel


# Set the URL for SMC login
url = "https://" + SMC_HOST + "/token/v2/authenticate"

# Let's create the login request data
login_request_data = {
    "username": SMC_USER,
    "password": SMC_PASSWORD
}

# Initialize the Requests session
#api_session = requests.Session()
api_session = requests.Session()


# Perform the POST request to login, or give a helpful (at least amusing) error message.
try:
    response = api_session.request("POST", url, verify=False, data=login_request_data)
except requests.exceptions.RequestException as e:
    print("\n\n   OH NO!!\n   I have failed you, and the only explanation I have is this:\n")
    raise SystemExit(e)
    

# If the login was successful
if(response.status_code == 200):

    try:
        # Open a file to save output to
        with open(OUTPUT_FILE, mode='w') as output:

            # note the date the data was generated
            today = datetime.now() 
            timeStamp = today.strftime('%Y-%m-%d %H:%M:%S')
            print('Data current as of: ' + timeStamp + '\n\n', file=output)
            if not QUIET:
                print('\n\tData current as of: ' + timeStamp + '\n\n', file=sys.stdout)

            # Get the list of data roles from the SMC
            url = 'https://' + SMC_HOST + '/smc-users/rest/v1/roles/data-roles'
            response = api_session.request("GET", url, verify=False)

            # Check if the request was successful
            if (response.status_code != 200):
                raise RuntimeError("An error has occurred, while fetching roles, with the following code: {}".format(response.status_code))

            # Print all the data roles
            dRoles = json.loads(response.content)["data"]
            ###print(dRoles)
            print("The defined Data Roles are:\n", file=output)
            if not QUIET:
                print("The defined Data Roles are:\n", file=sys.stdout)
            print("roleId\troleName\troleDescription", file=output)
            for item in dRoles:
                role = item['id']
                name = item['name']
                description = item['description']
                print(f'{role}\t{name}\t{description}', file=output)
                if not QUIET:
                    print(f'{role}\t{name}\t{description}', file=sys.stdout)

            # Get the list of functional roles from the SMC
            url = 'https://' + SMC_HOST + '/smc-users/rest/v1/roles/functionroles'
            response = api_session.request("GET", url, verify=False)

            # Check if the request was successful
            if (response.status_code != 200):
                raise RuntimeError("An error has occurred, while fetching roles, with the following code: {}".format(response.status_code))

            # Print all the functional roles
            fRoles = json.loads(response.content)["data"]
            ###print(fRoles)
            print("\nThe defined Functional Roles are:\n" +
                "ROLE\tNAME\tDESCRIPTION", file=output)
            if not QUIET:
                print("\nThe defined Functional Roles are:\n" +
                    "ROLE\tNAME\tDESCRIPTION", file=sys.stdout)
            for item in fRoles:
                role = item['id']
                name = item['name']
                description = item['description']
                print(f'{role}\t{name}\t{description}', file=output)
                if not QUIET:
                    print(f'{role}\t{name}\t{description}', file=sys.stdout)
            
            # Get the list of web function roles from the SMC
            url = 'https://' + SMC_HOST + '/smc-users/rest/v1/roles/webfunctionroles'
            response = api_session.request("GET", url, verify=False)

            # Check if the request was successful
            if (response.status_code != 200):
                raise RuntimeError("An error has occurred, while fetching roles, with the following code: {}".format(response.status_code))

            # Print all the web functional roles
            wRoles = json.loads(response.content)["data"]
            print("\nThe defined Web Functional Roles are:\n" +
                "ROLE\tNAME\tDESCRIPTION",
                
                 file=output)
            if not QUIET:
                print("\nThe defined Web Functional Roles are:\n" +
                    "ROLE\tNAME\tDESCRIPTION", file=sys.stdout)
            for item in wRoles:
                role = item['id']
                name = item['name']
                description = item['description']
                print(f'{role}\t{name}\t{description}', file=output)
                if not QUIET:
                    print(f'{role}\t{name}\t{description}', file=sys.stdout)

            # Get the list of users from the SMC
            url = 'https://' + SMC_HOST + '/smc-users/rest/v1/users'
            response = api_session.request("GET", url, verify=False)

            # Check if the request was successful
            if (response.status_code != 200):
                raise RuntimeError("An error has occurred, while fetching users, with the following code: {}".format(response.status_code))
            
            # Loop through the list of users and print the relevant information.
            data = json.loads(response.content)["data"]
            print('\nThe User list is:\n' +
                'USERNAME\tFULL NAME\tEMAIL\tIS ENABLED\tDATA ROLE\tFUNCTIONAL ROLES\tWEB FUNCTIONAL ROLES\tIS ADMIN', file=output)
            if not QUIET:
                print('\nThe User list is:\n' +
                    'USERNAME\tFULL NAME\tEMAIL\t\tIS ENABLED\tDATA ROLE\t\tFUNCTIONAL ROLES\t\t\tWEB FUNCTIONAL ROLES\t\tIS ADMIN', file=sys.stdout)
            for item in data:
                username = item['userName']
                if 'fullName' in item:
                    fullname = item['fullName']
                else:
                    fullname = "--"
                if 'emailAddress' in item:
                    email = item['emailAddress']
                else:
                    email = "--"
                enabled = item['enabled']
                dataRole = next((i.get('name') for i in dRoles if i['id'] == item['dataRoleId']), "--")
                funcRoles = []
                for r in item['functionRoleIds']:
                    funcRoles.append(next((i.get('name') for i in fRoles if i['id'] == r), "--"))
                webRoles = []
                for r in item['webFunctionRoleIds']:
                    webRoles.append(next((i.get('name') for i in wRoles if i['id'] == r), "na"))
                admin = item['isAdmin']
                print(f'{username}\t{fullname}\t{email}\t{enabled}\t{dataRole}\t{funcRoles}\t{webRoles}\t{admin}', file=output)
                if not QUIET:
                    print(f'{username}\t\t{fullname}\t{email}\t\t{enabled}\t\t{dataRole}\t{funcRoles}\t{webRoles}\t{admin}', file=sys.stdout)
            
            if not QUIET:
                print("\n  " + sys.argv[0] + " done.  Check for output in " + OUTPUT_FILE)
        
    except RuntimeError as err:
        print(err.args[0])

    uri = 'https://' + SMC_HOST + '/token'
    response = api_session.delete(uri, timeout=30, verify=False)

# If the login was unsuccessful
else:
    #print("An error has occurred, while logging in, with the following code {}".format(response.status_code))
    print("\n\n   OH NO!!\n   I cannot log in because when I tried the server said:\n")
    raise SystemExit(format(response.status_code))
