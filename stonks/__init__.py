from flask import Flask
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

print(f'{__name__} starting')

import stonks.views

if __name__ == '__main__':
  app.run()
