FROM alpine:3.11.5

ENV WORKDIR='/app'
COPY . /app
WORKDIR $WORKDIR

RUN apk update && apk upgrade && \
    apk add bash bash-completion curl python3 python3-dev vim && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    pip3 install . && \
    mkdir -p instance && \
    python3 -c 'import os; print(os.urandom(16))' > instance/config.py \
    chmod 777 $WORKDIR/scripts/entrypoint.sh

EXPOSE 5000

CMD flask run --host 0.0.0.0
#CMD sleep 600
