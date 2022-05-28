import sqlite3
from sqlite3 import Error

class tiledb:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def get_metadata(self):
        return dict((x, y) for x, y in self.cursor.execute("SELECT * FROM metadata").fetchall()) 

    def get_tile(self, zoom, column, row):
        tile_id = "{}/{}/{}".format(zoom, column, row)
        self.cursor.execute("SELECT tile_data FROM images WHERE tile_id='{}'".format(tile_id))
        results = self.cursor.fetchone()
        if (results is None):
            return None
        else:
            return results[0]

if __name__ == '__main__':
    db = tiledb(r".\data\2017-07-03_australia_sydney.mbtiles")
    print(db.get_bounds())
    print(db.get_metadata())
    print(db.get_tile(14, 15047, 6534))