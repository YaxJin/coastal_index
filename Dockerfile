FROM tensorflow/tensorflow
LABEL  maintainer="qooq147852@gmail.com"

COPY . /app
WORKDIR /app

# ADD . /app

RUN pip install -r requirements.txt
# RUN pip install tensorflow tensorflow-gpu 
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["flask/router.py"]