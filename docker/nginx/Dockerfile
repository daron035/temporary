FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf

ADD ./docker/nginx/development/default.conf /etc/nginx/conf.d/nginx.conf

CMD ["nginx-debug", "-g", "daemon off;"]
