import webshrinker

access_key = "your-API-access-key"
secret_key = "your-API-secret-key"

url = "https://www.webshrinker.com"

###################################
# Thumbnail / Screenshot examples #
###################################

ws = webshrinker.Thumbnails(access_key, secret_key)
ws.debug = True

# this will return information about the thumbnail image for the URL: https://www.webshrinker.com
try:
    print "Running ws.image() ..."
    response = ws.image(url)
    # the response variable contains the PNG image data
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

print "\n"

# this will return information about the thumbnail image for the URL: https://www.webshrinker.com
try:
    print "Running ws.info() ..."
    response = ws.info(url)
    print response
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

print "\n"

####################################
# Website Category Lookup examples #
####################################

ws = webshrinker.Categories(access_key, secret_key)

# this will list all the possible categories a website, URL, or IP address can be in
try:
    print "Running ws.list() ..."
    response = ws.list()
    print response
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

print "\n"

# this will lookup the categories for the URL: https://www.webshrinker.com
try:
    print "Running ws.lookup() ..."
    response = ws.lookup(url)
    print response

    if response["categorizing"] == True:
        print "** The URL is still being categorized, check back again soon **"
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