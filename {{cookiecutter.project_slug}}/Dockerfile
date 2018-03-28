FROM python:3.6-slim
ARG SETTINGS=development
RUN apt-get update && apt-get install -y --no-install-recommends \
            build-essential nginx supervisor git gettext&&\
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements requirements

RUN pip install --no-cache-dir -r requirements/${SETTINGS}.txt

COPY .. .
RUN chown -R www-data:www-data .

COPY supervisor.conf /etc/supervisor/conf.d/

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log \
    && mkdir /run/uwsgi && chown www-data:www-data /run/uwsgi

ENTRYPOINT [ "./entrypoint.sh" ]

VOLUME [ "/usr/src/app" ]

EXPOSE 80

CMD [ "/usr/bin/supervisord" ]
