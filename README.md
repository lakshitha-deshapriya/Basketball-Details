# Monitor Basketball league status


## Technologies used
* [Django](https://www.djangoproject.com) -> 4.1.3
* [Python](https://www.python.org) -> 3.11.0
* [sqlite](https://www.sqlite.org/index.html)
* [git](https://git-scm.com)


## SetUp
Run following commands after installation of python and initialization of python virtual environment in the project directory
```
  pip install -r requirements.txt
  python manage.py migrate
  python manage.py generate_data

```

## Notes
Authentication is enabled. Therefore when testing with postman, need to specify username and password using Basic Auth functionality in Authorization tab. Username and passwords are as follows for three types of users.

```
• Admin
  • username: admin
  • password: password

• Coach
  • username: <team name>_coach   eg: team_1_coach
  • password: coach
  
• Player
  • username: <team name>_player<player number>   eg: team_1_player1
  • password: player
```
  
## Endpoints 

```
• Admin : 
  • http://127.0.0.1:8000/auth

• User Details:
  • GET   : http://127.0.0.1:8000/user/         -> Get user list
  • POST  : http://127.0.0.1:8000/user/         -> Create user
  • GET   : http://127.0.0.1:8000/user/<id>     -> Get user
  • PUT   : http://127.0.0.1:8000/user/<id>     -> Edit User
  • DELETE: http://127.0.0.1:8000/user/<id>     -> Delete User
  
• Coach Details:
  • GET   : http://127.0.0.1:8000/coach/        -> Get coach list
  • POST  : http://127.0.0.1:8000/coach/        -> Create coach
  • GET   : http://127.0.0.1:8000/coach/<id>    -> Get coach
  • PUT   : http://127.0.0.1:8000/coach/<id>    -> Edit coach
  • DELETE: http://127.0.0.1:8000/coach/<id>    -> Delete coach
  
• Player Details:
  • GET   : http://127.0.0.1:8000/player/       -> Get player list
  • POST  : http://127.0.0.1:8000/player/       -> Create player
  • GET   : http://127.0.0.1:8000/player/<id>   -> Get player with stats
  • PUT   : http://127.0.0.1:8000/player/<id>   -> Edit player
  • DELETE: http://127.0.0.1:8000/player/<id>   -> Delete player

• Team Details:
  • GET   : http://127.0.0.1:8000/team/                         -> Get team list
  • POST  : http://127.0.0.1:8000/team/                         -> Create team
  • GET   : http://127.0.0.1:8000/team/<id>                     -> Get team details with team player stats
  • GET   : http://127.0.0.1:8000/team/<id>?filterPlayers=true  -> Get team details with 90th percentile player stats
  • PUT   : http://127.0.0.1:8000/team/<id>                     -> Edit team
  • DELETE: http://127.0.0.1:8000/team/<id>                     -> Delete team

```
