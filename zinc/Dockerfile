FROM debian

ARG ZINC_FIRST_ADMIN_USER
ARG ZINC_FIRST_ADMIN_PASSWORD

ENV ZINC_FIRST_ADMIN_USER $ZINC_FIRST_ADMIN_USER
ENV ZINC_FIRST_ADMIN_PASSWORD $ZINC_FIRST_ADMIN_PASSWORD

ENV ZINC_TELEMETRY=disabled
ENV DATA_PATH=/data

RUN apt update && apt install curl tar -y && \
    curl -o zinc.tar.gz -L https://github.com/prabhatsharma/zinc/releases/download/v0.1.8/zinc_0.1.8_Linux_x86_64.tar.gz && \
    tar -xvf zinc.tar.gz && \
    mkdir /data

EXPOSE 4080

ENTRYPOINT [ "/zinc" ]
