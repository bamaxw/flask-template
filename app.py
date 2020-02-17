from flask import Flask

from superflask import init_superflask_app

application = Flask(__name__)
init_superflask_app(application)


if __name__ == "__main__":
    application.run()
