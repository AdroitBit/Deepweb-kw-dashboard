# FROM node:alpine
FROM node:21-alpine3.18

WORKDIR /app



RUN npm install -g npm@10.5.2
# RUN npm install --global yarn --force
COPY ./package.json ./package.json
COPY ./yarn.lock ./yarn.lock
RUN yarn

COPY ./public/ ./public/
COPY ./src/ ./src/
COPY ./.eslintrc.cjs ./.eslintrc.cjs
COPY ./index.html ./index.html
COPY ./tsconfig.json ./tsconfig.json
COPY ./tsconfig.node.json ./tsconfig.node.json
COPY ./vite.config.ts ./vite.config.ts



EXPOSE 5173
CMD yarn dev --host 0.0.0.0 --port 5173