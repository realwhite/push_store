import os

from server.app import Application
from server.utils import load_conf

def main():
    config = load_conf(os.path.join(os.getcwd(), 'config.yml'))
    app = Application(config)
    app.run()
