# The lab's socket-mode image (RFC 0017 §2a): the image supplies the docker
# CLI; the daemon is the host's, mounted by runtime.docker: socket.
FROM python:3.13-slim
ADD https://download.docker.com/linux/static/stable/x86_64/docker-27.3.1.tgz /tmp/docker.tgz
RUN tar -xzf /tmp/docker.tgz -C /tmp && mv /tmp/docker/docker /usr/local/bin/docker \
    && rm -rf /tmp/docker /tmp/docker.tgz
