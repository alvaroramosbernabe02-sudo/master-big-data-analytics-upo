FROM eclipse-temurin:11-jre
ARG HBASE_VERSION=2.5.10
RUN apt-get update && apt-get install -y --no-install-recommends curl procps && rm -rf /var/lib/apt/lists/* \
 && curl -fsSL https://archive.apache.org/dist/hbase/${HBASE_VERSION}/hbase-${HBASE_VERSION}-hadoop3-bin.tar.gz | tar -xz -C /opt \
 && ln -s /opt/hbase-${HBASE_VERSION}-hadoop3 /opt/hbase
ENV HBASE_HOME=/opt/hbase PATH=$PATH:/opt/hbase/bin HBASE_MANAGES_ZK=false HBASE_HEAPSIZE=512m
WORKDIR /opt/hbase
