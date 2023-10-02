docker-compose down
docker rm db
docker stop py
docker rm py

docker-compose up -d
docker build -t py_i . --no-cache
docker run --name py --expose=4000 -p 4000:5000 -d py_i:latest