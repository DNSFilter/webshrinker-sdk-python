import sys
import requests
import base64
import hashlib

class WebShrinker(object):
    end_point = "https://api.webshrinker.com"
    request_type = "unknown"
    request_version = "v2"
    request_headers = {
        "user-agent": "webshrinker-python/2.0"
    }
    request_timeout = 10

    debug = False
    session = None
    use_keepalive = True
    verify_ssl = True
    disable_old_python_warnings = True

    access_key = ""
    secret_key = ""

    def __init__(self, access_key, secret_key):
        self.set_access_key(access_key)
        self.set_secret_key(secret_key)

        # If running on Python < 2.7.9 the requests/urllib3 libraries display warnings about possibly insecure SSL connections,
        # best option is to upgrade to Python >= 2.7.9
        if (self.disable_old_python_warnings):
            if (sys.version_info[0] == 2 and sys.version_info[1] == 7) and sys.version_info[2] < 9:
                requests.packages.urllib3.disable_warnings()

    def set_access_key(self, access_key):
        self.access_key = access_key

    def set_secret_key(self, secret_key):
        self.secret_key = secret_key

    def set_end_point(self, end_point):
        self.end_point = end_point

    def set_version(self, version):
        self.request_version = version

    def set_keep_alive(self, keepalive):
        self.use_keepalive = keepalive

    def set_verify_ssl(self, verify_ssl):
        self.verify_ssl = verify_ssl

    def set_timeout(self, timeout):
        self.request_timeout = timeout

    def signed_url(self, method, parameters=None):
        if parameters == None:
            parameters = {}

        parameters["key"] = self.access_key

        url = "%s/%s" % (self.request_type, self.request_version)

        if method != None:
            url = "%s/%s" % (url, method)

        query = ""
        for key, value in parameters.items():
            if query == "":
                query = "%s=%s" % (key, value)
            else:
                query = "%s&%s=%s" % (query, key, value)

        url = "%s?%s" % (url, query)
        to_hash = "%s:%s" % (self.secret_key, url)
        hash = hashlib.md5(to_hash).hexdigest()
        url = "%s/%s&hash=%s" % (self.end_point, url, hash)

        return url

    def request(self, method, parameters=None):
        session = requests

        if self.use_keepalive:
            if self.session == None:
                self.session = requests.Session()
            session = self.session

        url = self.signed_url(method, parameters)

        if self.debug:
            print "Requesting: " + url

        try:
            response = session.get(url, headers=self.request_headers, verify=self.verify_ssl, timeout=self.request_timeout)
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, 
                requests.exceptions.Timeout, requests.exceptions.TooManyRedirects) as e:
                raise RequestException(e.message)            

        return response

    def request_image(self, method, parameters=None):
        response = self.request(method, parameters)

        if response.status_code == 200 or response.status_code == 202:
            if not "content-type" in response.headers:
                raise ResponseException(response, error="The content-type header is missing")

            if response.headers["content-type"] != "image/png":
                raise ResponseException(response, error="Expected image/png data as a response but received '%s'" % response.headers["content-type"])

            return response, response.content
        elif response.status_code == 400:
            raise RequestException("One or more parameters in the request URL are invalid")
        elif response.status_code == 401:
            raise UnauthorizedException()
        elif response.status_code == 402:
            raise RequestLimitException()
        else:
            raise ResponseException(response)

    def request_json(self, method, parameter=None):
        response = self.request(method, parameter)
        data = response.json()

        if response.status_code == 200 or response.status_code == 202:
            if self.debug:
                if response.headers["content-type"] != "application/json":
                    print "Warning: expected content type 'application/json', got '%s'" % response.headers["content-type"]

            return response, data["data"][0]
        elif response.status_code == 400:
            raise RequestException(data["error"]["message"])
        elif response.status_code == 401:
            raise UnauthorizedException(data["error"]["message"])
        elif response.status_code == 402:
            raise RequestLimitException(data["error"]["message"])
        else:
            raise ResponseException(response, data["error"]["message"])

class RequestException(Exception):
    def __init__(self, message):
        super(self.__class__, self).__init__(message)

class ResponseException(Exception):
    def __init__(self, response, error=""):
        message = ""

        if "status_code" in response:
            message = "Error %d: " % response.status_code

        if error != "":
            message += error

        super(self.__class__, self).__init__(message)

class UnauthorizedException(Exception):
    def __init__(self, error=""):
        message = "Bad or missing API key, x-api-key, or x-api-secret HTTP headers"

        if error != "":
            message = error

        super(self.__class__, self).__init__(message)

class RequestLimitException(Exception):
    def __init__(self, error=""):
        message = "Account request limit reached - purchase additional requests through the account dashboard"

        if error != "":
            message = error

        super(self.__class__, self).__init__(message)

class Categories(WebShrinker):
    def __init__(self, accesskey, secretkey):
        super(self.__class__, self).__init__(accesskey, secretkey)
        self.request_type = "categories"
        self.request_version = "v2"

    def list(self):
        (response, result) = self.request_json(None)

        return result

    def lookup(self, uri):
        url = base64.b64encode(uri)
        (response, result) = self.request_json(url)

        result["categorizing"] = False
        if response.status_code == 202:
            result["categorizing"] = True

        return result
        
class Thumbnails(WebShrinker):
    def __init__(self, accesskey, secretkey):
        super(self.__class__, self).__init__(accesskey, secretkey)
        self.request_type = "thumbnails"
        self.request_version = "v2"

    def image(self, url=None, size="xlarge", refresh=False, expires=False, fullpage=False):
        if not url:
            raise RequestException("The 'url' parameter is required")

        url = base64.b64encode(url)

        parameters = { 
            "size" : size
        }

        if refresh != False:
            parameters["refresh"] = 1

        if expires != False:
            parameters["expires"] = int(expires)

        if fullpage != False:
            parameters["fullpage"] = 1

        (response, result) = self.request_image(url, parameters)

        return result

    def info(self, url=None, size="xlarge", refresh=False, expires=False, fullpage=False):
        if not url:
            raise RequestException("The 'url' parameter is required")

        url = "%s/info" % base64.b64encode(url)

        parameters = { 
            "size" : size
        }

        if refresh != False:
            parameters["refresh"] = 1

        if expires != False:
            parameters["expires"] = int(expires)

        if fullpage != False:
            parameters["fullpage"] = 1

        (response, result) = self.request_json(url, parameters)

        return result
