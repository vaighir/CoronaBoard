# CoronaBoard

### Background
It is a one-person university project created with Flask and is completely dockerized. The idea was to create a blackboard for people to communicate during the corona crisis - ask for help with groceries and dog walking while locked under quarantine. Additionally, the user can see a handful of current statistics from John Hopkins University.

### How to use
Start with `docker-compose up`

Open on port `5000`

Log in the top right corner.
New users can be created with the `register` link in top right corner.
Most functionalities (creating new posts, commenting and viewing users' profiles is restricted to logged in users). Only admin can view a list of all users.
Admin user can log in with `admin` username and `password` password, and the default user with `user1` username and `password` password.

Covid19 information comes from https://covid19api.com/ . Due to limited daily access can be used only sparingly.
