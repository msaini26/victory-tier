"""
Serves a page and responds to requests
"""
import websockets
from flask import Flask, render_template, request

app = Flask(__name__)

# Serve the main site (search bar)
@app.route('/', methods=['GET', 'POST'])
def form():
    return render_template('./index.html')

# Retrieve the closest three basketball players
@app.route('/search', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        query = request.form['q']       # q for query
    else:
        query = request.args.get('q')   # q for query

    # Reply with the three players
    return render_template('results.html', p1='LeBron James', p2='Michael Jordan', p3='Rajon Rondo')

if __name__ == "__main__":
    app.run()
