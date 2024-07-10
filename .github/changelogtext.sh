#!/usr/bin/env bash
set -e

PACKAGE_VERSION=${1:-$(sed -r 's/__version__ = "(.*)"/\1/' ravenpackapi/version.py)}

# Make sure the version is in the changelog
grep -n "^## \[v$PACKAGE_VERSION] \(.*\)" CHANGELOG.md >/dev/null \
    || (echo "Error. Version $PACKAGE_VERSION not in changelog" \
    && exit 1)
LINE_BEFORE=$( \
    grep -n "^## \[v$PACKAGE_VERSION] \(.*\)" CHANGELOG.md \
    | cut -d: -f1 \
    | head -n 1 \
)

# * cut from after the header of the current package version
# * select all the other headers, showing the linue numbers
# * get the line number of the first header
LINE_AFTER=$( \
    tail -n +$LINE_BEFORE CHANGELOG.md \
    | tail -n +2 \
    | grep -n "^## \[v.*\] \(.*\)" \
    | sed -r 's/(.*):## \[v(.*)\] \(.*\)/\1:\2/' \
    | cut -d: -f1 \
    | head -1
)

LINE_BEFORE=$((LINE_BEFORE + 1))
LINE_AFTER=$((LINE_AFTER + LINE_BEFORE))
LINE_AFTER=$((LINE_AFTER - 2))
# Extract range and remove empty lines from the beginning and end of the file
sed -n "$LINE_BEFORE,$LINE_AFTER p" CHANGELOG.md \
    | awk 'NF {p=1} p' | tac | awk 'NF {p=1} p' | tac
