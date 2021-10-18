from DbConnector import DbConnector

class CreateColls:

    def __init__(self):
        self.connection = DbConnector()
        self.client = self.connection.client
        self.db = self.connection.db

    def create_coll(self, collection_name):
        collection = self.db.create_collection(collection_name)    
        print('Created collection: ', collection)

    def show_coll(self):
        collections = self.client['test'].list_collection_names()
        print(collections)

def main():
    program = None
    try:
        program = CreateColls()
        program.create_coll(collection_name="User")
        program.create_coll(collection_name="Activity")
        program.create_coll(collection_name="TrackPoint")
        program.show_coll()
    except Exception as e:
        print("ERROR: Failed to use database:", e)
    finally:
        if program:
            program.connection.close_connection()


if __name__ == '__main__':
    main()