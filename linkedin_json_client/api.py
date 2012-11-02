#! usr/bin/env python
from datetime import datetime
import time
import urllib
import urlparse
import oauth2 as oauth
import simplejson

from linkedin_json_client.errors import LinkedInApiJsonClientError


class LinkedInJsonAPI(object):
    format = {'format': 'json'}

    base_url = 'https://api.linkedin.com'
    li_url = 'http://www.linkedin.com'

    api_comment_feed_url = (
        base_url + '/v1/people/~/network/updates/key=%(NETWORK_UPDATE_KEY)s/'
                   'update-comments')
    api_email_url = base_url + '/v1/people/~/email-address'
    api_mailbox_url = base_url + '/v1/people/~/mailbox'
    api_network_update_url = base_url + '/v1/people/~/network'
    api_profile_connections_url = base_url + '/v1/people/~/connections'
    api_profile_url = base_url + '/v1/people/~'
    api_shares_url = base_url + '/v1/people/~/shares'
    api_update_status_url = base_url + '/v1/people/~/current-status'

    access_token_path = base_url + '/uas/oauth/accessToken'
    authorize_path = base_url + '/uas/oauth/authorize'
    request_token_path = base_url + '/uas/oauth/requestToken'

    valid_network_update_codes = [
        'ANSW', 'APPS', 'CONN', 'JOBS', 'JGRP', 'PICT', 'RECU', 'PRFU',
        'QSTN', 'STAT']

    def __init__(self, ck, cs):
        self.consumer_key = ck
        self.consumer_secret = cs
        self.consumer = oauth.Consumer(self.consumer_key, self.consumer_secret)

    def check_network_code(self, code):
        if code not in self.valid_network_update_codes:
            raise ValueError('Code %s not a valid update code' % code)

    def dt_obj_to_string(self, dtobj):
        if (type(dtobj) == type(int) or type(dtobj) == type(str) or
            type(dtobj) == type(long)):
            return dtobj
        elif hasattr(dtobj, 'timetuple'):
            return time.mktime(int(dtobj.timetuple())*1000)
        else:
            raise TypeError('Inappropriate argument type - use either a '
                            'datetime object, string, or integer for '
                            'timestamps')

    def get_access_token(self, request_token, verifier):
        """
        Get an access token based on the generated request_token and the
        oauth verifier supplied in the return URL when a user authorizes their
        application
        """
        token = self.get_user_token(request_token)
        token.set_verifier(verifier)
        return dict(urlparse.parse_qsl(self.request(
            self.access_token_path, {}, 'POST', token=token)))

    def get_comment_feed(
        self, access_token, network_key, headers=None, **query_args):
        """
        Get a comment feed for a particular network update.
        Requires the update key for the network update as returned by the API.
        """
        token = self.get_user_token(access_token)
        url = self.api_comment_feed_url % {'NETWORK_UPDATE_KEY': network_key}
        return simplejson.loads(self.request(
            url, query_args, 'GET', headers=headers, token=token))

    def get_email_address(self, access_token, headers=None, **query_args):
        """
        Get the user email. Requires new api token and
        r_emailaddress permission.
        """
        token = self.get_user_token(access_token)
        s = self.request(self.api_email_url, query_args, 'GET', token=token,
            headers=headers)
        return None if 'null' == s else s

    def get_network_updates(self, access_token, **query_args):
        """
        Get network updates for the current user.  Valid keyword arguments are
        "count", "start", "type", "before", and "after". "Count" and "start"
        are for the number of updates to be returned. "Type" specifies what
        type of update you are querying. "Before" and "after" set the time
        interval for the query. Valid argument types are an integer
        representing UTC with millisecond precision or a Python datetime
        object.
        """
        if 'type' in query_args.keys():
            assert type(query_args['type']) == type(list()),\
                'Keyword argument "type" must be of type "list"'
            [self.check_network_code(c) for c in query_args['type']]

        if 'before' in query_args.keys():
            query_args['before'] = (self.dt_obj_to_string(query_args['before'])
                                if query_args['before'] else None)
        if 'after' in query_args.keys():
            query_args['after'] = (self.dt_obj_to_string(query_args['after'])
                               if query_args['after'] else None)

        token = self.get_user_token(access_token)
        return self.request(
            self.api_network_update_url, query_args, 'GET', token=token)

    def get_request_token(self, scope=None):
        """
        Get a request token based on the consumer key and secret to supply the
        user with the authorization URL they can use to give the application
        access to their LinkedIn accounts
        """
        query_args = {}

        if scope:
            assert type(scope) == type([]), '"Keyword argument "scope" '\
                                            'must be of type "list"'
            query_args['scope'] = " ".join(scope)

        return dict(urlparse.parse_qsl(self.request(
            self.request_token_path, query_args, 'POST')))

    def get_user_connections(
        self, access_token, selectors=None, query_args=None, headers=None):
        """
        Get the connections of the current user. Valid keyword arguments are
        "count" and "start" for the number of profiles you wish returned.
        Types are automatically converted from integer to string for URL
        formatting if necessary.
        """
        token = self.get_user_token(access_token)
        url = self.api_profile_connections_url
        if selectors:
            assert type(selectors) == type([]), (
                '"Keyword argument "selectors" must be of type "list"')
            url = self.prepare_field_selectors(selectors, url)
        return simplejson.loads(self.request(
            url, query_args, 'GET', headers=headers, token=token))

    def get_user_profile(
        self, access_token, selectors=None, headers=None, **query_args):
        """
        Get a user profile.  If keyword argument "id" is not supplied, this
        returns the current user's profile, else it will return the profile of
        the user whose id is specified.  The "selectors" keyword argument takes
        a list of LinkedIn compatible field selectors.
        """
        token = self.get_user_token(access_token)
        url = self.api_profile_url
        if selectors:
            assert type(selectors) == type([]), (
                '"Keyword argument "selectors" must be of type "list"')
            url = self.prepare_field_selectors(selectors, url)
        return simplejson.loads(self.request(
            url, query_args, 'GET', token=token, headers=headers))

    def get_user_token(self, access_token):
        """
        Fetches the user oauth.Token from the provided access_token dict.
        """
        return oauth.Token(access_token['oauth_token'],
            access_token['oauth_token_secret'])

    def invitation_factory(self, recipient, subject, body, **kwargs):
        id_rec_path = '/people/id='
        email_rec_path = '/people/email='

        auth_snippet = ('<item-content><invitation-request><connect_type>'
                        'friend</connect_type>%s</invitation-request>'
                        '</item-content>')
        recipient_snippet = ('<recipient><person path=%s>%s</person>'
                             '</recipient>')

        # recipient is an email
        if '@' in recipient:
            auth_xml = auth_snippet % ''
            recipient_xml = recipient_snippet % (
                email_rec_path + recipient, '<first>%s</first><last>%s</last>'
                % (kwargs['first_name'], kwargs['last_name']))
        # recipient is an id
        else:
            auth_xml = auth_snippet % (
                '<authorization>%s</authorization><value>%s</value>' %
                (kwargs['name'], kwargs['value']))
            recipient_xml = recipient_snippet % (id_rec_path + recipient, '')

        return (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<mailbox-item><recipients>%(recipients)s</recipients>'
            '<subject>%(subject)s</subject><body>%(body)s</body>'
            '%(auth)s</mailbox-item>' % {
                'auth': auth_xml, 'body': body, 'subject': subject,
                'recipients': recipient_xml})

    def message_factory(self, recipients, subject, body):
        """
        Create message XML for use with LinkedIn API. LinkedIn expects the
        following format:
        <mailbox-item><recipients>
            <recipient><person path="/people/{PERSON_ID}"/>
                </recipient></recipients>
            <subject>{SUBJECT}</subject>
            <body>{BODY}</body>
        </mailbox-item>
        """
        recipient_xml_list = [
        '<recipient><person path="/people/%s"/></recipient>' %
        r for r in recipients]

        return (
            '<?xml version="1.0" encoding="UTF-8"?>'
            "<mailbox-item><recipients>%s</recipients>"
            "<subject>%s</subject><body>%s</body></mailbox-item>" %
            ("".join(recipient_xml_list), subject, body))

    def prepare_field_selectors(self, selectors, url):
        prep_url = url
        selector_string = ':('
        for s in selectors:
            selector_string += s + ','
        selector_string = selector_string.strip(',')
        selector_string += ')'
        prep_url += selector_string
        return prep_url

    def request(self, url, query_args, method, body='', headers=None,
        token=None):
        """
        Send a LinkedInApi request and return the response content.
        Also, throw an error when operation fails.
            url - the url for the current API call
            query_args - any query parameters for 'url'
            method - request method ('POST', 'GET', etc.)
            token - token required for authenticated API requests
        """
        client = oauth.Client(self.consumer, token=token)
        query_args.update(self.format)
        resp, content = client.request(
            url + '?%s' % urllib.urlencode(query_args), method,
            body=body, headers=headers)

        # an error occurred
        if 400 <= resp.status and content:
            try:
                raise LinkedInApiJsonClientError(simplejson.loads(content))
            except:
                # if not JSON, usually key=value pairs
                error_json = {
                    u'errorCode': u'unknown',
                    u'message': u'%s' % dict(urlparse.parse_qsl(content)),
                    u'status': u'unknown',
                    u'timestamp': u'%s' % datetime.now()
                }
                raise LinkedInApiJsonClientError(error_json)
        return content

    def send_invitation(
        self, access_token, recipients, subject, body, **query_args):
        """
        Send an invitation to a user.  "Recipients" is an ID number OR
        email address (see below), "subject" is the message subject, and
        "body" is the body of the message.
        The LinkedIn API does not allow HTML in messages.  All XML will be
        applied for you.

        NOTE:
        If you pass an email address as the recipient, you MUST include
        "first_name" AND "last_name" as keyword arguments.  Conversely,
        if you pass a member ID as the recipient, you MUST include "name"
        and "value" as keyword arguments.  Documentation
        for obtaining those values can be found on the LinkedIn website.
        """
        if 'first_name' in query_args.keys():
            mxml = self.invitation_factory(recipients, subject, body,
                first_name=query_args['first_name'],
                last_name=query_args['last_name'])
        else:
            mxml = self.invitation_factory(recipients, subject, body,
                name=query_args['name'], value=query_args['value'])
        token = self.get_user_token(access_token)
        return self.request(
            self.api_mailbox_url, query_args, 'POST', body=mxml,
                headers={'Content-Type': 'application/xml'}, token=token)

    def send_message(self, access_token, recipients, subject, body):
        """
        Send a message to a connection. "Recipients" is a list of ID numbers,
        "subject" is the message subject, and "body" is the body of the
        message. The LinkedIn API does not allow HTML in messages.
        All XML will be applied for you.
        """
        assert type(recipients) == type(list()),\
                '"Recipients argument" (2nd position) must be of type "list"'
        mxml = self.message_factory(recipients, subject, body)
        token = self.get_user_token(access_token)
        url = self.api_mailbox_url
        return self.request(
            url, {}, 'POST', body=mxml, headers={
                'Content-Type': 'application/xml'}, token=token)

    def set_status_update(self, access_token, bd):
        """
        Set the status for the current user. The status update body is the last
        positional argument. NOTE: The XML will be applied to the status update
        for you.
        """
        xml_request = ('<?xml version="1.0" encoding="UTF-8"?>'
                       '<current-status>%s</current-status>' % bd)
        token = self.get_user_token(access_token)
        return self.request(
            self.api_update_status_url, {}, 'PUT', body=xml_request, headers={
                'Content-Type': 'application/xml'}, token=token)

    def share(self, access_token, comment, title, description,
        submitted_url=None, submitted_image_url=None):
        """
        Submit share using the LinkedIn. In general the comment is user
        provided data, whilst the description and title are something
        provided by your site. The submitted_url and submitted_image_url
        are both optional, and will include a URL and image in the share.
        NOTE: For submitted_image_url to work, you must also provide
        a submitted_url.

        Here are the character limits for the other fields:
            comment - 700 character limit
            description - 256 character limit
            title - 200 character limit
        """
        bd_pre_wrapper = '<?xml version="1.0" encoding="UTF-8"?>'\
                         '<share><comment>'
        bd_middle_wrapper = '</comment><content>'
        bd_post_wrapper = '</content><visibility><code>anyone</code>'\
                          '</visibility></share>'
        content = "<title>%s</title><description>%s</description>" % (
            title.strip(), description.strip())

        if submitted_url:
            content += '<submitted-url>%s</submitted-url>' % submitted_url

        if submitted_image_url:
            content += ('<submitted-image-url>%s</submitted-image-url>' %
                        submitted_image_url)

        xml_request = (bd_pre_wrapper + comment.strip() + bd_middle_wrapper +
                       content + bd_post_wrapper)
        token = self.get_user_token(access_token)
        url = self.api_shares_url
        return self.request(
            url, {}, 'POST', body=xml_request, headers={
                'Content-Type': 'application/xml'}, token=token)

    def submit_comment(self, access_token, network_key, bd):
        """
        Submit a comment to a network update. Requires the update key for
        the network update that you will be commenting on. The comment
        body is the last positional argument.  NOTE: The XML will be
        applied to the comment for you.
        """
        bd_pre_wrapper = '<?xml version="1.0" encoding="UTF-8"?>'\
                         '<update-comment><comment>'
        bd_post_wrapper = '</comment></update-comment>'
        xml_request = bd_pre_wrapper + bd + bd_post_wrapper
        url = self.api_comment_feed_url % {'NETWORK_UPDATE_KEY': network_key}
        token = self.get_user_token(access_token)
        return self.request(
            url, {}, 'POST', body=xml_request, headers={
                'Content-Type': 'application/xml'}, token=token)
