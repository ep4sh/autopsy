FROM python
RUN /usr/sbin/adduser --disabled-password --system flask
WORKDIR  /app
COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir
COPY . /app
EXPOSE 5000

ARG FLASK_APP
ARG FLASK_ENV
ENV FLASK_APP=${FLASK_APP}
ENV FLASK_ENV=${FLASK_ENV}
RUN chown -R flask /app && chmod u+x ./entrypoint.sh
USER flask
ENTRYPOINT ["./entrypoint.sh"]
