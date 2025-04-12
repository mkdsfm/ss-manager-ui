FROM debian:bullseye

RUN apt-get update && apt-get install -y \
    shadowsocks-libev \
    simple-obfs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY config.json /etc/shadowsocks-libev/config.json

RUN setcap 'cap_net_bind_service=+ep' /usr/bin/ss-server

EXPOSE 443

CMD ["ss-server", "-c", "/etc/shadowsocks-libev/config.json"]
