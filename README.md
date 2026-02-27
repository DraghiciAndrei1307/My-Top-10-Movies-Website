# My-Top-10-Movies-Website

## Description

This mini-project is a web application (developed using Flask) that creates and uses a SQLite database with SQLAlchemy 
ORM library. The purpose of this page is to let the user create a top 10 best movies ever. 

## Requirements

Before you start using this app, you need to create an account here: https://www.themoviedb.org/

Why you need an account on TMDB? Because you will need to have an 'API Read Access Token'. You will get that token right
after you signed up and accepted their terms of use. You can find the access token if you access Your Profile > 
Settings > API. There you will find the 'API Read Access Token'.  

## How to use

After you git cloned the repo locally on your working station/server, create yourself a virtual environment (.venv) and 
run the following command in the terminal, in order to install all the Python3 needed packages:

```commandline
python3 -m pip install -r requirements.txt
```

After you installed the required packages, go to main.py script and edit the ACCESS_TOKEN variable with the 'API Read 
Access Token' you obtained from the TMDB official website. 

To run the application, you need to open the required firewall ports (default port needed here is 5000) and then run 
the app by using the following command:

```commandline
python3 main.py
```

## About the development process of the app



