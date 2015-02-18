FROM ubuntu:14.04

MAINTAINER Jay Luker <jay_luker@harvard.edu>

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install \
    python-pip git-core build-essential curl \
    python-dev libxml2-dev libxslt1-dev libpq-dev \
    && apt-get clean \
    && rm -Rf /var/cache/apt

ADD . /src

RUN pip install -r /src/requirements/dce.txt

EXPOSE 8000

WORKDIR /src

CMD ["gunicorn", "-b", "0.0.0.0", "-c", "gunicorn.py", "dce_course_admin.wsgi", "--log-file", "-"]
