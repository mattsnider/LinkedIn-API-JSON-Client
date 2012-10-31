#!/usr/bin/env python
import httplib2
from mock import patch
import unittest
import urlparse
import simplejson

from linkedin_json_client import api
from linkedin_json_client.constants import (
    LinkedInScope, BasicProfileFields, BasicProfileSelectors, FullProfileSelectors)

"""

https://api.linkedin.com/v1/people/~/email-address
null
"""

class TestApi(unittest.TestCase):
    def setUp(self):
        super(TestApi, self).setUp()
        self.consumer_key = 'key'
        self.consumer_secret = 'secret'

        self.access_token = (
            'oauth_token=ef0bfbcc-1144-4c5d-a73b-b40c26605da2'
            '&oauth_token_secret=76310eea-fd89-4c44-a9db-0ee61de2c527'
            '&oauth_expires_in=0&oauth_authorization_expires_in=0')
        self.request_token = (
            'oauth_token=9f63bba2-a2ad-4d70-93c0-19d6f11fdc02'
            '&oauth_token_secret=b437f289-9955-4b55-a733-de4a89a15ab0'
            '&oauth_callback_confirmed=true'
            '&xoauth_request_auth_url=https%3A%2F%2Fapi.linkedin.com'
            '%2Fuas%2Foauth%2Fauthorize&oauth_expires_in=599')

        self.api = api.LinkedInJsonAPI(self.consumer_key, self.consumer_secret)

    def _responseFactory(self, info=None):
        d = {
            'status': '200',
            'transfer-encoding': 'chunked',
            'age': '1',
            'vary': 'Accept-Encoding',
            'server': 'Apache-Coyote/1.1',
            'connection': 'keep-alive',
            '-content-encoding': 'gzip',
            'date': 'Wed, 31 Oct 2012 21:10:29 GMT',
            'content-type': 'text/plain'
        }

        if info:
            d.update(info)

        return httplib2.Response(d)

    def _responseFactoryAPI(self, info=None):
        d = self._responseFactory()
        d.update({
            'vary': '*',
            'x-li-request-id': 'IMNF2HTLXM',
            'x-li-format': 'json',
            'content-type': 'application/json;charset=UTF-8'
        })

        if info:
            d.update(info)

        return httplib2.Response(d)

    def test_get_access_token(self):
        """
        Tests that expected responses from the LinkedIn API for
        get_access_token are properly handled. Known cases:
            success response
        """
        request_token = dict(urlparse.parse_qsl(self.request_token))
        verifier = 72096

        with patch('linkedin_json_client.api.oauth.Client') as patched_Client:
            # test a successful request
            client = patched_Client.return_value
            client.request.return_value = (
                self._responseFactory({
                    'content-length': '156',
                }),
                self.access_token)
            self.failUnlessEqual(
                self.api.get_access_token(request_token, verifier),
                dict(urlparse.parse_qsl(self.access_token)))

    def test_get_email_profile(self):
        """
        Tests that expected responses from the LinkedIn API for
        get_user_profile are properly handled. Known cases:
            success response without selectors
            success response with selectors
        """
        access_token = dict(urlparse.parse_qsl(self.access_token))

        with patch('linkedin_json_client.api.oauth.Client') as patched_Client:
            # test a successful request that returns null
            client = patched_Client.return_value
            client.request.return_value = (
                self._responseFactoryAPI({
                    'content-length': '4',
                    'content-location':
                        u'https://api.linkedin.com/v1/people/~/email-address?'
                        u'oauth_body_hash=2jmj7l5rSw0yVb%2FvlWAYkK%2FYBwk%3D&'
                        u'oauth_nonce=30612878&oauth_timestamp=1351720757&'
                        u'oauth_consumer_key=q00tdja3bfzo&format=json&'
                        u'oauth_signature_method=HMAC-SHA1&oauth_version=1.0&'
                        u'oauth_token=ef0bfbcc-1144-4c5d-a73b-b40c26605da2&'
                        u'oauth_signature=rTK25E5HTOqz2RhW5Y8kqviqHfs%3D',
                }),
                'null')
            email = self.api.get_email_address(access_token)
            self.failUnlessEqual(email, None)

            # test a successful request without selectors
            data_str = 'jsmith@votizen.com'
            client = patched_Client.return_value
            client.request.return_value = (
                self._responseFactoryAPI({
                    'content-length': '20',
                    'content-location':
                        u'https://api.linkedin.com/v1/people/~/email-address?'
                        u'oauth_body_hash=2jmj7l5rSw0yVb%2FvlWAYkK%2FYBwk%3D&'
                        u'oauth_nonce=74552870&oauth_timestamp=1351726586&'
                        u'oauth_consumer_key=wldnomopxrhh&format=json&'
                        u'oauth_signature_method=HMAC-SHA1&oauth_version=1.0&'
                        u'oauth_token=fc0522c7-0fd3-45e8-8130-5ea462d87ac0&'
                        u'oauth_signature=nF9y%2FOfWA0L2eq8i1w%2F2skUcfSQ%3D',
                }),
                data_str)
            email = self.api.get_email_address(access_token)
            self.failUnlessEqual(email, data_str)

    def test_get_request_token(self):
        """
        Tests that expected responses from the LinkedIn API for
        get_request_token are properly handled. Known cases:
            success response without scope
            success response with scope
        """
        with patch('linkedin_json_client.api.oauth.Client') as patched_Client:
            client = patched_Client.return_value
            client.request.return_value = (
                self._responseFactory({
                    'content-length': '236',
                }),
                self.request_token)

            # test a successful request without scope
            self.failUnlessEqual(
                self.api.get_request_token(),
                dict(urlparse.parse_qsl(self.request_token)))

            # test a successful request with
            self.failUnlessEqual(
                self.api.get_request_token(
                    scope=[
                        LinkedInScope.BASIC_PROFILE,
                        LinkedInScope.EMAIL_ADDRESS,
                        LinkedInScope.NETWORK_UPDATES,
                        LinkedInScope.CONNECTIONS,
                        LinkedInScope.CONTACT_INFO,
                        LinkedInScope.MESSAGES]),
                dict(urlparse.parse_qsl(self.request_token)))

    def test_get_user_profile(self):
        """
        Tests that expected responses from the LinkedIn API for
        get_user_profile are properly handled. Known cases:
            success response without selectors
            success response with selectors
        """
        access_token = dict(urlparse.parse_qsl(self.access_token))
        selectors = [
            BasicProfileSelectors.ID, BasicProfileSelectors.FIRST_NAME,
            BasicProfileSelectors.LAST_NAME,
            BasicProfileSelectors.LOCATION, FullProfileSelectors.DATE_OF_BIRTH,
            BasicProfileSelectors.PUBLIC_PROFILE_URL,
            BasicProfileSelectors.PICTURE_URL,
            BasicProfileSelectors.SITE_STANDARD_PROFILE_REQUEST,
            BasicProfileSelectors.TWITTER_ACCOUNTS, BasicProfileSelectors.SUMMARY,
            BasicProfileSelectors.MAIN_ADDRESS
        ]

        with patch('linkedin_json_client.api.oauth.Client') as patched_Client:
            # test a successful request without selectors
            data = {  # this was an actual response from API
                      "firstName": "John",
                      "headline": "Tester at Product Testing",
                      "lastName": "Smith",
                      "siteStandardProfileRequest": {
                          "url": "http://www.linkedin.com/profile?viewProfile="
                                 "&key=169364659&authToken=idE-&authType=name"
                                 "&trk=api*a165186*s173442*"}
            }
            data_str = simplejson.dumps(data)

            client = patched_Client.return_value
            client.request.return_value = (
                self._responseFactoryAPI({
                    'content-length': '248',
                    'content-location':
                        u'https://api.linkedin.com/v1/people/~?oauth_body_hash'
                        u'=2jmj7l5rSw0yVb%2FvlWAYkK%2FYBwk%3D&oauth_nonce='
                        u'4922800&oauth_timestamp=1351725442&'
                        u'oauth_consumer_key=q00tdja3bfzo&format=json&'
                        u'oauth_signature_method=HMAC-SHA1&oauth_version=1.0&'
                        u'oauth_token=ef0bfbcc-1144-4c5d-a73b-b40c26605da2&'
                        u'oauth_signature=GLkQMUFaheMJ8y%2Bg2PRomHe8J6I%3D',
                }),
                data_str)
            profile = self.api.get_user_profile(access_token)
            self.failUnlessEqual(profile, data)

            # test a successful request with selectors
            data = {  # this was an actual response from API
                      "firstName": "John",
                      "id": "OAwW7wk0xl",
                      "lastName": "Smith",
                      "location": {
                          "country": {"code": "us"},
                          "name": "San Francisco Bay Area"
                      },
                      "publicProfileUrl": "http://www.linkedin.com/pub/john-smith/"
                                          "48/877/b57",
                      "siteStandardProfileRequest": {
                          "url": "http://www.linkedin.com/profile?viewProfile="
                                 "&key=169364659&authToken=idE-&authType=name"
                                 "&trk=api*a165186*s173442*"
                      },
                      "twitterAccounts": {"_total": 0}
            }
            data_str = simplejson.dumps(data)

            client = patched_Client.return_value
            client.request.return_value = (
                self._responseFactoryAPI({
                    'content-length': '427',
                    'content-location':
                        u'https://api.linkedin.com/v1/people/~:(id,first-name,'
                        u'last-name,location,date-of-birth,public-profile-url,'
                        u'picture-url,site-standard-profile-request,'
                        u'twitter-accounts,summary,main-address)?'
                        u'oauth_body_hash=2jmj7l5rSw0yVb%2FvlWAYkK%2FYBwk%3D&'
                        u'oauth_nonce=18576507&oauth_timestamp=1351720755&'
                        u'oauth_consumer_key=q00tdja3bfzo&format=json&'
                        u'oauth_signature_method=HMAC-SHA1&oauth_version=1.0&'
                        u'oauth_token=ef0bfbcc-1144-4c5d-a73b-b40c26605da2&'
                        u'oauth_signature=ZSNPv8LmiuTtmE1ON%2F0kR0K1r6Y%3D',
                }),
                data_str)
            profile = self.api.get_user_profile(
                access_token, selectors=selectors)
            self.failUnlessEqual(profile, data)

            # smoke test that names from actual request match constants
            self.failUnlessEqual(
                profile[BasicProfileFields.FIRST_NAME],
                data[BasicProfileFields.FIRST_NAME])
            self.failUnlessEqual(
                profile[BasicProfileFields.LAST_NAME],
                data[BasicProfileFields.LAST_NAME])
            self.failUnlessEqual(
                profile[BasicProfileFields.ID],
                data[BasicProfileFields.ID])
            self.failUnlessEqual(
                profile[BasicProfileFields.PUBLIC_PROFILE_URL],
                data[BasicProfileFields.PUBLIC_PROFILE_URL])
            self.failUnlessEqual(
                profile[BasicProfileFields.LOCATION],
                data[BasicProfileFields.LOCATION])
            self.failUnlessEqual(
                profile[BasicProfileFields.SITE_STANDARD_PROFILE_REQUEST],
                data[BasicProfileFields.SITE_STANDARD_PROFILE_REQUEST])
            self.failUnlessEqual(
                profile[BasicProfileFields.TWITTER_ACCOUNTS],
                data[BasicProfileFields.TWITTER_ACCOUNTS])

if __name__ == '__main__':
    unittest.main()