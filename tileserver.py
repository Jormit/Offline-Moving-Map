from flask import Flask
from flask import make_response
from flask import send_from_directory
from flask import abort
from flask import redirect
import tiledb

app = Flask(__name__)
map_data = r".\static\2017-07-03_australia-oceania_australia.mbtiles"

@app.route('/')
def root():
    return redirect('/index.html')

@app.route('/metadata')
def get_metadata():  
    db = tiledb.tiledb(map_data)
    return db.get_metadata()

@app.route('/tiles/<z>/<x>/<y>.pbf')
def get_tile(z=0, x=0, y=0): 
    db = tiledb.tiledb(map_data)
    y = (2 ** int(z)) - int(y) - 1
    tile = db.get_tile(z, x, y)
    if (tile is None):
        abort(404)
    response = make_response(tile) 
    response.headers.set('Content-Type', 'application/protobuf')
    response.headers.set('Content-Encoding', 'gzip')
    response.headers.set('Content-Disposition', 'attachment', filename='tile_{}_{}_{}.pbf'.format(z,x,y))
    return response

@app.route('/fonts/<stack>/<filename>')
def get_font(stack, filename):
    response = make_response(send_from_directory('./static/font/', filename))     
    response.headers.set('Content-Type', 'application/protobuf')
    response.headers.set('Content-Disposition', 'attachment', filename=filename)
    return response

@app.route('/<filename>')
def get_file(filename):
    return send_from_directory('./static', filename)

if __name__ == "__main__":  
    app.run(debug=True)