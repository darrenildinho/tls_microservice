from flask import Flask, send_from_directory, send_file
import cert_generator

app = Flask(__name__)

ca_cert_path = "/app/certs/CA/ca-cert.pem"
ca_key_path = "/app/certs/CA/ca-key.pem"
ca_csr_path = '/app/certs/CA/CA.csr'
ca_signed_cert='/app/certs/CA/ca-signed-cert.pem'

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/ca-cert")
def generate_ca_cert():
    # code for generating tls cert using open ssl library through shell command
    #Should just be a get request
    #do  cert bundle in another function
    #could create seperate library for the actual generation of these certs and use this function as the api handler like in original code


    cert_generator.generate_ca_cert()
    cert_generator.generate_server_cert_bundle()

    return send_file(ca_signed_cert, as_attachment=True)






@app.route("/server-cert-bundle")
def generate_server_cert_bundle():
    cert_options="/C=IT/ST=PR/L=Parma/O=MineMeld/OU=TBD/CN=please use a real CA/emailAddress=techbizdev@paloaltonetworks.com"
    cert_generator.generate_server_cert(cert_options)

    return "This will be a POST request with the necessary info for generating the server cert and key"





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)