"""
Serves a page and responds to requests
"""
import websockets
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__, template_folder='../frontend')

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
        query = request.form['q']       # q for query
    else:
        query = request.args.get('q')   # q for query

    # Reply with the three players
    return render_template('results.html', p1='LeBron James', p2='Michael Jordan', p3='Rajon Rondo')

if __name__ == "__main__":
    app.run()
