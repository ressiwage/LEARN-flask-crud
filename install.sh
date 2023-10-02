sudo apt install gnome-terminal
sudo apt remove docker-desktop
sudo rm /usr/local/bin/com.docker.cli
sudo apt-get update
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-cache policy docker-ce
sudo apt install docker-ce


sudo apt-get update
sudo apt-get install docker-compose-plugin
sudo apt install docker-compose