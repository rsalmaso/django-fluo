#!/bin/bash

if [ "$1" == "" ]; then
  path="$PWD"
else
  path="$1"
fi

if [ ! -d "${path}" ]; then
  echo "Not a directory: ${path}"
  exit -1
fi
pidfile="${path}/uwsgi.pid"
logfile="${path}/uwsgi.log"
media="${path}/media"
static="${path}/static"
wsgi="wsgi"
wsgipath="${path}"
wsgifile="${wsgipath}/${wsgi}.py"

echo "Launching uWSGI"
uwsgi --no-orphans --harakiri 60 --harakiri-verbose --idle 30 --http 0.0.0.0:8000 --static-map="/media=${media}" --static-map="/static=${static}" --chdir="${wsgipath}" -w "${wsgi}" --touch-reload "${wsgifile}" --pidfile="${pidfile}" &

echo "listening for changes"
while read line; do
  filename="$(basename $line)"
  dirname="$(dirname $line)"
  if [ "${filename##*.}" == "py" ]; then
    touch "${path}"/wsgi.py
  fi;
  if [ "${filename##*.}" == "less" ]; then
    #css="${dirname}/$(basename ${line} .less).css"
    #lessc -x "${line}" "${css}"
    lessc -x "${static}/css/all.less" "${static}/css/all.css"
    lessc -x "${static}/css/ie.less" "${static}/css/ie.css"
  fi;
done < <(inotifywait -r -q -m -e MODIFY --format '%w%f' "${path}");

echo "Killing uWSGI"
killall inotifywait
killall uwsgi

