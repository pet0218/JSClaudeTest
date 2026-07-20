FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install --omit=dev

COPY server.js ./
COPY src/data ./src/data

EXPOSE 3001

CMD ["node", "server.js"]
