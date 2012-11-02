Introduction
============

The LinkedIn-API-JSON-Client library provides an abstract interface for working with the LinkedIn API. My goal is that you should not have to understand oauth or much of the details of the LinkedIn client library (if setup correctly, it should just work).

All functions and classes are documented inline. If you have additional questions, I can be reached on github or at admin@mattsnider.com.

Disclaimer
==========

This package is loosely based on the LinkedIn-Client-Library by Aaron Brenzel. The original library was written for XML support, but LinkedIn now supports JSON responses, which IMHO provides a cleaner interface for use with python. I have tried to preserve the same general architecture and api functions, while adding some new ones, improving error management, and making the API more DRY.

Getting started
===============

Standard stuff applies to install. Use PIP to install with dependencies:

    pip install linkedin-api-json-client

Or install from the command line:

    python setup.py install

If you install from the command line, you will need to also install the oauth2, simplejson, and httplib2 packages.

This package is intended for use with the LinkedIn API. You must supply your own API key for this library to work. Once you have an API key from LinkedIn, the syntax for instantiating an API client object is this::

    my_key = 'mysecretkey'
    my_secret = 'mysecretsecret'
    li_client = LinkedInJsonAPI(my_key, my_secret)

From there, you can obtain request tokens, authorization urls, access tokens, and actual LinkedIn data through the LinkedInJsonAPI object's methods.  The object will handle signing requests, url formatting, and JSON parsing for you.

Dependencies
============

Currently, the API is dependent on oauth2, httplib2 (for oauth2), and simplejson. All can easily be obtained using Python Package Index, and will be automatically included, if you use PIP to install.

Authorization Guide
===================

Oauth authorization is a multi-step process. When a user wants to authorize your app, you must first create an authorization URL, indicating which permissions your application needs, and redirect the user there::

    from urllib import urlencode
    from linkedin_json_client.constants import LinkedInScope
    try:
        request_token_dict = li_client.get_request_token(scope=[
            LinkedInScope.BASIC_PROFILE, LinkedInScope.EMAIL_ADDRESS])
        url = '%s?%s' % (li_client.authorize_path, urlencode(request_token_dict))
        # store your request token in the user session for use in callback
        request.session['li_request_token'] = request_token_dict
        # REDIRECT USER TO url
    except (HTTPError, socket.error):
        # failed to connect to LinkedIn, handle this in your application

When you setup your application on LinkedIn, you specified a callback URL for authorization. That URL should compare the stored request token against an oauth verifier token::

    oauth_verifier = request.GET.get('oauth_verifier')
    request_token = request.session.get('li_request_token')

    oauth_problem = request.GET.get('oauth_problem')
    if oauth_problem or request_token is None:
        if oauth_problem == 'user_refused':
            # user refused auth, handle in your application
        # some other problem, handle in your application
    else:
        access_token = li_client.get_access_token(request_token, oauth_verifier)
        # user successfully authorized, store this access_token and associate with the user for use with API

Once you have an access token, you may make calls against the API::

    from linkedin_json_client.constants import BasicProfileFields, BasicProfileSelectors
    json_object = li_client.get_user_profile(access_token, [BasicProfileSelectors.FIRST_NAME, BasicProfileSelectors.LAST_NAME, BasicProfileSelectors.ID])

    json_object[BasicProfileFields.ID]
    json_object[BasicProfileFields.FIRST_NAME]
    json_object[BasicProfileFields.LAST_NAME]

If something goes wrong with any API calls, except authorization, a LinkedInApiJsonClientError is raised, so it is best to always wrap API calls in a try statement and handle the error in your app::

    try:
        # api call
    except LinkedInApiJsonClientError, e:
        print e

Todo
====

#. Search support
#. Test coverage where the LinkedIn API is mocked
#. Build docs from comments
#. Test coverage against the LinkedIn API, will require test users with fairly complete profiles. Haven't been able to get help from LinkedIn to create test data, so if anyone has any ideas here, let me know.