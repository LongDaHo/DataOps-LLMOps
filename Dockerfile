FROM quay.io/debezium/connect-base:1.9

LABEL maintainer="Debezium Community"

ENV DEBEZIUM_VERSION="2.1.4.Final" \
    MAVEN_REPO_CENTRAL="" \
    MAVEN_REPOS_ADDITIONAL="" \
    MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR \
    MONGODB_MD5=3060b16543ba0fe2cd8c56124d361054 

RUN docker-maven-download debezium mongodb "$DEBEZIUM_VERSION" "$MONGODB_MD5"