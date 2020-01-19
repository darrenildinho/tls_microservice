import subprocess
import os
import tarfile


ca_cert_path = "/app/certs/CA/ca-cert.pem"
ca_key_path = "/app/certs/CA/ca-key.pem"
ca_csr_path = '/app/certs/CA/CA.csr'
ca_signed_cert = '/app/certs/CA/ca-signed-cert.pem'
ca_subj = '/C=NL/ST=NH/L=Ams/O=DKCorp/OU=SOC/CN=ca.server/emailAddress=darren@email.me'

client_dir = '/app/certs/client'
server_dir = '/app/certs/Server'

#server_subj = '/C=NL/ST=NH/L=Ams/O=TelcoMedia/OU=TV/CN=ca.server/emailAddress=telcomediasoc@telcomedia.no'


def generate_ca_cert():


    #openssl command for generating the public CA Cert and private key file
    cert_options = ['openssl','req','-x509','-newkey','rsa:4096','-sha256','-nodes','-keyout',ca_key_path,'-out',
                    ca_cert_path,'-subj',ca_subj]
    run_shell_command(cert_options)
    sign_ca_cert()

    #TODO package file into a zip perhaps?


def sign_ca_cert():
    create_ca_self_signing_request()

    sign_cert= ['openssl','x509','-req','-days','365','-in',ca_csr_path,'-CA',ca_cert_path,'-CAkey',ca_key_path,
                '-CAcreateserial','-out',ca_signed_cert]

    run_shell_command(sign_cert)


def create_ca_self_signing_request():
    sign_request = ['openssl','req','-new','-sha256','-key',ca_key_path,'-out',ca_csr_path,'-subj',ca_subj]
    run_shell_command(sign_request)

def generate_private_key(key_file):

    #take in file name as this can be used for servers and clients.

    #TODO take -subj field as variable as it should be different each request
    key_options=['openssl','req','-x509','-newkey','rsa:4096','-nodes','-keyout',key_file,'-subj',
                 '/C=NL/ST=NH/L=Ams/O=MineMeld/OU=TBD/'
                 'CN=ca.server/emailAddress=darren@email.me']

    gen_key = ['openssl', 'genrsa', '-out', key_file, '4096']

    run_shell_command(gen_key)



def run_shell_command(command):
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE)

    stdout, stderr = process.communicate()

    return stdout,stderr

def generate_ca_signed_cert(csr_file,signed_cert):
    cert_options=['openssl', 'x509', '-req', '-days', '365', '-in', csr_file, '-CA', ca_cert_path, '-CAkey', ca_key_path,
                  '-CAcreateserial', '-out', signed_cert]
    run_shell_command(cert_options)


def generate_signing_request(key_file,csr_file,subj):
    sign_options = ['openssl', 'req', '-new','-sha256','-key',key_file,'-out',csr_file, '-subj',subj]
    run_shell_command(sign_options)



def generate_server_cert_bundle():

    #TODO take in a dictionary with these values stored in it from original call

    server_name = "server1"
    server_cert_dir=server_dir+"/"+server_name
    try:
        os.mkdir(server_cert_dir)
    except:
        print("NO")
    server_key=server_cert_dir+"/"+"server1-key.pem"
    server_csr = server_cert_dir+"/"+"server1-csr.pem"
    server_subj= '/C=NL/ST=NH/L=Ams/O=TelcoMedia/OU=TV/CN=ca.server/emailAddress=telcomediasoc@telcomedia.no'
    server_signed_cert = server_cert_dir+"/"+server_name+"-signed-cert.pem"
    print("All good")

    generate_private_key(server_key)
    print("all good again")
    generate_signing_request(server_key, server_csr,server_subj)
    print("all great")
    generate_ca_signed_cert(server_csr,server_signed_cert)

    #TODO generate tar with server certs
    create_tarball(server_cert_dir,server_name+'cert-bundle.tgz')


def create_tarball(cert_dir_path, output_name):

    with tarfile.open(cert_dir_path+"/"+output_name, "w:gz") as tar:
        tar.add(cert_dir_path, arcname=os.path.basename(cert_dir_path))


def create_client_cert_bundle():
    pass