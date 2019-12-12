#Specify a base image
FROM python:alpine

#State a work directory
WORKDIR /usr/app

# Copy the requirements file to the docker container file
# to avoid the building the project multiple times 
COPY ./requirements.txt ./
#Install some dependencies
RUN pip3 install -r requirements.txt
# Copy the rest of the files to the working directory
COPY ./ ./

#Default command
CMD ["flask", "run", "--host=0.0.0.0"]