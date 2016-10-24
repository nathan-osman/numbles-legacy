FROM ubuntu:16.04
MAINTAINER Nathan Osman <nathan@quickmediasolutions.com>

# Install packages from APT
RUN \
    apt-get update && \
    apt-get install -y python-pip python-dev libpq-dev uwsgi uwsgi-plugin-python && \
    rm -rf /var/lib/apt/lists/*

# Install the PIP requirements
COPY requirements.txt /root/
RUN pip install -r /root/requirements.txt

# Copy the source file and management script
COPY numbles /root/numbles
COPY manage.py /usr/local/bin

# Run the application through uWSGI
CMD [ \
    "uwsgi", \
    "--http-socket", "0.0.0.0:80", \
    "--plugin", "python", \
    "--chdir", "/root", \
    "--module", "numbles.wsgi" \
]

# Set PYTHONPATH so that manage.py can find the script
ENV PYTHONPATH=/root

# Expose port 80
EXPOSE 80
