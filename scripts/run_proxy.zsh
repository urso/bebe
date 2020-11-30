#!/usr/bin/env zsh

DURATION=20
version=$1
binary=$2
shift 2

rm -Rf tmp
mkdir -p tmp/proxy
mkdir -p tmp/acquire

{sleep $DURATION; killall $binary; killall filebeat}&

export TIMEFMT="CPU=%P User=%U Sys=%S Total=%E MaxRSS=%M InOps=%I OutOps=%O Job=%J"
#{ time ./bin/$version/$binary -httpprof localhost:6060 -path.data tmp/acquire -path.logs tmp/acquire --cpuprofile tmp/acquire/cpu.prof $@ >/dev/null 2>&1 }&
{ time ./bin/$version/$binary -httpprof localhost:6060 -path.data tmp/acquire -path.logs tmp/acquire $@ >/dev/null 2>&1 }&

{ time ./bin/$version/filebeat -httpprof localhost:6161 -path.data tmp/proxy -path.logs tmp/proxy -c input/proxy.yml -c output/console.yml } | pv -Warl >/dev/null
