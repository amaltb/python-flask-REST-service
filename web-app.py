import requests
from flask import Flask, render_template, session, redirect, request, url_for, g, make_response, jsonify

from database import Database
from twitter_utils import get_request_token, get_authorization_url, get_access_token
from user import User

app = Flask(__name__)

app.secret_key = '1234'

Database.initialise(host='localhost', database='learning', user='ambabu', password='Workexp8261@')


@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user = User.load_from_db_by_screenname(session['screen_name'])


@app.route('/', methods=['GET'])
def homepage():
    return render_template('home.html')


@app.route('/login/twitter', methods=['GET'])
def twitter_login():
    if 'screen_name' in session:
        return redirect(url_for('user_profile'))

    request_token = get_request_token()
    session['request_token'] = request_token

    return redirect(get_authorization_url(request_token))


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('homepage'))


@app.route('/auth/twitter', methods=['GET'])
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = get_access_token(session['request_token'], oauth_verifier)

    user = User.load_from_db_by_screenname(access_token['screen_name'])

    if not user:
        user = User(access_token['screen_name'], access_token['oauth_token'],
                    access_token['oauth_token_secret'], None)
        user.save_to_db()

    session['screen_name'] = user.screen_name

    return redirect(url_for('user_profile'))


@app.route('/profile')
def user_profile():
    return render_template('profile.html', user=g.user)


@app.route('/search', methods=['GET']) # search query string parameter here
def search():
    query = request.args.get('q')
    tweets = g.user.tweet_request('https://api.twitter.com/1.1/search/tweets.json?q={}'.format(query))

    tweet_text = [{'tweet': tweet['text'], 'label':'neutral'} for tweet in tweets['statuses']]

    for tweet in tweet_text:
        sentiment = requests.post("http://text-processing.com/api/sentiment/",
                                  {'text': tweet['tweet'], 'language': 'english'})
        label = sentiment.json().get('label')
        tweet['label'] = label

    return render_template('search.html', content=tweet_text)


@app.route("/post", methods=['POST'])
def post_test():
    if not request.json:
        return make_response(jsonify({'error': 'request body is not a valid json'}), 400)
    value1 = request.json['key1']
    value2 = request.json['key2']

    return jsonify({'key1': value1, 'key2': value2}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


app.run(port=4995, debug=True)
