FROM conoria/alpine-pandoc:latest
MAINTAINER Borodin Gregory <grihabor@mail.ru>

RUN apk update \
 && apk add python3 py3-pip \
 && pip3 install sphinx

CMD ["/bin/sh"]
