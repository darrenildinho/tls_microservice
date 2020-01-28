import subprocess
import os
import tarfile
from shutil import copyfile

ca_bundle = "/app/certs/CA/bundle"
ca_cert_path = "/app/certs/CA/ca-cert.pem"
ca_key_path = "/app/certs/CA/ca-key.pem"
ca_csr_path = '/app/certs/CA/CA.csr'
ca_signed_cert = '/app/certs/CA/ca-signed-cert.pem'
ca_subj = '/C=NL/ST=NH/L=Ams/O=DKCorp/OU=SOC/CN=ca.server/emailAddress=darren@email.me'

client_dir = '/app/certs/client'
server_dir = '/app/certs/Server'


def generate_ca_cert():

    #openssl command for generating the public CA Cert and private key file
    cert_options = ['openssl', 'req', '-x509', '-newkey', 'rsa:4096', '-sha256', '-nodes', '-keyout', ca_key_path,
                    '-out', ca_cert_path, '-subj', ca_subj]
    run_shell_command(cert_options)
    sign_ca_cert()

    try:
        os.mkdir(ca_bundle)
    except OSError:
        print("Problem creating "+ca_bundle+" directory")

    copyfile(ca_cert_path, ca_bundle+"/ca-cert.pem")
    copyfile(ca_signed_cert, ca_bundle+"/ca.csr")

    create_tarball(ca_bundle, "ca-bundle.tgz")


def sign_ca_cert():
    create_ca_self_signing_request()

    sign_cert = ['openssl', 'x509', '-req', '-days', '365', '-in', ca_csr_path, '-CA', ca_cert_path, '-CAkey',
                ca_key_path, '-CAcreateserial', '-out', ca_signed_cert]

    run_shell_command(sign_cert)


def create_ca_self_signing_request():
    sign_request = ['openssl', 'req', '-new', '-sha256', '-key', ca_key_path, '-out', ca_csr_path, '-subj', ca_subj]
    run_shell_command(sign_request)


def generate_private_key(key_file):

    gen_key = ['openssl', 'genrsa', '-out', key_file, '4096']

    run_shell_command(gen_key)


def run_shell_command(command):
    #TODO Add error handling to places that use this

    #Need to look at this error handling more, Very generic but for some reason if I try to return stderr it causes
    #all commands to fail running. Added very generic error handling for now as the shell commands dont rely on
    #output of previous commands so I'll get away with it.

    # process = subprocess.Popen(command,
    #                            stderr=subprocess.PIPE
    #                            )
    #
    # stdout, stderr = process.communicate()
    #
    # return stdout, stderr

    try:
        subprocess.check_call(command, stdout=subprocess.PIPE
                              )
    except subprocess.CalledProcessError as e:
        command_string = ' '.join([str(x) for x in command])
        return "Command "+command_string + "Returned with Error code -"+e.returncode


def generate_ca_signed_cert(csr_file, signed_cert):

    cert_options = ['openssl', 'x509', '-req', '-days', '365', '-in', csr_file, '-CA', ca_cert_path, '-CAkey',
                    ca_key_path, '-CAcreateserial', '-out', signed_cert]
    run_shell_command(cert_options)


def generate_signing_request(key_file, csr_file, subj):
    sign_options = ['openssl', 'req', '-new', '-sha256', '-key', key_file, '-out', csr_file, '-subj', subj]
    run_shell_command(sign_options)


def create_server_cert_bundle(server_name, cert_subj):

    server_cert_dir = server_dir+"/"+server_name
    try:
        os.mkdir(server_cert_dir)
    except OSError:
        print("Problem creating "+server_name+" directory")
    server_key = server_cert_dir+"/"+server_name+"-key.pem"
    server_csr = server_cert_dir+"/"+server_name+"-csr.pem"

    server_signed_cert = server_cert_dir+"/"+server_name+"-signed-cert.pem"
    output_tar = server_name+"-cert-bundle.tgz"

    generate_private_key(server_key)
    generate_signing_request(server_key, server_csr, cert_subj)
    generate_ca_signed_cert(server_csr, server_signed_cert)

    create_tarball(server_cert_dir, output_tar)

    return server_cert_dir+"/"+output_tar


def create_tarball(cert_dir_path, output_name):

    with tarfile.open(cert_dir_path+"/"+output_name, "w:gz") as tar:
        tar.add(cert_dir_path, arcname=os.path.basename(cert_dir_path))


def create_client_cert_bundle(client_name, cert_subj):
    client_cert_dir = client_dir+"/"+client_name
    try:
        os.mkdir(client_cert_dir)
    except OSError:
        print("Problem creating "+client_name+" directory")
    server_key = client_cert_dir+"/"+client_name+"-key.pem"
    server_csr = client_cert_dir+"/"+client_name+"-csr.pem"

    server_signed_cert = client_cert_dir+"/"+client_name+"-signed-cert.pem"
    output_tar = client_name+"-cert-bundle.tgz"

    generate_private_key(server_key)
    generate_signing_request(server_key, server_csr, cert_subj)
    generate_ca_signed_cert(server_csr, server_signed_cert)

    create_tarball(client_cert_dir, output_tar)

    return client_cert_dir+"/"+output_tar
