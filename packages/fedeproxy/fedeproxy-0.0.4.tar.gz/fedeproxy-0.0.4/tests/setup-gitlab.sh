#!/bin/bash

set -ex

function prepare_environment() {
    : ${MY_IP:=0.0.0.0}
}

function cleanup() {
    local serial=$1
    
    docker stop test-gitlab$serial || true
    docker rm test-gitlab$serial || true
}

function run_gitlab() {
    local serial=$1
    local GITLAB_OMNIBUS_CONFIG="external_url 'http://${MY_IP}:818${serial}'; gitlab_rails['gitlab_shell_ssh_port'] = 222${serial};"
    docker run --name="test-gitlab$serial" -d \
	   -e GITLAB_OMNIBUS_CONFIG="$GITLAB_OMNIBUS_CONFIG" \
	   -p 222$serial:22 -p 818$serial:818$serial \
	   octobus/heptapod:0.24.0
}

function setup_gitlab() {
    local serial=$1
    run_gitlab $serial
    while true ; do
	if test $(curl --silent http://${MY_IP}:818$serial -o /dev/null -w "%{http_code}") = 302 ; then
	    docker exec test-gitlab$serial gitlab-rails runner "user = User.find_by_username 'root'; user.password = 'Wrobyak4'; user.password_confirmation = 'Wrobyak4'; user.password_automatically_set = false ; user.save!"
	    docker exec test-gitlab$serial gitlab-rails runner "Gitlab::CurrentSettings.current_application_settings.update(default_vcs_type: 'git')"
	    return
	fi
	sleep 5
    done
    false
}

function setup() {
    local serial
    for serial in $serials ; do
	setup_gitlab $serial
    done
}

function teardown() {
    local serial
    for serial in $serials ; do
	cleanup $serial
    done
}

: ${serials:=1 2}

for f in prepare_environment ${@:-teardown setup} ; do
    $f
done
