from flask import request
from flask_restx import Namespace
from werkzeug.datastructures import FileStorage
from flask_restx import Resource, reqparse
import os
import hashlib
import socket

import logging
import logging.handlers
import socket

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
formatter_costom = logging.Formatter('%(message)s')
base_msg_line = "Logger: 0|TCP|v1|"
ip_msg_line = "00014|WebLoglevel=notice src="
file_msg_line = "00015|WebLoglevel=notice src="
domain_msg_line = "00016|WebLoglevel=notice src="

handler.formatter = formatter_costom
logger.addHandler(handler)

# STATIC PATH
UPLOAD_DIRECTORY = '/tmp/file'
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

api = Namespace('upload', description='File upload operations')
server_port = 443

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)


def get_server_ip():
    hostname = socket.gethostname()
    server_ip = socket.gethostbyname(hostname)
    return server_ip


@api.route("/file")
class file_upload(Resource):
    @api.expect(upload_parser)
    @api.doc("get_file", body={"file": "formData"})
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance

        file_path = os.path.join(UPLOAD_DIRECTORY, uploaded_file.filename)

        # Read the binary data of the file
        uploaded_file.save(file_path)
        with open(file_path, 'rb') as f:
            file_data = f.read()
        file_size = os.path.getsize(file_path)
        os.remove(file_path)

        # file hash calc
        hash_md5 = hashlib.md5(file_data).hexdigest()
        hash_sha1 = hashlib.sha1(file_data).hexdigest()
        hash_sha256 = hashlib.sha256(file_data).hexdigest()

        # file save
        file_path_save = os.path.join(UPLOAD_DIRECTORY, hash_sha256)
        uploaded_file.save(file_path_save)

        server_ip = get_server_ip()

        # print(hash_md5, hash_sha1, hash_sha256, server_ip, server_port, file_size)
        msg = f"{base_msg_line}{file_msg_line}{request.remote_addr} dst={server_ip} dpt={server_port} app=HTTPS sha256={hash_sha256} sha1={hash_sha1} md5={hash_md5} filesize={file_size}"
        logger.info(msg)

        return {"msg": "success"}


@api.route("/ip/<ip>")
class ip_upload(Resource):
    @api.doc("get_ip")
    def get(self, ip):
        server_ip = get_server_ip()

        # print(ip, server_ip, server_port)
        msg = f"{base_msg_line}{ip_msg_line}{request.remote_addr} dst={server_ip} dpt={server_port} app=HTTPS ip={ip}"
        logger.info(msg)

        return {"msg": "success"}


@api.route("/hash/<hash>")
class hash_upload(Resource):
    @api.doc("get_hash")
    def get(self, hash):
        server_ip = get_server_ip()

        # print(hash, server_ip, server_port)
        msg = f"{base_msg_line}{file_msg_line}{request.remote_addr} dst={server_ip} dpt={server_port} app=HTTPS sha256={hash}"
        logger.info(msg)

        return {"msg": "success"}


@api.route("/domain/<domain>")
class domain_upload(Resource):
    @api.doc("get_domain")
    def get(self, domain):
        server_ip = get_server_ip()

        # print(domain, server_ip, server_port)
        msg = f"{base_msg_line}{domain_msg_line}{request.remote_addr} dst={server_ip} dpt={server_port} app=HTTPS domain={domain}"
        logger.info(msg)

        return {"msg": "success"}
