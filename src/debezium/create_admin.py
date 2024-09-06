from pymongo import MongoClient
from pymongo.errors import OperationFailure

def create_admin_user():
    try:
        # Connection string to the MongoDB replica set
        connection_string = "mongodb://mongo1:30001,mongo2:30002,mongo3:30003/?replicaSet=my-replica-set"
        
        # Create a MongoClient to the replica set
        client = MongoClient(connection_string)

        # Connect to the admin database
        admin_db = client['admin']

        # Check if the admin user already exists
        admin_users = admin_db.command("usersInfo", "admin")['users']
        if not admin_users:
            # Create the admin user
            admin_db.command("createUser", "admin", pwd="admin", roles=[{"role": "userAdminAnyDatabase", "db": "admin"}])
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")

    except OperationFailure as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        client.close()

# Run the function
create_admin_user()
