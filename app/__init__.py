from flask import Flask

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")  # ✅ Set correct paths
    app.config.from_object('app.config.Config')

    from .routes import routes
    app.register_blueprint(routes)

    return app
