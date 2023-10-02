sh install.sh

docker-compose up -d

docker exec db /bin/sh -c 'mysql -u root -p"r3Dk7jcPBsSNtoTYxhGX" </initial.sql'
