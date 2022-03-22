To run backend install docker, from the directory with the docker-compose file run
    
    docker-compose -f docker-compose.dev.yml up --build

To test the api run:
    
    curl localhost:8000/api/load

Port is mapped to 8000 (configurable in docker compose file)

To test file upload:
    cd into testcases/upload folder:
        curl -F 'file=@c.csv' http://127.0.0.1:8000/uploader

To test file download:
    cd into testcases/download folder:
        curl http://127.0.0.1:8000/downloader/a.csv  --output yourFileName.csv

Cool guide(s) to start out with:

    https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
    https://pythonise.com/series/learning-flask/sending-files-with-flask
    https://towardsdatascience.com/understanding-python-imports-init-py-and-pythonpath-once-and-for-all-4c5249ab6355

Refer to flask documentation:

    https://flask.palletsprojects.com/en/2.0.x/
    https://flask.palletsprojects.com/en/2.0.x/api/#flask.send_from_directory
    https://docs.python.org/3/library/json.html
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_json.html

To shell into container for debugging

    docker exec -it {container_id} sh 
    retrieve the container_id from: docker ps 