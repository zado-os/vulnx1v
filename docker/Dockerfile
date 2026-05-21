FROM python:3-alpine
MAINTAINER ZADO-OS Roger OS

LABEL name DevXploit
LABEL src "https://github.com/zado-os/devxploit"
LABEL creator zado-os
LABEL desc "DevXploit — CMS detection, Exploits Scan, dorks, DNS, shell injector"

RUN apk add --no-cache git && \
    git clone https://github.com/zado-os/devxploit.git /opt/devxploit

RUN addgroup -S devxploit && adduser -S -G devxploit devxploit
RUN chown -R devxploit:devxploit /opt/devxploit

USER devxploit
WORKDIR /opt/devxploit

RUN pip install --user --upgrade pip && \
    pip install --user -r ./requirements.txt

VOLUME [ "/devxploit" ]

ENTRYPOINT [ "python3", "devxploit.py" ]
CMD [ "--help" ]
