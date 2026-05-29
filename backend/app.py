from flask import Flask
from flask_cors import CORS

from backend.controllers.compiler_controller import compiler_bp


# Application factory keeps setup isolated and test-friendly.
def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(compiler_bp)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
