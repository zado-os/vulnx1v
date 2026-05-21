FROM python:3-alpine
MAINTAINER ZADO-OS Roger OS

LABEL name nexploit
LABEL src "https://github.com/zado-os/nexploit"
LABEL creator zado-os
LABEL desc "Nexploit — CMS detection, Exploits Scan, dorks, DNS, auto shell injector"

RUN apk add --no-cache git && \
    git clone https://github.com/zado-os/nexploit.git /opt/nexploit

RUN addgroup -S nexploit && adduser -S -G nexploit nexploit
RUN chown -R nexploit:nexploit /opt/nexploit

USER nexploit
WORKDIR /opt/nexploit

RUN pip install --user --upgrade pip && \
    pip install --user -r ./requirements.txt

VOLUME [ "/nexploit" ]

ENTRYPOINT [ "python3", "nexploit.py" ]
CMD [ "--help" ]
