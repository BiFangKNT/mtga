#!/bin/bash

NAME="$1"

openssl genrsa -out "$NAME.key" 2048
openssl pkcs8 -topk8 -nocrypt -in "$NAME.key" -out "$NAME.key.pk8"
rm "$NAME.key"
mv "$NAME.key.pk8" "$NAME.key"
openssl req -reqexts v3_req -sha256 -new -key "$NAME.key" -out "$NAME.csr" -config <(cat openssl.cnf v3_req.cnf "$NAME.cnf") -subj `cat $NAME.subj`
openssl x509 -req -extensions v3_req -days 365 -sha256 -in "$NAME.csr" -CA ca.crt -CAkey ca.key -CAcreateserial -out "$NAME.crt" -extfile <(cat openssl.cnf v3_req.cnf "$NAME.cnf")
