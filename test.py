import webshrinker
ws = webshrinker.Categories("<access key>", "<secret key>")

# this will list all the possible categories a website, URL, or IP address can be in
try:
    response = ws.list()
    if response["success"] == True:
        print response["categories"]
    else:
        print response["error"]
except webshrinker.RequestException as e:
    # an error happened while making the request (possible DNS or connection timeout issue)
    raise
except webshrinker.ResponseException as e:
    # a general error happened while receiving the response
    raise
except webshrinker.UnauthorizedException as e:
    # the API access or secret key used is invalid
    raise
except webshrinker.RequestLimitException as e:
    # the account reached its request limit
    raise

# this will lookup the categories for the URL: https://www.webshrinker.com
try:
    response = ws.lookup("https://www.webshrinker.com")
    if response["success"] == True:
        print response["categories"]
    else:
        print response["error"]
except webshrinker.RequestException as e:
    # an error happened while making the request (possible DNS or connection timeout issue)
    raise
except webshrinker.ResponseException as e:
    # a general error happened while receiving the response
    raise
except webshrinker.UnauthorizedException as e:
    # the API access or secret key used is invalid
    raise
except webshrinker.RequestLimitException as e:
    # the account reached its request limit
    raise

