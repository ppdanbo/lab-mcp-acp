### how to create ssl key and crt
REM Generate unencrypted private key
openssl genrsa -out localhost.key 2048

REM Create certificate signing request (CSR)
openssl req -new -key localhost.key -out localhost.csr -subj "/CN=localhost"

REM Generate self-signed certificate
openssl x509 -req -days 365 -in localhost.csr -signkey localhost.key -out localhost.crt
