FROM node:24-alpine

WORKDIR /frontend

EXPOSE 5173

COPY /package.json .
RUN npm update -g npm && npm install

COPY . .
