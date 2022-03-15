To run backend install docker, from the directory with the docker-compose file run
    
    docker-compose -f docker-compose.dev.yml up --build

To test the api run:
    
    curl localhost:8000/api/load

Port is mapped to 8000 (configurable in docker compose file)
