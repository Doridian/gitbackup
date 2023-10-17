FROM alpine

ENV GITHUB_TOKEN=
ENV GITHUB_ORGANIZATIONS=foxCaves,FoxDenHome,FoxBukkit,MoonHack,PawNode,SpaceAgeMP,WSVPN

RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN apk --no-cache add python3 py3-cffi py3-pip git && pip3 install -r requirements.txt

COPY . /app

RUN mkdir -p /app/backups
VOLUME /app/backups

ENTRYPOINT [ "python3", "loop.py" ]
