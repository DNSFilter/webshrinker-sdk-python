This SDK provides the python libraries needed to make use of the [Web Shrinker](https://www.webshrinker.com) API services.

## APIs Exposed

* Website Thumbnail / Screenshots API functions (v2)
* Website Category Lookup API functions (v2)

## Features

* Supports keep-alive to speed up multiple requests
* Throws meaningful exceptions to aid debugging

## Installing

The best way to install is by using pip:

```bash
$ pip install webshrinker
```

The SDK also depends on the "requests" package which should be installed by pip automatically.

### Making Category Lookup Requests

Here is an example categorization request, just replace the &lt;access key&gt; and &lt;secret key&gt; placeholders with your actual account keys.
You can find and create access keys via the [Account Dashboard](https://dashboard.webshrinker.com). Additional information can be found on the [Website Categorization API v2 Reference](http://docs.webshrinker.com/website-url-categorization-api/v2/index.html).

```python
import webshrinker

ws = webshrinker.Categories("<access key>", "<secret key>")

# this will list all the possible categories a website, URL, or IP address can be in
try:
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

# this will lookup the categories for the URL: https://www.webshrinker.com
try:
    response = ws.lookup("https://www.webshrinker.com")
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
```

### Making Thumbnail / Screenshot Requests

Here is an example categorization request, just replace the &lt;access key&gt; and &lt;secret key&gt; placeholders with your actual account keys.
You can find and create access keys via the [Account Dashboard](https://dashboard.webshrinker.com). Additional information can be found on the [Thumbnail API v2 Reference](http://docs.webshrinker.com/thumbnail-api/v2/index.html).

```python
import webshrinker

ws = webshrinker.Thumbnails("<access key>", "<secret key>")

# this will fetch the thumbnail image for a URL as PNG binary data
try:
    response = ws.image("https://www.webshrinker.com")
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

# this will return information about the thumbnail image for the URL: https://www.webshrinker.com
try:
    response = ws.info("https://www.webshrinker.com")
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
```

### Options

* set_keep_alive(True|False): Enable/disable the use of session in the requests module which supports keep-alive (default: True)
* set_verify_ssl(True|False): Enable/disable the verification of the SSL endpoint (default: True)
* set_timeout(seconds): Sets the amount of time to wait for an API connection before raising an exception (default: 10 seconds)
