FROM node:7

RUN npm install -g bower

COPY ./deployment/packagefiles/bower.txt ./

RUN awk '{system("bower install --allow-root " $0)}' bower.txt
