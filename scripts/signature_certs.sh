#!/bin/bash

if [ ! -d ".certs" ]; then
    # If the directory doesn't exist, create it
    mkdir .certs
    echo "The .certs directory has been created."
else
    echo "The .certs directory already exists."
fi
cd .certs

openssl genpkey -algorithm RSA -out signature_private.pem -pkeyopt rsa_keygen_bits:2048

cd ..

echo 'The singature keys were successfully created'