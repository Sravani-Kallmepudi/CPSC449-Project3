from quart import Quart, g, request, jsonify, abort
from quart_schema import validate_request, RequestSchemaValidationError, QuartSchema
import toml
import redis
import json
import httpx

app = Quart(__name__)
QuartSchema(app)

r = redis.Redis()
r.flushall

@app.errorhandler(400)
def badRequest(e):
    return {"error": str(e).split(':', 1)[1][1:]}, 400

# ---------------REPORT A GAME---------------

@app.route("/reportgame", methods=["POST"])
async def addScore():
    body = await request.get_json()
    username = body.get("username").lower()
    result = body.get("result")
    guesses = body.get("guesses")

    if r.hexists(username, "total") == False:
        r.hmset(username, {"total":0, "count":0})

    score = (7 - guesses) if (result == 1) else 0
    total = r.hincrby(username, "total", score)
    count = r.hincrby(username, "count", 1)
    average = total/count

    r.zadd("leaderboard", {username:average})
    return {"score": score, "updated_average": average},200


# ---------------GET LEADERBOARD TOP 10---------------

@app.route("/leaderboard", methods=["GET"])
async def getTopTen():
    lb = r.zrange("leaderboard", 0, 9, withscores=True, desc=True)
    lbdict = dict((i[0].decode("utf-8"),i[1]) for i in lb)
    return lbdict,200


# ---------------RESET LEADERBOARD DATABASES---------------

@app.route("/resetleaderboard", methods=["POST"])
async def clearLeaderboard():
    r.flushall()
    return {"message": "leaderboard reset"},200
 
    
# ---------------REGISTER TO GET SCORE UPDATES---------------

@app.route("/scoreupdates", methods=["POST"])
async def getScoreUpdate():
    body = await request.get_json()
    URL = body.get("URL")

    auth = request.authorization
    if not(auth):
        abort(401, "Please provide the username")
    username = auth.username
    httpx.post('http://127.0.0.1:5100/game/updates', json={"URL":URL, "username":username})

    # while registering send callback URL
    #You can construct the callback URL from the PORT environment variable and socket.getfqdn().
    # send http req to game service using httpx and send URL
    
    return {"message": "registered for score updates successfully!!"}, 200

#@app.route("/scoreupdates/reply", methods=["POST"])
#async def scoreResponse():
 #   body = await request.get_data()
  #  data = body.get("data")
   
   # if data == 0:
    #    return {"game update": "Lost"}
    #return {"game update": "Win"}

