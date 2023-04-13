#!/bin/sh
PYTHONPATH=
for addon in /storage/.kodi/addons/*/lib /storage/.kodi/addons/*/libs /usr/lib/kodi/addons/*/lib; do
  [ -d "${addon}" ] && PYTHONPATH="${PYTHONPATH:+${PYTHONPATH}:}${addon}"
done
export PYTHONPATH
echo "PYTHONPATH=${PYTHONPATH}"
exec /usr/bin/python "$@"