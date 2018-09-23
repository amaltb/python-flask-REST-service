## Python web application using flask framework

This is an example web application written in python using flask micro web framework. This application also shows 
**_twitter oAuth2_** for authentication purposes. This app also enables user to query tweets based on any topic of interest 
and does a sentiment analysis on the tweets before displaying it out on a web page.


### How to install
For using this application, just download it and execute following command to start the web application.
Also this application uses postgres sql as the backend database. See the database folder to get the ER diagram and 
schema SQLs.
```
unzip <project.zip>
cd <project directoy>/python-flask-webapp
python web-app.py
Go to 127.0.0.1:4995 or localhost:4995 in any of the web browser of your choice
```

#### REST API signature 

```
(GET, POST)

/
/profile
/search
/login/twitter
/auth/twitter
/logout
```  