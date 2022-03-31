FROM python:3.9.7

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

# Copy the a2p2v source code
COPY --chown=python pentest-a2p2v-core /home/python/pentest-a2p2v-core
COPY --chown=python pentest-a2p2v-gui /home/python/pentest-a2p2v-gui

# Install the a2p2v core software and requirements
WORKDIR /home/python/pentest-a2p2v-core

# Install the a2p2v core software and requirements
RUN python -m pip install .

# TODO:
# - Load the capabilities.xml file
WORKDIR /home/python/pentest-a2p2v-gui
RUN python -m pip install -r requirements.txt

# Copy the GUI configuration file
COPY --chown=python config/gui/default.json /home/python/pentest-a2p2v-gui/config/default.json

# Copy the A2P2v configuration files (a2p2v.config and metasploit definitions)
RUN mkdir -p /home/python/.config
COPY --chown=python config/core /home/python/.config/a2p2v

# Update the PATH and activate the venv in the .bashrc
RUN echo "export PATH=/home/python/.local/bin:$PATH" >> /home/python/.bashrc
RUN echo "source /home/python/venv/bin/activate" >> /home/python/.bashrc

# Load the a2p2v capabilities definitions
RUN a2p2v --importdb /home/python/.config/a2p2v/capabilities.xml
# Expose the port from the GUI
EXPOSE 3000

# Run the GUI
CMD python a2p2v_gui_server.py
