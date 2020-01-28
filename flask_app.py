from flask import Flask, send_file, request
from cert_generator import generate_ca_cert, create_server_cert_bundle

app = Flask(__name__)

ca_bundle = "/app/certs/CA/bundle/ca-bundle.tgz"
ca_cert_path = "/app/certs/CA/ca-cert.pem"
ca_key_path = "/app/certs/CA/ca-key.pem"
ca_csr_path = '/app/certs/CA/CA.csr'
ca_signed_cert = '/app/certs/CA/ca-signed-cert.pem'


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/ca-cert-bundle", methods=['GET'])
def get_ca_cert_bundle():

    return send_file(ca_bundle, as_attachment=True)


@app.route("/unsigned-ca-cert", methods=['GET'])
def get_ca_cert():

    return send_file(ca_cert_path, as_attachment=True)


@app.route("/server-cert-bundle", methods=['POST'])
def get_server_cert_bundle():

    post_data = request.get_json()
    server_name = post_data['servername']
    cert_subj = post_data['cert_data']
    server_cert_tar = create_server_cert_bundle(server_name, cert_subj)

    return send_file(server_cert_tar, as_attachment=True)


@app.route("/client-cert-bundle", methods=['POST'])
def get_client_cert_bundle():

    post_data = request.get_json()
    client_name = post_data['clientname']
    cert_subj = post_data['cert_data']
    client_cert_tar = create_server_cert_bundle(client_name, cert_subj)

    return send_file(client_cert_tar, as_attachment=True)


if __name__ == "__main__":
    generate_ca_cert()
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
