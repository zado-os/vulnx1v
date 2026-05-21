FROM python:3.11-slim
LABEL maintainer="Hussain Al-zadjali <zado-os>"
LABEL org.opencontainers.image.source="https://github.com/zado-os/devxploit"
LABEL org.opencontainers.image.title="DevXploit"
LABEL org.opencontainers.image.version="4.2.0"

WORKDIR /opt/devxploit
COPY . /opt/devxploit/

RUN pip install --no-cache-dir -r requirements.txt && \
    chmod +x devxploit

VOLUME ["/devxploit/logs"]
ENTRYPOINT ["python3", "devxploit.py"]
CMD ["--help"]
