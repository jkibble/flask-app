from flask import Flask, render_template

app = Flask(__name__)

print(f'{__name__} starting')

@app.route('/')
def home():
  return render_template('index.html')

if __name__ == '__main__':
  app.run()
