FROM python:latest

# Update the system packages
RUN apt update 

# Add Python user
RUN useradd -rm -d /home/python -s /bin/bash python 

# Switch to the Python User
USER python

# Change to the python home directory
WORKDIR /home/python

# Set the PATH in the build environment
ENV VIRTUAL_ENV=/home/python/venv
ENV PATH="$VIRTUAL_ENV/bin:/home/python/.local/bin:$PATH"

# Create a virtualenv
RUN python -m venv venv

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install wheel
RUN python -m pip install wheel

# Copy the flask hmi source code
COPY --chown=python . /home/python/flaskhmi

# Change to the flask HMI directory
WORKDIR /home/python/flaskhmi

# Install the requirements
RUN python -m pip install -r requirements.txt

# Update the PATH and activate the venv in the .bashrc
RUN echo "export PATH=/home/python/.local/bin:$PATH" >> /home/python/.bashrc
RUN echo "source /home/python/venv/bin/activate" >> /home/python/.bashrc

# Expose the port to connect
EXPOSE 8800

# Run the Flask HMI web server
CMD python -m flaskhmi
