docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes -e MYSQL_DATABASE=microblog -e MYSQL_USER=microblog -e MYSQL_PASSWORD=microblog mysql/mysql-server:5.7
docker run --name elasticsearch -d -p 9200:9200 -p 9300:9300 --rm -e "discovery.type=single-node" elasticsearch/elasticsearch:7.2.0
docker build -t microblog:latest .
docker run --name microblog -d -p 8000:5000 --rm -e SECRET_KEY=my-secret-key --link mysql:dbserver -e DATABASE_URL=mysql+pymysql://microblog:microblog@dbserver/microblog --link elasticsearch:elasticsearch -e ELASTICSEARCH_URL=http://elasticsearch:9200 microblog:latest
curl http://192.168.99.100:8000
docker ps
docker logs microblog
