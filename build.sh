docker rmi $(docker images -a -q)

docker build ./ -t gsheet_service
