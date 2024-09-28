#!/bin/bash

mkdir -p .certs
cd .certs

openssl genrsa -out jwt_private.pem 2048
openssl rsa -in jwt_private.pem -outform PEM -pubout -out jwt_public.pem

cd ..

echo 'The keys were successfully created'