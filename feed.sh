#!/bin/sh
set -eu

REPOSITORY_URL="https://nullptrx.github.io/frp-openwrt"
PUBKEY_URL="$REPOSITORY_URL/frp.pub"

detect_arch() {
	if [ -f /etc/openwrt_release ]; then
		# shellcheck disable=SC1091
		. /etc/openwrt_release
		if [ -n "${DISTRIB_ARCH:-}" ]; then
			printf '%s\n' "$DISTRIB_ARCH"
			return 0
		fi
	fi

	if command -v apk >/dev/null 2>&1; then
		apk --print-arch
		return 0
	fi

	echo "Unable to determine OpenWrt architecture" >&2
	exit 1
}

install_opkg_feed() {
	arch="$(detect_arch)"
	feed_url="$REPOSITORY_URL/openwrt-24.10/$arch/frp"
	tmp_key="/tmp/frp.pub"

	wget -O "$tmp_key" "$PUBKEY_URL"
	opkg-key add "$tmp_key"
	rm -f "$tmp_key"

	[ -f /etc/opkg/customfeeds.conf ] || touch /etc/opkg/customfeeds.conf
	sed -i '\|^src/gz frp |d' /etc/opkg/customfeeds.conf
	echo "src/gz frp $feed_url" >> /etc/opkg/customfeeds.conf

	opkg update
}

install_apk_feed() {
	arch="$(detect_arch)"
	repo_url="$REPOSITORY_URL/SNAPSHOT/$arch/frp"
	keys_dir="/etc/apk/keys"
	key_path="$keys_dir/frp.pub"

	mkdir -p "$keys_dir"
	wget -O "$key_path" "$PUBKEY_URL"
	chmod 644 "$key_path"

	repositories_file="/etc/apk/repositories.d/frp.list"
	mkdir -p "$(dirname "$repositories_file")"
	printf '%s\n' "$repo_url" > "$repositories_file"

	apk update
}

if command -v opkg >/dev/null 2>&1; then
	install_opkg_feed
elif command -v apk >/dev/null 2>&1; then
	install_apk_feed
else
	echo "Neither opkg nor apk was found on this system." >&2
	exit 1
fi
