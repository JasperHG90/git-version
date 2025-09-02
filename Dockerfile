FROM alpine/git:v2.49.1

RUN apk update && apk add bash

COPY git_version.sh /git_version.sh
COPY entrypoint.sh /entrypoint.sh

RUN ["chmod", "+x", "/git_version.sh"]
RUN ["chmod", "+x", "/entrypoint.sh"]

ENTRYPOINT [ "/entrypoint.sh" ]
