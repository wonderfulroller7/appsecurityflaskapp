#Specify a base image
FROM alpine

#Install some dependencies
RUN pip3 install -r requirements.txt

#Default command
CMD ["flask", "run"]
