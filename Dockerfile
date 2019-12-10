#Specify a base image
FROM python:alpine

#Copy the local file to the docker container file
COPY ./ ./
#Install some dependencies
RUN pip3 install -r requirements.txt

#Default command
CMD ["flask", "run", "--host=0.0.0.0"]
