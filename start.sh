#to copy test folders into the container
docker cp tests/. jupyter-user2:/tests
docker cp testFramework.sh jupyter-user2:/testFramework.sh
sudo docker exec -it -w / jupyter-user2 /bin/bash 