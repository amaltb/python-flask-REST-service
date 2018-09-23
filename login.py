from twitter_utils import get_request_token, get_access_token, console_based_authorize


class Login:

    def __init__(self):
        pass

    @staticmethod
    def login_wt_twitter_acc():
        twitter_request_token = get_request_token()
        twitter_oauth_verifier = console_based_authorize(twitter_request_token)
        twitter_access_token = get_access_token(twitter_request_token, twitter_oauth_verifier)

        return twitter_access_token
