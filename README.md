# python-tips-aid

## About
python-tips-aid like the name suggests is a mobile friendly python package tailor made to be usable by the owners of 
the python_tips, it periodically syncs the tweets on the @python_tips account in the Database, it also gives the user the priviledge of retweeting particular tweets to his own account after authentication,
it also allows for seamless filtering over the tweets scraped.

It also provides API endpoints that can be easily plugged into a Front End

### How to install
First activate your vitual environment with   `source venv/bin/activate`
- Next   
```python
cd twitter_help
pip install -r requirements.txt
```
- change .env.example to .env and fill in your environment variables
- Now run
```python
python manage.py makemigration 
python manage.py migrate
```
- create a superuser with 
```python 
python manage.py createsuperuser
```

### Creating Social Auth Application (Required Only For the usage of API)
- login to django admin as superuser
- create a social application with following fields
... PROVIDER ----> Twitter
...      Name -----> choose any name e.g TwitterAuth.
...      Client ID -----> Twitter Api Key
...      Secret Key -----> Twitter Secret Key
...      select `example.com` under `available sites` and move to `chosen sites`
...      SAVE the new soical application you have created.

### Run Server
```python 
python manage.py runserver
```

### Run Celery Tasks
- Firstly Make sure you are in **twitter_help** project directory containing the manage.py file
- next open a new terminal with your venv active and in the right directory with manage.py run
```python 
    celery -A twitter_help worker -B -l INFO
```

### CAVEATS (This doesnt affect the API and the API would work just fine without)
for the django website twitter user authentication to function properly, if it wasnt already obvious, you would need to be running an https server which django doesnt support out of the box, however you can use the very handy ngrok.io to listen to port 8000 which django listens to by default. **THEN** you would need to update the website urls on the twitter developer account
#### assuming we use ngrok and our live url is https://db9fe5b84537.ngrok.io
- Callback Url ---> `http://db9fe5b84537.ngrok.io/twitter-auth/cb`
- Website Url ----> `http://db9fe5b84537.ngrok.io`

also change app permissions in developer.twitter dashboard to allow Read/Write Access

### Swagger Docs For the API
Open the Swagger Docs to see the available endpoints
`http://127.0.0.1:8000/api/swagger`

### LIVE URL
`https://pytip-helper.herokuapp.com`   currently without the API integration just plain django web


### API Endpoints

- `api/auth/twitter` ---> POST ----> {
    'access_token': Twitter Access Token, 
    'token_secret': Twitter Access Secret Token
}

- `api/user/favorites` ---> POST ----> {
    'username': twitter username, 
    'tweets_count': number of tweets to be fetched, max is 400
}

- `api/user/mentions` ---> POST ----> {
    'tweets_count': number of tweets to be fetched, max is 400
}

**endpoints under `api/tweets/...` can be found in the swagger docs at `/api/swagger/`**

**github url `https://github.com/shols232/python-tips-aid`**
