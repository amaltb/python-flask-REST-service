import oauth2
import json
from database import CursorFromConnectionFromPool
from twitter_utils import consumer


class User:
    def __init__(self, screen_name, oauth_token, oauth_token_secret, id):
        self.screen_name = screen_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    def __repr__(self):
        return str(vars(self))

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO users (screen_name, oauth_token, '
                           'oauth_token_secret) VALUES (%s, %s, %s)',
                           (self.screen_name, self.oauth_token, self.oauth_token_secret))

    @classmethod
    def load_from_db_by_screenname(cls, screen_name):
        with CursorFromConnectionFromPool() as cursor:
            # adding a trailing comma to define the tuple in the below statement.
            cursor.execute('SELECT * FROM users WHERE screen_name=%s', (screen_name,))
            user_data = cursor.fetchone()

            # can be replaced with if user_data, bcs None is equivalent to false in boolean..
            if user_data is not None:
                return cls(user_data[1], user_data[2], user_data[3], user_data[0])
            # return None is the default return type in python. So no need to explicitly return None.
            else:
                return None

    def tweet_request(self, url, verb="GET"):
        token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        client = oauth2.Client(consumer, token)

        response, context = client.request(url, verb)

        if response.status != 200:
            print("An error occurred while searching the tweets..")
            print(response)

        return json.loads(context.decode('utf-8'))
