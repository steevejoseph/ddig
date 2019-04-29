FROM node:10

WORKDIR /opt/app
COPY package.json .
COPY . .

RUN npm i -g serve
RUN npm install

CMD ["npm", "start"]