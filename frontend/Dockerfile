FROM node:18.13.0

COPY package.json /workspace/package.json
COPY package-lock.json /workspace/package-lock.json
WORKDIR /workspace

RUN npm install

COPY . /workspace

RUN npm run build

EXPOSE 3000

CMD npm start
