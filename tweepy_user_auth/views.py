from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect
from django.conf import settings
import tweepy

def auth(request):
    # start the OAuth process, set up a handler with our details
    oauth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY)
    # direct the user to the authentication url
    # if user is logged-in and authorized then transparently goto the callback URL
    auth_url = oauth.get_authorization_url()
    response = HttpResponseRedirect(auth_url)
    # store the request token
    request.session['request_token'] = oauth.request_token
    request.session.modified = True

    return response

# tweepy callback view
def auth_callback(request):
    '''
        acesses twitter oauth_verifier and sets token, token secret into session
    '''
    request_token = request.session['request_token']
    del request.session['request_token'] 

    auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY)
    auth.request_token = request_token
    verifier = request.GET.get('oauth_verifier')
    auth.get_access_token(verifier)
    request.session['token'] = (auth.access_token, auth.access_token_secret)
    request.session['is_authenticated'] = True
    return redirect('/')


def logout(request):
    try:
        del request.session['token']
        del request.session['is_authenticated']
    except KeyError:
        # the keys dont exist hence not authenticated
        pass

    return redirect('/')