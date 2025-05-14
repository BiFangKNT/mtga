#!/bin/bash

while true; do
    read -p "Do you want to generate ca cert and key? [yes/no] " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit 1;;
        * ) echo "Please answer yes or no.";;
    esac
done

openssl genrsa -out ca.key 2048
openssl req -new -x509 -extensions v3_ca -days 36500 -key ca.key -out ca.crt -config <(cat openssl.cnf v3_ca.cnf)
