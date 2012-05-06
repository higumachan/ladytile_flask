# -*- coding: utf-8 -*-

from flask import *
import urllib
import urllib2
import Facebook
from facebook_login import *
import pymongo
from settings import *

app = Flask(__name__);

db = pymongo.Connection().ladytile;

@app.before_request
def before_request():
    g.conn = pymongo.Connection();
    g.db = g.conn.ladytile; 
    print "request_start";

@app.teardown_request
def teardown_request():
    g.conn.disconnect();
    g.db = None;
    print "request_end"

@app.route("/")
@require_login
def index(api):
    """
    token = api.oauth2_token;
    post_data = {};
    post_data["access_token"] = token;
    pd = urllib.urlencode(post_data);
    s = urllib2.urlopen('https://graph.facebook.com/me?access_token=%s' % token).read();
    """
    s = api.me();
    return (s);

@app.route("/post")
@require_login
def post(api):
    
    s = api.post_feed(picture="http://thumbnail.image.rakuten.co.jp/@0_mall/sellishop/cabinet/os2012/oos-9729-m.jpg?_ex=256x256");

    return (s);

@app.route("/cute", methods=["POST"])
@require_login
def cute(api):
    id = request.form["id"];
    user = g.db.user.find_one({"access_token": api.access_token});
    pict = g.db.tile.find_one({"_id": id, "cute": {"$ne": user["_id"]}});
    pict.cute.append(api.user["id"]);
    pict.cute_count += 1;
    g.db.tile.save(pict);
    user.fav.append(pict["_id"]);
    g.db.user.save(user);
    api.post_feed(picture=pict["image_url"]);

    return ("OK");

@app.route("/click_image/<int:tile_id>")
@recommend_login
def click_image(tile_id, api=None):
    tile = g.db.tile.find_one({"_id": tile_id});
    log = {"tile": tile, "time": datetime.datetime.now()};
    if (api != None):
        user = g.db.user.find_one({"access_token": api.access_token});
        log["user"] = user;
    g.db.click_log.insert(log);

    return (redirect(tile.url));


@app.route("/get-lady/<genre>/<int:page>")
def get_lady(genre, page):
    result = g.db.tile.find({"genre": genre}).sort("_id", pymongo.DESCENDING).limit(20).skip(page * 20);
    
    return (json.dumps(list(result)));

@app.route("/callback")
def callback():
    code = request.args["code"];
    fb = Facebook.Facebook(API_KEY, SECRET_KEY);
    access_token = fb.get_access_token(APP_URL + "/callback", code);

    api = fb.getAPI();
    me = api.me();
    user = g.db.user.find_one({"_id": me["id"]});
    if (user == None):
        user = {"_id": me["id"], "name": me["name"], "gender": me["gender"], "birth_day": me["birth_day"], "access_token": access_token, "fav": []};
    g.db.save(user);
    result = make_response(redirect("/"));
    result.set_cookie("access_token", access_token);
    return (result);

if __name__ == "__main__":
    app.debug = True;
    app.run();

