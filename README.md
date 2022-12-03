# CPSC-449-Web Backend Engineering:Project-3
# Project Members:

1. Apurva Umakant Gawande
2. Gage Glovanni
3. Gowtham Kishore Mahadasu
4. Sravani Kallempudi

# Project description: 

In this project, we are creating three replicas of the database which are named primary, secondary 1 and secondary 2. We are then configuring our game service such that the reads are distributed across the three replicas while writes continue to go to the primary database. We have created a new RESTful microservice to maintain a leaderboard for Wordle games.

## Configuration files:
1. Procfile is a mechanism for declaring what commands are run by your application to start the app 
2. Update the nginx.config into default file present in /etc/nginx/sites-enabled

## The following are the steps to run the project:
1. Installing and configuring Nginx:
```bash
sudo apt update
sudo apt install --yes nginx-extras
```
2. Clone the github repository:
```bash
git clone https://github.com/plo8/cpsc449-project2.git
```
3. Then cd into the cpsc449-project2 folder and run the following commands:
```bash
cd cpsc449-project2/
mkdir var
```
4. Start the services
```bash
foreman start 
```
5. Run both the init scripts to populate the database and automatically connect the api to the database. 
```bash
./bin/init_auth.sh    
./bin/init_game.sh
```
Now the API can be run using Postman(the method which we followed) or using curl or httpie.

## ENDPOINT 1:
For registering an user: @app.route("/register", methods=["POST"])
```bash
http POST http://tuffix-vm/register/ username=Rain password=rain@123
```
## ENDPOINT 2:
For authenticating the user:@app.route("/auth", methods=["GET"])
```bash
Ex: On postman with Basic-Auth: http://tuffix-vm/auth
```
## ENDPOINT 3: 
For creating a new game for an authenticated user:@app.route("/game/", methods=["POST"])
```bash
Ex: On postman with Basic-Auth: http://tuffix-vm/game
```
## ENDPOINT 4:
For getting the game state of the authenticated user:@app.route("/game/:gameId", methods=["GET"])
```bash
Ex: On postman with Basic-Auth: http://tuffix-vm/game/:gameId
``` 
## ENDPOINT 5:
List all the games for the authenticated user:@app.route("/my-games", methods=["GET"])
```bash
Ex: On postman with Basic-Auth: http://tuffix-vm/my-games  
```
## ENDPOINT 6:
Guessing a word: @app.route("/game/:gameId", methods=["PATCH"])
```bash
Ex: On postman with Basic-Auth: http://tuffix-vm/game/:gameId
note: In the body, select raw - JSON and then {"word":"apple"}
```
