# python-tips-aid



## About
python-tips-aid like the name suggests is a mobile friendly python package tailor made to be usable by the owners of 
the python_tips, it periodically syncs the tweets on the @python_tips account in the Database, it also gives the user the priviledge of retweeting particular tweets to his own account after authentication,
it also allows for seamless filtering over the tweets scraped.

It also provides API endpoints that can be easily plugged into a Front End

### Preview
![image](github-images/Screenshot from 2021-05-29 18-02-11.png)
![image](github-images/Screenshot from 2021-05-29 18-02-18.png)

### Windows Users Caveat for Installation
if you are running the package on a windows OS open up your requirements.txt file and change `celery==5.1.0` to `celery==5.0.5` to avoid `ModulNotFoundError: No module named 'grp'`


### How to install
First activate your vitual environment with  `source venv/bin/activate` if on linux
- Next   
```python
cd python-tips-aid
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
- Firstly Make sure you are in **python-tips-aid** project directory containing the manage.py file
- next open a new terminal with your venv active and in the right directory with manage.py run
```python 
    celery -A twitter_help worker -B -l INFO
```
check the website at `http://127.0.0.1:8000`

### CAVEATS (This doesnt affect the API and the API would work just fine without)
for the django website twitter user authentication to function properly, if it wasnt already obvious, you would need to be running an https server which django doesnt support out of the box, however you can use the very handy ngrok.io to listen to port 8000 which django listens to by default. **THEN** you would need to update the website urls on the twitter developer account
#### assuming we use ngrok and our live url is https://db9fe5b84537.ngrok.io
- Callback Url ---> `http://db9fe5b84537.ngrok.io/twitter-auth/cb`
- Website Url ----> `http://db9fe5b84537.ngrok.io`

also change app permissions in developer.twitter dashboard to allow Read/Write Access

IF all these arent done, you cant authenticate for the website aspect :(.

### Swagger Docs For the API
Open the Swagger Docs to see the available endpoints
`http://127.0.0.1:8000/api/swagger`

### LIVE URL
`https://pytip-helper.herokuapp.com`   

### API LIVE URL
`https://pytip-helper.herokuapp.com/api`   


### API Endpoints

- `api/auth/twitter` ---> POST ----> {
    'access_token': Twitter Access Token, 
    'token_secret': Twitter Access Secret Token
} ----> RESPONSE ---> {
    token: token_string # USE THIS TOKEN FOR AUTHORIZATION ON POST REQUEST
} with the format under Headers  ---> `Authorization : 'Token your_token_string'` send this along with every POST request

- `api/user/favorites` ---> POST ----> {
    'username': twitter username, 
    'tweets_count': number of tweets to be fetched, max is 400
}

- `api/user/mentions` ---> POST ----> {
    'tweets_count': number of tweets to be fetched, max is 400
}

**endpoints under `api/tweets/...` can be found in the swagger docs at `/api/swagger/`**

**github url `https://github.com/shols232/python-tips-aid`**
