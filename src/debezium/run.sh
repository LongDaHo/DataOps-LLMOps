python3 src/debezium/create_admin.py
python3 src/debezium/create_user.py
curl -i -X POST -H "Accept:application/json" -H 'Content-Type: application/json' http://localhost:8083/connectors -d @src/debezium/register-mongodb-avro.json