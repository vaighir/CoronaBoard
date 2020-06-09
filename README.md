# CoronaBoard

### Background
It is a one-person university project created with Flask and completely dockerized. The idea was to create a blackboard for people to communicate during the corona crisis - ask for help with groceries and dog walking while locked under quarantine. Additionaly, the user can see a handful of current statistics from John Hopkins University.

### How to use
Start with `docker-compose up`

Open on port `5000`

Log in the top right corner.
New users can be created with the `register` link in top right corner.
Most functionalities (creating new posts, commenting and viewing users' profiles is restricted to logged in users). Only admin can view a list of all users.

