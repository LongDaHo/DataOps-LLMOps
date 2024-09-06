from pymongo import MongoClient
from pymongo.errors import OperationFailure

def create_roles_and_user():
    try:
        # Connection string to the MongoDB replica set
        connection_string = "mongodb://admin:admin@mongo1:30001,mongo2:30002,mongo3:30003/?replicaSet=my-replica-set"

        # Create a MongoClient to the replica set
        client = MongoClient(connection_string)

        # Connect to the admin database
        admin_db = client['admin']

        # Authenticate as the admin user (if not already in connection string)
        # admin_db.authenticate('admin', 'admin')

        # Create the custom roles
        roles_to_create = [
            {
                "role": "listDatabases",
                "privileges": [{"resource": {"cluster": True}, "actions": ["listDatabases"]}],
                "roles": []
            },
            {
                "role": "readChangeStream",
                "privileges": [{"resource": {"db": "", "collection": ""}, "actions": ["find", "changeStream"]}],
                "roles": []
            }
        ]

        for role in roles_to_create:
            try:
                admin_db.command("createRole", role["role"], privileges=role["privileges"], roles=role["roles"])
                print(f"Role '{role['role']}' created successfully.")
            except OperationFailure as e:
                if "already exists" in str(e):
                    print(f"Role '{role['role']}' already exists.")
                else:
                    raise

        # Create the debezium user
        debezium_user = {
            "user": "debezium",
            "pwd": "dbz",
            "roles": [
                {"role": "readWrite", "db": "inventory"},
                {"role": "read", "db": "local"},
                {"role": "listDatabases", "db": "admin"},
                {"role": "readChangeStream", "db": "admin"},
                {"role": "read", "db": "config"},
                {"role": "read", "db": "admin"}
            ]
        }

        try:
            admin_db.command("createUser", debezium_user["user"], pwd=debezium_user["pwd"], roles=debezium_user["roles"])
            print(f"User '{debezium_user['user']}' created successfully.")
        except OperationFailure as e:
            if "already exists" in str(e):
                print(f"User '{debezium_user['user']}' already exists.")
            else:
                raise

    except OperationFailure as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        client.close()

# Run the function
create_roles_and_user()
