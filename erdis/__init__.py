from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='home')

    from . import assegnazioni
    app.register_blueprint(assegnazioni.bp)
    app.add_url_rule('/assegnazioni', endpoint='assegnazioni')

    return app
