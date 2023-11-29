FROM python:3-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apk update && \
    apk add --no-cache mariadb-dev build-base pkgconfig
RUN pip3 install -r requirements.txt
COPY app.py .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
