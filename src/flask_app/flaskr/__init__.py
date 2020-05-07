#!/usr/bin/env python3
import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # FIXME add the secret key created for the image?
        # ENV_NAME=os.environ['ENV_NAME'],
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import index
    from . import user_blueprint
    from . import post_blueprint
    from . import comment_blueprint
    from . import auth
    app.register_blueprint(index.bp)
    app.register_blueprint(user_blueprint.bp)
    app.register_blueprint(post_blueprint.bp)
    app.register_blueprint(comment_blueprint.bp)
    app.register_blueprint(auth.bp)

    return app
