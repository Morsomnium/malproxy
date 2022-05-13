import json
import logging

from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth

import configs
import configs.paths as paths

app = Flask(configs.app_name)
auth = HTTPBasicAuth()
logging.basicConfig(filename=configs.logging.path,
                    level=configs.logging.level,
                    format=configs.logging.log_format)


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
    return jsonify("pong!")


@app.route(paths.global_version)
def global_version():
    return jsonify(configs.version)


@app.route("/log", methods=['GET', 'POST'])
def log_root():
    if request.method == 'POST':
        app.logger.info("req %s with %s and headers %s", request.path, str(request.form), dict(request.headers))
    else:
        app.logger.info("req %s with %s and headers %s", request.path, request.args, dict(request.headers))
    return jsonify({"status": "ok"})


@app.route(paths.episode_finished)
@auth.login_required
def episode_finished():
    return jsonify({"status": "ok"})


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

        with open('configs/users.json', mode='r') as users_file:
            users = json.load(users_file)
        users.update(new_user_params)
        with open('configs/users.json', mode='w') as users_file:
            json.dump(users, users_file, indent=2)
    except Exception as e:
        app.logger.info("Failed to create a new user!")
        app.logger.exception(e)
        return jsonify({"status": "error", "details": "No..."})

    app.logger.info("User '%s' created successfully.", username)
    return jsonify({"status": "ok", "username": request.json.get('username')})


if __name__ == '__main__':
    app.run(debug=configs.debug_mode, port=configs.port)
