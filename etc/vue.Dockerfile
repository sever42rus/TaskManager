FROM node:latest

RUN npm install -g npm@latest

WORKDIR /frontend

ENV PATH /frontend/node_modules/.bin:$PATH

COPY ./frontend/package.json /frontend/package.json

RUN npm install


