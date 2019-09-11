#!/bin/bash


echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker push bmltenabled/tomato:latest
docker push bmltenabled/tomato:$TRAVIS_COMMIT
