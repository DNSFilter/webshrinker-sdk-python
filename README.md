This SDK provides the python libraries needed to make use of the [Web Shrinker](https://www.webshrinker.com) API services.

## APIs Exposed

* Website Categorization API functions (v1)

## Features

* Supports keep-alive to speed up multiple requests
* Throws meaningful exceptions to aid debugging

## Installing

The best way to install is by using pip:

```bash
$ pip install webshrinker
```

The SDK also depends on the "requests" package which should be installed by pip automatically.

### Making Requests

Here is an example categorization request, just replace the &lt;access key&gt; and &lt;secret key&gt; placeholders with your actual account keys.
You can find and create access keys via the [Account Dashboard](https://dashboard.webshrinker.com).

```python
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
```

### Options

* set_keep_alive(True|False): Enable/disable the use of session in the requests module which supports keep-alive (default: True)
* set_verify_ssl(True|False): Enable/disable the verification of the SSL endpoint (default: True)
* set_timeout(seconds): Sets the amount of time to wait for an API connection before raising an exception (default: 10 seconds)
