import json
import logging

from flask import Flask, jsonify, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth

import configs
import configs.paths as paths
import malapi

app = Flask(configs.app_name)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    with open('/Users/eduardlooga/PycharmProjects/malproxy/configs/users.json', 'r') as users_file:
        app.logger.debug("Reading users.json file and validating a password...")
        users = json.load(users_file)
        if username in users and check_password_hash(users.get(username)['password'], password):
            app.logger.debug("Password is valid!")
            return username
        app.logger.warn("Invalid password for user %s!", username)


@app.route(paths.global_ping)
def global_ping():
    app.logger.info("Ping endpoint was called.")
    return jsonify("pong!")


@app.route(paths.global_version)
def global_version():
    app.logger.info("Version endpoint was called.")
    return jsonify(configs.version)


@app.route(paths.global_log, methods=['GET', 'POST'])
def log_root():
    if request.method == 'POST':
        app.logger.info("req %s with %s and headers %s", request.path, str(request.form), dict(request.headers))
    else:
        app.logger.info("req %s with %s and headers %s", request.path, request.args, dict(request.headers))
    return jsonify({"status": "ok"})


@app.route(paths.plex_handler, methods=['POST'])
def plex_handler():
    app.logger.info("Plex handler endpoint called.")
    plex_data = json.loads(request.form['payload'])
    app.logger.debug("Plex payload is %s", plex_data)

    if plex_data['Metadata']['librarySectionTitle'] != configs.plexdictionary.anime_folder:
        return jsonify({"status": "ok"})

    plex_event = plex_data[configs.plexdictionary.event]
    app.logger.debug("Plex event is %s", plex_event)

    if plex_event == configs.plexdictionary.play:
        app.logger.info("A playback has just started!")
    elif plex_event == configs.plexdictionary.pause:
        app.logger.info("User has paused the media.")
    elif plex_event == configs.plexdictionary.resume:
        app.logger.info("User has resumed the media.")
    elif plex_event == configs.plexdictionary.scrobble:
        app.logger.info("User has watched the media past 90%.")
    else:
        app.logger.error("Unknown event received (%s)! App does not how to handle it yet.", plex_event)
        abort(501, description="Unknown event received! App does not how to handle it yet.")


@app.route(paths.episode_finished)
@auth.login_required
def episode_finished():
    app.logger.info("req %s with %s", request.path, request.json)
    # Init the MalAPI object
    # Check that the title is present in the list
    # TODO: some logic with title status?
    # update the title
    return jsonify({"status": "ok"})


@app.route(paths.get_list)
@auth.login_required
def get_anime_list():
    app.logger.info("req %s with %s", request.path, request.json)
    user = request.args.get('user')

    # load users file and fetch the necessary data from there
    app.logger.debug("Loading users file...")
    with open(configs.users_db, mode='r') as users_file:
        users = json.load(users_file)

    app.logger.debug("Checking %s's presence in users file and fetching username and token...", user)
    if user in users:
        mal_token = users[user]['mal_password']
        mal_username = users[user]['mal_username']

    # Init the MalAPI object
    app.logger.debug("Initializing MalAPI object...")
    mal_api = malapi.MalAPI(mal_username, mal_token)

    # get all animes in "watching" list
    app.logger.debug("Fetching 'Watching' list for %s...", mal_username)
    watching_list = mal_api.get_anime_list()
    app.logger.info("'Watching' list for %s: %s", mal_username, watching_list)

    # Check that the title is present in the list
    # TODO: some logic with title status?
    # update the title
    return jsonify(watching_list)


@app.route(paths.create_user, methods=['POST'])
@auth.login_required
def create_user():
    app.logger.info("req %s with %s", request.path, request.json)
    default_user_params = {
        "shared": False,
        "password": "not_set",
        "mal_username": "",
        "mal_password": ""
    }
    try:
        password = request.json.get('password')
        username = request.json.get('username')
        password_hash = generate_password_hash(password)

        default_user_params['password'] = password_hash
        default_user_params['shared'] = request.json.get('shared', False)
        default_user_params['mal_username'] = request.json.get('mal_username')
        default_user_params['mal_password'] = request.json.get('mal_password')
        new_user_params = {username: default_user_params}

        with open(configs.users_db, mode='r') as users_file:
            users = json.load(users_file)
        users.update(new_user_params)
        with open(configs.users_db, mode='w') as users_file:
            json.dump(users, users_file, indent=2)
    except Exception as e:
        app.logger.error("Failed to create a new user!")
        app.logger.exception(e)
        return jsonify({"status": "error", "details": str(e)})

    app.logger.info("User '%s' created successfully.", username)
    return jsonify({"status": "ok", "username": request.json.get('username')})


if __name__ == '__main__':
    logging.basicConfig(filename=configs.logging.path,
                        level=configs.logging.level,
                        format=configs.logging.log_format)
    app.run(debug=configs.debug_mode, port=configs.port)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(configs.logging.level)
