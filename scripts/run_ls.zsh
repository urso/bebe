#!/usr/bin/env zsh

DURATION=90
version=$1
binary=$2
shift 2

export TIMEFMT="CPU=%P User=%U Sys=%S Total=%E MaxRSS=%M InOps=%I OutOps=%O"
rm -Rf data/*;
{sleep $DURATION; killall $binary}&
{ time ./bin/$version/$binary -httpprof localhost:6060 -c output/logstash.yml $@ }
