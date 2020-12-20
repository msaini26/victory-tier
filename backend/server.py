"""
Serves a page and responds to requests
"""
import websockets
from flask import Flask, render_template, request, send_from_directory, jsonify
from model import Model
import argparse

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
        query = request.json['search']
    else:
        query = request.args.get('search')

    results = model.search(query)

    # Reply with the queried player and the three similar players
    return jsonify(results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', dest='port')
    args = parser.parse_args()
    if args.port:
        app.run(host='0.0.0.0', port=args.port)
