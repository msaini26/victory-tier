"""
Serves a page and responds to requests
"""
import websockets
from flask import Flask, render_template, request, send_from_directory
from model import Model

app = Flask(__name__, template_folder='../frontend')
model = Model('./data/fantasy-basketball-stats.json')

# Serve the main site (search bar)
@app.route('/', methods=['GET', 'POST'])
def form():
    return render_template('./index.html')

@app.route('/src/<path:path>', methods=['GET'])
def serve_static(path):
    print(f'Serve {path}')
    return send_from_directory('../frontend/src', path)

# Retrieve the closest three basketball players
@app.route('/search', methods=['GET', 'POST'])
def serve():
    if request.method == 'POST':
        query = request.form['search']       # q for query
    else:
        query = request.args.get('search')   # q for query

    results = model.search(query)

    # Reply with the three players
    return render_template('results.html', **results)

if __name__ == "__main__":
    app.run()
