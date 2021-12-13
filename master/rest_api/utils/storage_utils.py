from flask import g
import sqlite3


class StorageUtils:

    def __init__(self):
        pass

    def get_db(self):
        # Connect to the sqlite DB at 'files.db' and store the connection in 'g.db'
        # Re-use the connection if it already exists
        if 'db' not in g:
            g.db = sqlite3.connect('../storage/metadata.db', detect_types=sqlite3.PARSE_DECLTYPES)

        # Enable casting Row objects to Python dictionaries
        g.db.row_factory = sqlite3.Row
        return g.db

    def close_db(self, e=None):
        # Close the DB connection and remove it from the 'g' object
        self.db = g.pop('db', None)
        if self.db is not None:
            self.db.close()

    def insert_file_meta_data(self, filename, size, content_type, date, file_data_1_names, file_data_2_names):
        # Insert the File record in the DB
        db = self.get_db()
        cursor = db.execute(
        """INSERT INTO `metadata`(`filename`, `size`, `content_type`, `created`, `part1_filenames`,
        `part2_filenames`) VALUES (?,?,?,?,?,?)""",
        (filename, size, content_type, date, ','.join(file_data_1_names), ','.join(file_data_2_names))
        )
        
        db.commit()    

        return cursor.lastrowid    

    def get_metadata(self, file_id):
        db = self.get_db()
        cursor = db.execute("SELECT * FROM `metadata` WHERE `id`=?", [file_id])

        if not cursor:     
            return None
        else:
            return cursor.fetchone()

