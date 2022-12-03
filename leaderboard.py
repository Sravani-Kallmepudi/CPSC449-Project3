from quart import Quart, g, request, jsonify, abort
from quart_schema import validate_request, RequestSchemaValidationError, QuartSchema
import toml
import redis
import json

app = Quart(__name__)
QuartSchema(app)

r = redis.Redis()
r.flushall

@app.errorhandler(400)
def badRequest(e):
    return {"error": str(e).split(':', 1)[1][1:]}, 400

# ---------------REPORT A GAME---------------

@app.route("/reportgame/<string:username> <int:result> <int:guesses>", methods=["POST"])
async def addScore(username, result, guesses):
    if r.hexists(username, "total") == False:
        r.hmset(username, {"total":0, "count":0})

    score = (7 - guesses) if (result == 1) else 0
    total = r.hincrby(username, "total", score)
    count = r.hincrby(username, "count", 1)
    average = total/count

    r.zadd("leaderboard", {username:average})
    return {"message": "game successfully reported", "updated_average": average},200


# ---------------GET LEADERBOARD TOP 10---------------

@app.route("/leaderboard", methods=["GET"])
async def getTopTen():
    return r.zrange("leaderboard", 0, 9, withscores=True, desc=True),200


# ---------------RESET LEADERBOARD DATABASES---------------

@app.route("/resetleaderboard", methods=["POST"])
async def clearLeaderboard():
    r.flushall()
    return {"message": "leaderboard reset"},200