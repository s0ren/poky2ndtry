#!/bin/bash

# kør dette script UDEN sudo



mkdir poky

# https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html
sudo apt-get install -y gawk wget git diffstat unzip texinfo gcc build-essential chrpath socat cpio python3 python3-pip python3-pexpect xz-utils debianutils iputils-ping python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev pylint3 xterm python3-subunit mesa-common-dev zstd liblz4-tool

git init

git add .
git commit . -m "første commit"

git checkout -b subtrees

git subtree add -P poky --squash git://git.yoctoproject.org/poky kirkstone -m "poky kirkstone hentet"
git commit . "poky subtree"
git checkout -b metaraspisubtree
git subtree add -P poky/meta-raspberrypi --squash git://git.yoctoproject.org/meta-raspberrypi kirkstone -m "meta-raspberrypi kirkstone hentet"
git commit . "meta-raspberrypi subtree"

git checkout -b first_raspi