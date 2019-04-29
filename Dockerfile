FROM node:10

WORKDIR /opt/ddig
COPY . .

RUN \
    apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get update && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    apt-get install -y python3-tk

RUN pip3 install -r requirements.txt

WORKDIR /opt/ddig/frontend
RUN npm install -g create-react-app react-scripts
RUN npm install
RUN npm run build

WORKDIR /opt/ddig

EXPOSE 5000 5000
CMD ["flask" "run"]
