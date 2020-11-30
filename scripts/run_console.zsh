#!/usr/bin/env zsh

DURATION=20

version=$1
binary=$2
shift 2

export TIMEFMT="CPU=%P User=%U Sys=%S Total=%E MaxRSS=%M InOps=%I OutOps=%O"
rm -Rf data/*;
rm -Rf ./bin/$version/data/*;
{sleep $DURATION; killall $binary}&
{ time ./bin/$version/$binary -c output/console.yml $@ } | pv -Warl >/dev/null
