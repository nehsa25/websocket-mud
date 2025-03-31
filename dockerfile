FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME c:\data\mud-images
VOLUME c:\data\certs

EXPOSE 60049

CMD [ "python", "./mud.py" ]