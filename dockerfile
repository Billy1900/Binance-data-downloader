FROM python:3.8-slim-buster
# The latest alpine images don't have some tools like (`git` and `bash`).
# Adding git, bash and openssh to the image
# RUN apt update && apt upgrade && \
#     apt add --no-cache bash git openssh
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "main.py"]