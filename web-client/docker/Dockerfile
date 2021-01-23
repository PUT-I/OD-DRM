FROM node:lts-alpine

# make the 'app' folder the current working directory
WORKDIR ./app/

# copy both 'package.json' and 'package-lock.json' (if available)
COPY ./package.json ./

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY ./public/* ./public/
COPY ./src/ ./src/

# install project dependencies
RUN npm install

EXPOSE 8080
ENTRYPOINT ["npm", "run", "serve"]
