#
# Container with just the core AtomSpace framework installed.
# This includes the cogserver, atomspce-rocks and atomspace-cog.
# It does NOT include nlp, unify, ure, pln or opencog.
#
# Steps:
# 1. docker build --no-cache -t opencog/atomspace .
# 2. docker create --name atomspace -p 17001:17001
#       -v /ABSOLUTE/PATH/TO/YOUR/WORKING/DIRECTORY/On/Your/PC/:/opencog
#       -w /opencog
#       -it opencog/atomspace
# 3. docker start -i atomspace
#

FROM opencog/opencog-deps:latest

# The apt installs below will fail, unless we are at the latest.
RUN apt-get -y update; apt-get -y upgrade

# Basic tools that allow this image to be minimally usable.
#  * Networking tools (ping, ifconfig, telnet, netcat)
#  * Terminal sharing tools (tmux, byobu)
#  * Debug tools (gdb)
#  * Webserver (apache2, php)
RUN apt-get -y install \
	net-tools iputils-ping telnet netcat-openbsd traceroute iptraf \
	tmux byobu \
	gdb time \
	apache2 php

# Install cogutil
ENV LAST_COGUTIL_UPDATE 2025-05-29
RUN  /tmp/octool -c && ccache -C

# Update Link Grammar. This avoids having to rebuild the opencog/deps
# This installs the latest release tarball, and NOT github master.
ENV LAST_LINK_GRAMMAR_UPDATE 2024-05-02
RUN  /tmp/octool -l default && ccache -C

# Install core AtomSpace.
ENV LAST_ATOMSPACE_UPDATE 2025-04-02
RUN  /tmp/octool -a && ccache -C

USER opencog
WORKDIR /home/opencog

# Setup the workspace for developers
COPY /scripts/ /home/opencog
RUN sudo chown -R opencog:opencog .
RUN sudo chown -R opencog:opencog .[a-z]*

# XXX FIXME - despite efforts, the timestamp on
#    /usr/local/lib/guile/3.0/site-ccache/opencog.go
# is older than that on
#    /usr/local/share/guile/site/3.0/opencog.scm
# So hack around this by forcing a compile.
RUN guile -c "(use-modules (opencog) (opencog exec) (opencog cogserver) (opencog persist) (opencog persist-cog) (opencog persist-rocks))"

# RUN guile -c "(use-modules (opencog persist-pgres))"

CMD /bin/bash

ONBUILD USER root
