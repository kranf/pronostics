!#/usr/bin/bash
docker run --name mongotest -v $PWD/mongo-data:/data/db -p 27017:27017 -d mongotest
