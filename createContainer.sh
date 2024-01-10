#!/bin/bash
docker rm ims-server-container
docker run --privileged -d -p 80:80 --restart always --name ims-server-container ims-server
docker stop ims-server-container