import http.client, json, os, sys, urllib
import re
import random, urllib.request

# Hostname of your ShareCare application
host = "sharecare.tipuric.com"

# Number of WebSite tests
WEBSITE_TEST_COUNT = 50

# Number of API tests
API_TEST_COUNT = 50

# Keep every N-th user/charity/post/media in the database
KEEP_SOME_DATA = False
N_TO_KEEP = 2

######################################
#######  Supporting functions  #######
######################################

def CallWebSite (host=None, path="/"):
    try:            
        response = urllib.request.urlopen('http://' + host + path)
        print(response.getcode())
    except Exception as ex:
        print(ex)
        raise ex

def CallAPI (method="GET", host=None, function=None, headers=None, body=None):
        
    request_path = "/{0}".format(function)
    
    try:
        conn = http.client.HTTPConnection(host)        
        conn.request(method, request_path, body, headers)        
        response = conn.getresponse()        
        data = response.read().decode("UTF-8")
        print(request_path, body, headers, method)
        result = None
        if len(data) > 0:
            result = json.loads(data)

        print(result)
        return result
    except Exception as ex:
        print(ex)
        raise ex

def AddCharity (name=None, description=None, createdByUser=None, funds=None):
    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        "name": name,
        "description": description,
        "createdByUser": createdByUser,
        "funds": funds
    }
    
    result = CallAPI(method="POST", host=host, function="charities", headers=headers, body = json.dumps(body))

    charityId = 0
    
    if (result != None):
        charityId = result['id']
        print(json.dumps(result, sort_keys=True, indent=2))

    return charityId

def GetCharityById (charityId=None):
    headers = {
        'Content-Type': 'application/json',
    }  

    result = CallAPI(method="GET", host=host, function="charities/{0}".format(charityId), headers=headers, body = None)

    if (result != None):        
        print(json.dumps(result, sort_keys=True, indent=2))

def DeleteCharityById (charityId=None):
    headers = {
        'Content-Type': 'application/json'
    }

    result = CallAPI(method="DELETE", host=host, function="charities/{0}".format(charityId), headers=headers, body = None)
    
    if (result != None):
        print(json.dumps(result, sort_keys=True, indent=2))

def AddPost (charityId, userId, mediaId, description, funds, charityName=None, userName=None):
    headers = {
        'Content-Type': 'application/json'
    }
    
    body = {
        "charityId": charityId,
        "userId": userId,
        "mediaId": mediaId,
        "description": description,
        "funds": funds,
        "charityName": charityName,
        "userName": userName
    }
    
    result = CallAPI(method="POST", host=host, function="posts", headers=headers, body = json.dumps(body))

    postId = 0
    
    if (result != None):
        postId = result['id']
        print(json.dumps(result, sort_keys=True, indent=2))

    return postId

def DeletePostById (postId=None):
    headers = {
        'Content-Type': 'application/json'
    }

    result = CallAPI(method="DELETE", host=host, function="posts/{0}".format(postId), headers=headers, body=None)
    
    if (result != None):
        print(json.dumps(result, sort_keys=True, indent=2))

def AddUser (firstName, lastName, eMail, password, age=None):
    headers = {
        'Content-Type': 'application/json'
    }

    body = {
        "firstName": firstName,
        "lastName": lastName,
        "eMail": eMail,
        "password": password,
        "age": age
    }
    
    result = CallAPI(method="POST", host=host, function="users", headers=headers, body = json.dumps(body))

    userId = 0
    
    if (result != None):
        userId = result['id']
        print(json.dumps(result, sort_keys=True, indent=2))

    return userId

def GetUserById (userId=None):
    headers = {
        'Content-Type': 'application/json',
    }  

    result = CallAPI(method="GET", host=host, function="users/{0}".format(userId), headers=headers, body = None)

    if (result != None):        
        print(json.dumps(result, sort_keys=True, indent=2))

def DeleteUserById (userId=None):
    headers = {
        'Content-Type': 'application/json'
    }

    result = CallAPI(method="DELETE", host=host, function="users/{0}".format(userId), headers=headers, body = None)
    
    if (result != None):
        print(json.dumps(result, sort_keys=True, indent=2))

def AddMedia (url):
    headers = {
        'Content-Type': 'application/json'
    }

    body = {
        "url": url
    }
    
    result = CallAPI(method="POST", host=host, function="media", headers=headers, body = json.dumps(body))

    userId = 0
    
    if (result != None):
        userId = result['id']
        print(json.dumps(result, sort_keys=True, indent=2))

    return userId

def GetMediaById (mediaId=None):
    headers = {
        'Content-Type': 'application/json',
    }  

    result = CallAPI(method="GET", host=host, function="media/{0}".format(mediaId), headers=headers, body = None)

    if (result != None):        
        print(json.dumps(result, sort_keys=True, indent=2))

def DeleteMediaById (mediaId=None):
    headers = {
        'Content-Type': 'application/json'
    }

    result = CallAPI(method="DELETE", host=host, function="media/{0}".format(mediaId), headers=headers, body = None)
    
    if (result != None):
        print(json.dumps(result, sort_keys=True, indent=2))

#######################################
######  Main simulator function  ######
#######################################

# Load Testing the Web Site
print("Load Testing the Web Site...")

for i in range(0, WEBSITE_TEST_COUNT):
    CallWebSite(host)

# Load Testing the Web Site
print("Load Testing the API...")

for i in range(0, API_TEST_COUNT):
    
    charityId = AddCharity(name="Test Charity", description="Test Charity", 
        createdByUser="jackson.mall@pci.com", funds=100)
    GetCharityById(charityId)

    postId = AddPost(charityId=1, userId=1, mediaId=1, description="Test Post", 
        funds=100, charityName="Test Charity", userName="Mark Povich")
    CallWebSite(host, "/posts")

    userId = AddUser(firstName="Test", lastName="User", eMail="test@user.com", 
        password="test", age=25)
    GetUserById(userId)

    mediaId = AddMedia(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    GetMediaById(mediaId)

    # Delete every N-th Charity/Post/User/Media
    if (i % N_TO_KEEP or not KEEP_SOME_DATA):
        DeleteCharityById(charityId)
        DeletePostById(postId)
        DeleteUserById(userId)
        DeleteMediaById(mediaId)