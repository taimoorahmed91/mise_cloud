# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container to /root
WORKDIR /root

# Copy the requirements file into the container
COPY requirements.txt /root/

# Install vim and other dependencies
RUN apt-get update && apt-get install -y vim

# Script to install each package individually
COPY install_packages.sh /root/install_packages.sh
RUN chmod +x /root/install_packages.sh && /root/install_packages.sh

# Create the required directory structure
RUN mkdir -p /root/ise-landscape

# Copy the content of the local mise folder to the container
COPY ./mise /root/ise-landscape

# Keep the container running
CMD ["tail", "-f", "/dev/null"]

