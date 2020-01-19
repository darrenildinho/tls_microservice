FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN apk add openssl
#RUN openssl req  -nodes -new -x509  -keyout server.key -out server.cert -subj "/C=IT/ST=PR/L=Parma/O=MineMeld/OU=TBD/CN=me/emailAddress=darren@email.me"
RUN pip install -r req/requirements.txt
EXPOSE 5000
CMD ["python3","flask_app.py"]