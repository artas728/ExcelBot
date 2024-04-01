# Use the specified Python base image
FROM python:3.10.9-buster as build

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Add the requirements.txt file to the root directory inside the container
ADD requirements.txt /

# Install the Python dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Copy everything from the current directory into the /app directory inside the container
COPY . /chatbot_interface/

# Set the working directory to /app
WORKDIR /chatbot_interface

# Command to run the Panel application when the container starts
CMD ["panel", "serve", "main.py", "--address", "0.0.0.0", "--port", "8080", "--allow-websocket-origin=*", "--num-procs", "0"]

# Inform Docker that the container listens on the specified network port at runtime
EXPOSE 8080