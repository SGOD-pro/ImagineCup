FROM node:22-alpine

RUN useradd -m myuser

WORKDIR /app


COPY package.json package.json
RUN npm ci

COPY . .
RUN chown -R appuser:myuser /app

USER myuser

EXPOSE 8080

RUN npm run build
CMD [ "npm", "start"]