FROM node:22.16-alpine

RUN npm install -g http-server

WORKDIR /

COPY package*.json ./

RUN npm install

COPY . app

RUN cd app && npm run build

WORKDIR /app

EXPOSE 8080
CMD [ "http-server", "dist" ]