### How to create ssl key and crt
#### Generate unencrypted private key
``` bash
openssl genrsa -out localhost.key 2048
```

#### Create certificate signing request (CSR)
``` bash
openssl req -new -key localhost.key -out localhost.csr -subj "/CN=localhost"
```

#### Generate self-signed certificate
``` bash
openssl x509 -req -days 365 -in localhost.csr -signkey localhost.key -out localhost.crt
```