import oauth2
import constants
import urlparse

consumer = oauth2.Consumer(constants.TWITTER_CONSUMER_KEY, constants.TWITTER_CONSUMER_SECRET)


def get_request_token():
    client = oauth2.Client(consumer)
    response, context = client.request(constants.TWITTER_REQUEST_TOKEN_URL, "POST")

    if response.status != 200:
        return Exception("Error occurred while getting request token...")

    request_token = dict(urlparse.parse_qsl(context.decode('utf-8')))
    return request_token


def console_based_authorize(request_token):
    print("Go to following URL in your browser")
    print get_authorization_url(request_token)
    oauth_verifier_pin = raw_input("Enter PIN from above URL: ")

    return oauth_verifier_pin


def get_authorization_url(request_token):
    return "{}?oauth_token={}".format(constants.TWITTER_AUTHORIZATION_URL, request_token['oauth_token'])


def get_access_token(request_token, oauth_verifier):
    twitter_oauth_token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    twitter_oauth_token.set_verifier(oauth_verifier)
    client = oauth2.Client(consumer, twitter_oauth_token)

    response, context = client.request(constants.TWITTER_ACCESS_TOKEN_URL, "POST")

    if response.status != 200:
        return Exception("Error occurred while getting access token...")

    access_token = dict(urlparse.parse_qsl(context.decode('utf-8')))
    return access_token
