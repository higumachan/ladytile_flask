import pit

fb = pit.Pit().get("facebook_test");

API_KEY = fb["key"]
SECRET_KEY = fb["secret"];

APP_URL = "http://localhost:5000"
PERMISSIONS = ("user_about_me", "user_birthday", "publish_stream", "offline_access");

