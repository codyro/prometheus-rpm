#!/bin/sh

set -eu

echo "Checking matrix-alertmanager-receiver"

PKG="$(:;
	grep Version: matrix-alertmanager-receiver.spec \
		| awk '{print $2}'
	)"
RELEASE="$(sed -n 's/^Release: *\([0-9]*\).*$/\1/p' matrix-alertmanager-receiver.spec)"

echo "Package version: $PKG"

LATEST="$(:;
	curl -s 'https://github.com/metio/matrix-alertmanager-receiver/releases' \
		| sed -n 's#^.*href="/metio/matrix-alertmanager-receiver/tree/\([^"-]*\)".*$#\1#p' \
		| head -n1
	)"

echo "Latest version:  $LATEST"

if [ "$LATEST" != "$PKG" ]; then
	printf '%-32s %s -> %s\n' 'matrix-alertmanager-receiver' "$PKG" "$LATEST"
fi

if [ "$LATEST" != "$PKG" ]; then
	DATE="$(date "+%a %b %d %Y")"
	USER="Lars Kiesow <lkiesow@uos.de>"
	sed -i "s/^Version: .*/Version:       ${LATEST}/" matrix-alertmanager-receiver.spec
	sed -i "s/^%changelog/%changelog\n\* ${DATE} ${USER} - ${LATEST}-${RELEASE}\n- Update to ${LATEST}\n/" matrix-alertmanager-receiver.spec

	git commit matrix-alertmanager-receiver.spec -m "Update matrix-alertmanager-receiver to ${LATEST}"
fi
