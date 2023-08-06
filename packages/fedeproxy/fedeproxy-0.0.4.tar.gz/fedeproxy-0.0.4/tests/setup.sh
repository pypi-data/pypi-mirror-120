#!/bin/bash

set -e

if test $(id -u) != 0 ; then
    SUDO=sudo
fi

if ! which hg >/dev/null || ! which git >/dev/null ; then
    $SUDO apt-get install -qq -y mercurial git
fi

tests/setup-gitlab.sh "$@"
tests/setup-gitea.sh "$@"
