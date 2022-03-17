To run backend install docker, from the directory with the docker-compose file run
    
    docker-compose -f docker-compose.dev.yml up --build

To test the api run:
    
    curl localhost:8000/api/load

Port is mapped to 8000 (configurable in docker compose file)

To test file upload:
    cd into testcases/upload folder:
        curl -F 'file=@a.csv' http://127.0.0.1:8000/uploader

To test file download:
    cd into testcases/download folder:
        curl http://127.0.0.1:8000/downloader/a.csv  --output yourFileName.csv

Cool guide(s) to start out with for handling file uploads with flask:

    https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
    https://pythonise.com/series/learning-flask/sending-files-with-flask

Refer to flask documentation:

    https://flask.palletsprojects.com/en/2.0.x/api/#flask.send_from_directory

To shell into container for debugging

    docker exec -it {container_id} sh 
    retrieve the container_id from: docker ps 