#!/bin/bash

if [ ! -d ".certs" ]; then
    mkdir .certs
    echo "The .certs directory has been created."
else
    echo "The .certs directory already exists."
fi

cd .certs

openssl genrsa -out jwt_private.pem 2048
openssl rsa -in jwt_private.pem -outform PEM -pubout -out jwt_public.pem

cd ..

echo 'The jwt keys were successfully created'