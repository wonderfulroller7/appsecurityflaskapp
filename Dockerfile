#Specify a base image
FROM ubuntu:18.04

# Install pip
RUN apt-get update && apt-get install -y \
    python3-pip

#State a work directory
WORKDIR /usr/app

# Copy the requirements file to the docker container file
# to avoid the building the project multiple times 
COPY ./requirements.txt ./
#Install some dependencies
RUN pip install -r requirements.txt
# Copy the rest of the files to the working directory
COPY ./ ./

#Default command
CMD ["flask", "run", "--host=0.0.0.0"]
