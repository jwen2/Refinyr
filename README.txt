To run backend install docker, from the directory with the docker-compose file run
    
    docker-compose -f docker-compose.dev.yml up --build

To test the api run:
    
    curl localhost:8000/api/load

Port is mapped to 8000 (configurable in docker compose file)

To test file upload:
    cd into testcases folder:
        curl -F 'file=@a.csv' http://127.0.0.1:5000/uploader

Cool guide to start out with for handling file uploads with flask:

    https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask