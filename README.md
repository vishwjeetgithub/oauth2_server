# Samples for Understanding OAuth2 and Building a Basic Authorization Server of Your Own Beginner's Guide

This repository holds the samples for Understanding OAuth2 and Building a Basic Authorization Server of Your Own Beginner's Guide. See the guide for instructions on using these samples.


## Dependencies
## Authlib - pip install Authlib
## $ pip install Authlib requests
## $ pip install Authlib Flask


How the whole cycle works

Login cycle
=====================================

1. Client tries to access 5000/ (root)
2. Check whether client is authenticated (before_request)
    Fetch access token from cookies
3. If cookie does not exist or is invalid proceed to Login : 5000 (/login)
        Redirect to login page on authentication server : auth path
        Pass client_id
        Pass callback URL - /callback
4.  On the auth server auth path, from the URL (before showing the login screen) : 5001 (/auth)
        fetch client id
        fetch redirect URL - /callback
        verify the key and the redirect URL <-??
5. show the login screen, attach client id and redirect path to the URL : 5001 (HTML)
        Login screen submit takes to /signin : 5001 (oauth server /signin)
6. /signin 5001
        Fetch user name, pwd, client id, redirect url
        Verify the key and the redirect URL <-??
        Authenticate client
        generate_authorization_code
        Reirect to the redirect_url with authorization code in the URL /callback (5000/)
7. Callback (5000 /callback)(No UI is shown)
        check authorization code is returned or not
        POST to token_path along with (on oauth server 5001)
            the autorization_code received earlier
            client_id
            client_secret
            redirect_url
        Fetch access_token
        Set access_token cookie

Rest API
======================================

1. Before serving API request
    verify access_token

2. Route to main (/) 5000 (client app)(The core rest api call that we wanted to do)
        Fetch access_token from cookie
        Get request to the API resource. Pass bearer access_token in header

Access Token
======================================
Access token itself is not encrypted. Following function tries to validate the token, by matching the signature. In case token is tampered it throws an exception
jwt.decode(access_token, public_key,
                               issuer = ISSUER,
                               algorithms = ['RS256'])