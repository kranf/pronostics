#!/bin/sh

DOCKER_IMAGE_NAME='mongotest'

if [ "$(docker ps | grep -c "$DOCKER_IMAGE_NAME")" -gt 0 ]; then
  echo "Container $DOCKER_IMAGE_NAME already running"
  exit 0
fi

if [ "$(docker container ls -a | grep -c "$DOCKER_IMAGE_NAME")" -gt 0 ]; then
  echo "Starting $DOCKER_IMAGE_NAME"
  docker start "$DOCKER_IMAGE_NAME"
  exit 0
fi

if [ "$(docker image ls -a | grep -c "$DOCKER_IMAGE_NAME")" -eq 0 ]; then
  echo "Building $DOCKER_IMAGE_NAME"
  docker build "$DOCKER_IMAGE_NAME"
  docker run --name "$DOCKER_IMAGE_NAME" -v "$PWD"/mongo-data:/data/db -p 27017:27017 -d "$DOCKER_IMAGE_NAME"
  exit 0
fi
