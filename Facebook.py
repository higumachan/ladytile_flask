import urllib
import urllib2

API_URL = "https://graph.facebook.com";

class Facebook:
    def __init__(self, app_key, secret_key):
        self._app_key = app_key;
        self._secret_key = secret_key;
        self._api = None;

    def getAPI(self, access_token=None):
        if (self._api == None):
            if (access_token == None):
                self._api = API(self._access_token);
            else:
                self._api = API(access_token);
        return (self._api);
    
    def get_access_token_url(self, callback, permission):
        get_data = {
            "client_id": self._app_key,
            "redirect_uri": callback,
            "scope": ",".join(permission),
        };
        en_data = urllib.urlencode(get_data);

        return ("https://graph.facebook.com/oauth/authorize?" + en_data);

    def get_access_token(self, callback, code):
        post_data = {
            "client_id": self._app_key,
            "redirect_uri": callback,
            "client_secret": self._secret_key,
            "code": code,
        };
        en_data = urllib.urlencode(post_data);
        
        read = urllib2.urlopen("https://graph.facebook.com/oauth/access_token", en_data).read();

        result = read.split("=")[1];
        self._access_token = result;
        return result;
    def set_access_token(self, access_token):
        self._access_token = access_token;

class API:
    def __init__(self, access_token):
        self._access_token = access_token;

    def _bind_api(url, params=[]):
        def func(*args, **kwards):
            access_token = args[0]._access_token;
            post_data = {};
            for param in params:
                if (kwards.has_key(param) == True):
                    post_data[param] = kwards[param];
            en_data = urllib.urlencode(post_data);
            if (post_data == {}):
                result = urllib2.urlopen(API_URL + url + "?access_token=%s" % access_token).read();
            else:
                result = urllib2.urlopen(API_URL + url + "?access_token=%s" % access_token, en_data).read();
            return (result);
        return (func);
    
    me = _bind_api("/me");
    feed = _bind_api("/feed");
    post_feed = _bind_api("/feed", ["message", "link", "picture"]);

