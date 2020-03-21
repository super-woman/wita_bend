FROM python:3.7-slim

LABEL application="WITA_BEND"

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

# Install requirements
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /usr/apps
WORKDIR /usr/apps
COPY . /usr/
