# FROM ubuntu:jammy
FROM zocker160/blender-bpy

#constants & env variables
# ENV BACKEND_HOME = kadcarsnft_api

# 1. nginx setup
RUN apt-get update && apt-get upgrade -y
RUN apt update
RUN apt install python3-pip -y
# RUN apt-get update && apt-get upgrade -y && apt-get install nginx vim -y --no-install-recommends
# RUN apt install software-properties-common -y
# RUN add-apt-repository ppa:deadsnakes/ppa
# RUN apt install python3.10
# RUN apt install python3-pip -y
# COPY nginx.default /etc/nginx/sites-available/default
# RUN ln -sf /dev/stdout /var.log.nginx.access.log
# RUN ln -sf /dev/stderr /var/log/nginx/error.log

# 3. django app setup
RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/app/pip_cache
RUN mkdir -p /usr/src/app/kadcarsnft

# COPY requirements.txt start-server.sh /usr/src/app/
COPY requirements.txt /usr/src/app/
COPY kadcarsnft_api /usr/src/app/
#COPY .pip_cache /usr/src/app/pip_cache/

WORKDIR /usr/src/app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --cache-dir /usr/src/app/pip_cache
RUN chown -R www-data:www-data /usr/src/app
ADD requirements.txt /usr/src/app/

# 2. blender setup
# RUN apt update
# RUN apt install build-essential git subversion -y cmake libx11-dev libxxf86vm-dev libxcursor-dev libxi-dev libxrandr-dev libxinerama-dev libglew-dev

# RUN mkdir -p ~/blender-git/
# WORKDIR /~/blender-git/
# RUN git clone https://git.blender.org/blender.git

# RUN mkdir /~/blender-git/lib/
# WORKDIR /~/blender-git/lib/
# RUN svn checkout https://svn.blender.org/svnroot/bf-blender/trunk/lib/linux_centos7_x86_64

# WORKDIR /~/blender-git/blender/
# RUN make update
# RUN make

# 4. network setup
EXPOSE 8020
STOPSIGNAL SIGTERM

WORKDIR /usr/src/app/kadcarsnft_api/

# 5. start app
# CMD ["/usr/src/app/start-server.sh"]
# CMD python manage.py runserver 8020