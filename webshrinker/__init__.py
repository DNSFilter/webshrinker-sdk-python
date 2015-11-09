import sys
import requests
import base64
import md5

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

    def signed_url(self, method, parameter=None):
        url_part1 = "%s/%s/%s/key:%s" % (self.request_type, self.request_version, method, self.request_headers["x-api-key"])

        url_part2 = ""
        if parameter != None:
            url_part2 = "/%s" % parameter

        to_hash = "%s%s%s" % (self.request_headers["x-api-secret"], url_part1, url_part2)
        hash = md5.new(to_hash).hexdigest()

        url = "%s/%s/hash:%s%s" % (self.end_point, url_part1, hash, url_part2)

        return url

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

        try:
            response = session.get(url, headers=self.request_headers, verify=self.verify_ssl, timeout=self.request_timeout)
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, 
                requests.exceptions.Timeout, requests.exceptions.TooManyRedirects) as e:
                raise RequestException(e.message)            

        return response

    def request_image(self, method, parameter=None):
        response = self.request(method, parameter)

        if response.status_code == 200:
            if not "content-type" in response.headers:
                raise ResponseException(response, {"error": "The content-type header is missing"})

            if response.headers["content-type"] != "image/png":
                raise ResponseException(response, {
                    "error": "Expected image/png data as a response but received '%s'" % response.headers["content-type"]
                })

            data = {
                "success": True,
                "image": base64.b64encode(response.content)
            }

            if "thumbnail-state" in response.headers:
                data["state"] = response.headers["thumbnail-state"]
            if "last-modified" in response.headers:
                data["modified"] = response.headers["last-modified"]

            return data
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
    def __init__(self, data={}):
        message = "Bad or missing API key, x-api-key, or x-api-secret HTTP headers"

        if "error" in data:
            message = data["error"]

        super(self.__class__, self).__init__(message)

class RequestLimitException(Exception):
    def __init__(self, data={}):
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

        data = self.request_json("list")

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
        data = self.request_json("lookup", base64_parameter)

        result = default_data.copy()
        result.update(data)
        return result
        
class Thumbnails(WebShrinker):
    base64_url = False

    def __init__(self, accesskey, secretkey):
        super(self.__class__, self).__init__(accesskey, secretkey)
        self.request_type = "thumbnails"
        self.request_version = "v2"

    def image(self, url=None, size="xlarge", refresh=False):
        default_data = {
            "success": False,
            "image": None,
            "state": "ERROR",
            "modified": 0
        }

        if not url:
            raise RequestException("The 'url' parameter is required")

        parameters = "size:%s" % size

        if refresh != False:
            parameters = "%s/refresh:1" % parameters

        if self.base64_url:
            url = base64.b64encode(url)

        parameters = "%s/url:%s" % (parameters, url)

        default_data["url"] = self.signed_url("image", parameters)

        data = self.request_image("image", parameters)
        result = default_data.copy()
        result.update(data)

        return result
