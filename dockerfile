FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Graphviz
RUN apt-get update && apt-get install -y graphviz

COPY . .

EXPOSE 22009
EXPOSE 22010

CMD [ "python", "mud.py" ]