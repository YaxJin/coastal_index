FROM python:3.8-buster
LABEL  maintainer="qooq147852@gmail.com"

COPY . /app
WORKDIR /app

# ADD . /app

RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["flask/router.py"]