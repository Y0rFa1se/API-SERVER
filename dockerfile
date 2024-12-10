#NOT TESTED YET!!

FROM nginx

COPY nginx.conf /etc/nginx/nginx.conf

RUN apt-get update && apt-get install -y certbot python3-certbot-nginx cron
RUN certbot --nginx --non-interactive --agree-tos --email "y0rfa1se0@gmail.com" -d "y0rfa1se.duckdns.org"
RUN echo "0 3 * * * certbot renew --quiet && nginx -s reload" > /etc/cron.d/certbot-renew
RUN chmod 0644 /etc/cron.d/certbot-renew
RUN service cron start

EXPOSE 443 80

CMD ["nginx", "-g", "daemon off;"]