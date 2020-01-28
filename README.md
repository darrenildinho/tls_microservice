# Tls_microservice

A small TLS CA service for generation of cert key pairs for mutual authentication

## Installation

You need to have docker installed to run this.

In the same directory as the DockerFile run the following command to build the container image.

```bash
docker build --tag tls_microservice .
```
  To  start the container run the following:
```bash
docker run -p 5000:5000 tls_microservice:latest
```
# Usage
The container will run on localhost:5000 so any calls will need to be made there.

In order to get the ca cert bundle you will need to make a GET request to the following url

127.0.0.1:5000/ca-cert-bundle

The CA cert bundle includes a signed and unsigned version of the ca certificate.

You can also request just the simple unsigned CA cert via making a GET request to
127.0.0.1:5000/unsigned-ca-cert

The service will allow servers and clients to request certificate bundles to be generated for each host. In order to generate these the host name and subject details for the cert are required. These are passed to the service in a POST request.

In order to get a certificate bundle for your server you need to make a POST request including the server name and the details for the cert generation.

Please note you need to keep the "servername" OR "clientname" and "cert_data" headers for the request or it will fail.

Sample for generating server cert bundle
```bash
wget --header='Content-Type: application/json' --post-data '{"servername":"server5", "cert_data": "/C=IE/ST=WD/L=Kill/O=Mine/OU=TBD/CN=tls_microservice/emailAddress=test@testable.test"}' -O server.tgz http://localhost:5000/server-cert-bundle
```

Sample for generating client cert bundle
```bash
wget --header='Content-Type: application/json' --post-data '{"clientname":"client2", "cert_data": "/C=IE/ST=WD/L=Kill/O=Mine/OU=TBD/CN=tls_microservice/emailAddress=test@testable.test"}' -O server.tgz http://localhost:5000/server-cert-bundle
```

These will return a .tgz file including the hosts public cert, private key and ca signed certificates used for mutual authentication.

