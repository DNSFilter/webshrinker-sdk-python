import sys
import requests
import base64

class WebShrinker(object):
    end_point = "https://api.webshrinker.com"
    request_type = "unknown"
    request_version = "v1"
    request_headers = {
        "x-api-key": "no-api-key-set",
        "x-api-secret": "no-api-secret-key-set",
        "user-agent": "webshrinker-python/1.0"
    }
    request_timeout = 10

    debug = False
    session = None
    use_keepalive = True
    verify_ssl = True
    disable_old_python_warnings = True

    def __init__(self, accesskey, secretkey):
        self.set_access_key(accesskey)
        self.set_secret_key(secretkey)

        # If running on Python < 2.7.9 the requests/urllib3 libraries display warnings about possibly insecure SSL connections,
        # best option is to upgrade to Python >= 2.7.9
        if (self.disable_old_python_warnings):
            if (sys.version_info[0] == 2 and sys.version_info[1] == 7) and sys.version_info[2] < 9:
                requests.packages.urllib3.disable_warnings()

    def set_access_key(self, accesskey):
        self.request_headers["x-api-key"] = accesskey

    def set_secret_key(self, secretkey):
        self.request_headers["x-api-secret"] = secretkey

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

    def request(self, method, parameter=None):
        url = "%s/%s/%s/%s" % (self.end_point, self.request_type, self.request_version, method)

        if parameter != None:
            url = "%s/%s" % (url, parameter)

        session = requests

        if self.use_keepalive:
            if self.session == None:
                self.session = requests.Session()
            session = self.session

        if self.debug:
            print "Requesting: " + url

        data = {}
        try:
            response = session.get(url, headers=self.request_headers, verify=self.verify_ssl, timeout=self.request_timeout)
            data = response.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, 
                requests.exceptions.Timeout, requests.exceptions.TooManyRedirects) as e:
                raise RequestException(e.message)            

        if response.status_code == 200:
            if self.debug:
                if response.headers["content-type"] != "application/json":
                    print "Warning: expected content type 'application/json', got '%s'" % response.headers["content-type"]

            # sanity check
            if "success" in data:
                return data

            # if we don't have a 'success' parameter than something went wrong
            if self.debug:
                print "Response error: status code %d, content: %s" % (response.status_code, data)

            data["success"] = False
            if not "error" in data:
                data["error"] = "An unknown error occurred, expected success but found none"
            raise ResponseException(response, data)
        elif response.status_code == 401:
            raise UnauthorizedException(data)
        elif response.status_code == 402:
            raise RequestLimitException(data)
        else:
            raise ResponseException(response, data)

class RequestException(Exception):
    def __init__(self, message):
        super(self.__class__, self).__init__(message)

class ResponseException(Exception):
    def __init__(self, response, data={}):
        message = ""

        if "status_code" in response:
            message = "Error %d: " % response.status_code

        if "error" in data:
            message += data["error"]
        else:
            message += "An unknown error occurred, retry the request again"

        super(self.__class__, self).__init__(message)

class UnauthorizedException(Exception):
    def __init__(self, data):
        message = "Bad or missing API key, x-api-key, or x-api-secret HTTP headers"

        if "error" in data:
            message = data["error"]

        super(self.__class__, self).__init__(message)

class RequestLimitException(Exception):
    def __init__(self, data):
        message = "Account request limit reached - purchase additional requests through the account dashboard"

        if "error" in data:
            message = data["error"]

        super(self.__class__, self).__init__(message)

class Categories(WebShrinker):
    def __init__(self, accesskey, secretkey):
        super(self.__class__, self).__init__(accesskey, secretkey)
        self.request_type = "categories"
        self.request_version = "v1"

    def list(self):
        default_data = {
            "success": False,
            "categories": []
        }

        data = super(self.__class__, self).request("list")

        result = default_data.copy()
        result.update(data)
        return result

    def lookup(self, uri):
        default_data = {
            "success": False,
            "categorizing": False,
            "categories": []
        }

        base64_parameter = base64.b64encode(uri)
        data = super(self.__class__, self).request("lookup", base64_parameter)

        result = default_data.copy()
        result.update(data)
        return result
        

