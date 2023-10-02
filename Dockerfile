FROM python:3.10.8-buster
EXPOSE 4000

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app


# RUN apt-get update && \
#     apt-get install -y locales && \
#     sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
#     dpkg-reconfigure --frontend=noninteractive locales

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
ENV PYTHONUNBUFFERED=1

RUN pip3 install cython

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install wheel 

RUN --mount=type=cache,target=/root/.cache/pip \
        pip install -r requirements.txt

# RUN apt-get update 

COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["python/main.py" ]