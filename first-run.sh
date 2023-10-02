sh install.sh

docker-compose up -d

docker exec -i db mysql -u root -pr3Dk7jcPBsSNtoTYxhGX library < initial.sql

docker build --network=host -t py_i . --no-cache
docker run --name py --expose=4000 -p 4000:5000 -d py_i:latest