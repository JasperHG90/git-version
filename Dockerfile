FROM bitnami/git:2.46.2

COPY git_version.sh /git_version.sh
COPY entrypoint.sh /entrypoint.sh

RUN ["chmod", "+x", "/git_version.sh"]
RUN ["chmod", "+x", "/entrypoint.sh"]

ENTRYPOINT [ "/entrypoint.sh" ]
