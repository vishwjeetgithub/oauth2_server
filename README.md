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

How to securely store JWTs in a cookie
======================================
A JWT needs to be stored in a safe place inside the user’s browser. We already established that storing sensitive data inside localStorage is a bad idea. To reiterate, whatever you do, don’t store a JWT in localStorage (or sessionStorage). If any of the third-party scripts you include in your page are compromised, it can access all your users’ tokens.

To keep them secure, you should always store JWTs inside an HttpOnly cookie. This is a special kind of cookie that’s only sent in HTTP requests to the server. It’s never accessible (both for reading and writing) from JavaScript running in the browser.


HTTP has different verbs, which have different semantics:
======================================

GET : does not change anything server side, multiple GET with same parameters should get same response - typically get an account value
POST : can make changes server side, multiple POST with same parameters can lead to different results and responses - typically add an amount to an account
PUT : can make changes server side, multiple PUT with same parameters should lead to same result and response - typically set an account value

As POST is not idempotent, major browser will warn you if you send twice the same POST request which is not desirable in GET use cases.
Anyway, headers in the HTTP request control where the response should be cached or not, so it is possible to ask caches to not keep responses to GET requests.

Browser caching is a different question, because then can store the last URLs in their history cache. So sensitive information should not be send in the URL, unless you consistently clean the history when you close you browser, and close your browser when you have finished browsing a site. But sent in URL and sent in a GET request are different questions.

Post request will reload the page

One factor to consider is that GET requests can be cached, but POST requests are never cached. Some data doesn't change frequently. Some changes rarely.
Requests can be cached in various ways - by the browser, by the server, and by CDNs. All of these result in faster response times and reduced load on the server

Why is using a HTTP GET to update state on the server in a RESTful call incorrect?
======================================
The practical case where you will have a problem is that the HTTP GET is often retried in the event of a failure by the HTTP implementation. So you can in real life get situations where the same GET is received multiple times by the server. If your update is idempotent (which yours is), then there will be no problem, but if it's not idempotent (like adding some value to an amount for example), then you could get multiple (undesired) updates.

HTTP POST is never retried, so you would never have this problem

While technically you can send a body with a GET request, it is not standard practice and is generally discouraged. The HTTP specification does not define semantics for a body in a GET request, and many servers and proxies do not handle it properly. For retrieving data, rely on query parameters and URL paths.
