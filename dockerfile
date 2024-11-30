FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME d:\data\mud-images

EXPOSE 60049

CMD [ "python", "./mud.py" ]