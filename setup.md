# Project Setup Guide

### requirements
- python3.7 or higher
- pipenv 
  - Get it by running
  
    -`pip install pipenv`

### Starting
##### 1.Cloning the repo
- Clone the repo or fork it and then clone from your profile.
- Cd into **rewrite**
- Create a new branch by doing the following:

  - `git checkout -b branch_name`
##### 2.Pipenv and migrations
- Go to directory where the pipfile is and run 

  -`pipenv install`
- Activate pipenv by doing 

  -`pipenv shell`
  
##### 4.Env vars
- Go into the folder **rewrite** create a file called **config.yaml**
- Copy everything from **config.yaml.example** into your **config.yaml**.
- Replace the token value with your own bot token and you can change the prefix according to your comforts.
  
##### 5.Running the bot
- Go into the folder **rewrite** and open up you terminal/cmd.
- Activate pipenv by running

  -`pipenv shell`
- run the bot by using

  -`pipenv run start`
