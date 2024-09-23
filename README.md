This project is in process

## System Architecture
<p align="center">
<img src="./assets/DataOps-LLMOps.svg" width=100% height=100%>

<p align="center">
    System Architecture
</p>

```shell
export PYTHONDONTWRITEBYTECODE=1
```

```shell
docker-compose -f mongo-docker-compose.yaml up -d
sudo chmod 777 /etc/hosts
echo "172.20.0.3 mongo1\n172.20.0.4 mongo2\n172.20.0.5 mongo3" >> /etc/hosts
```


```shell
docker-compose -f stream-docker-compose.yaml up -d
bash src/debezium/run.sh
```

```shell
docker-compose -f docker-compose.yaml up -d
python3 -m bytewax.run src/test.py 
```
