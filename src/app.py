import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

from src.config.Constants import ErrorCode, ErrorMessage
from src.config.Config import get_config

db = SQLAlchemy()
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
cfg = get_config()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = cfg['database']['url']
    app.config['SECRET_KEY'] = cfg['app']['secret_key']

    db.init_app(app)

    app.config['SWAGGER'] = {
        'title': 'Flask API',
    }
    conf_path = os.path.abspath(__file__)
    conf_path = os.path.dirname(conf_path)
    conf_path = os.path.join(conf_path, 'config/colors_template.yaml')
    swagger = Swagger(app=app, template_file=conf_path)

    from src.routes.UserRoute import user
    from src.routes.PostRoute import post
    from src.routes.InteractionRoute import interaction
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(post, url_prefix='/post')
    app.register_blueprint(interaction, url_prefix='/interaction')

    @app.route('/', methods=['GET'])
    def home():
        """
        check healthz
        """
        return {"code": ErrorCode.Success, "message": ErrorMessage.Success, "data": []}

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host=cfg['app']['host'], port=cfg['app']['port'])
