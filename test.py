import webshrinker
ws = webshrinker.Thumbnails("uMLcIVMUIL47YmrImRXV", "Skihd030jfyVNPsz3qYJ")
ws.debug = True
ws.end_point = "http://api.app"

# this will list all the possible categories a website, URL, or IP address can be in
try:
    response = ws.image("https://www.webshrinker.com", size="1000000000000000000000x100")
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
