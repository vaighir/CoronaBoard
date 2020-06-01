#!/usr/bin/env python3
import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
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
    from . import covid_blueprint
    app.register_blueprint(index.bp)
    app.register_blueprint(user_blueprint.bp)
    app.register_blueprint(post_blueprint.bp)
    app.register_blueprint(comment_blueprint.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(covid_blueprint.bp)

    from . import http_error_handlers
    app.register_error_handler(404, http_error_handlers.page_not_found)

    return app
