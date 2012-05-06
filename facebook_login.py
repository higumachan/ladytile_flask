from functools import wraps
from settings import *
import Facebook
from flask import *

def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwards):
        facebook = Facebook.Facebook(API_KEY, SECRET_KEY);
        api = None;
        if (request.cookies.has_key("access_token") == True):
            api = facebook.getAPI(request.cookies["access_token"]);
        else:
            result = make_response(redirect(facebook.get_access_token_url(APP_URL + "/callback", PERMISSIONS)));
            return (result);
        kwards["api"] = api;

        return func(*args, **kwards);
    return wrapper;

def recommend_login(func):
    @wraps(func)
    def wrapper(*args, **kwards):
        facebook = Facebook.Facebook(API_KEY, SECRET_KEY);
        api = None;
        if (request.cookies.has_key("access_token") == True):
            api = facebook.getAPI(request.cookies["access_token"]);
        kwards["api"] = api;

        return func(*args, **kwards);
    return wrapper;

