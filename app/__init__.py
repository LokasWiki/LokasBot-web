import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
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

    # a simple page that says hello
    @app.route('/status')
    def status():
        # return render_template("home.html")
        return 'Hello, World!'

    # register the database commands
    from . import db

    db.init_app(app)

    # apply the blueprints to the app
    from . import auth, words_count_tool
    app.register_blueprint(auth.bp, url_prefix="/auth")
    app.register_blueprint(words_count_tool.bp, url_prefix="/tools/words_Count")

    print(app.url_map)
    return app
