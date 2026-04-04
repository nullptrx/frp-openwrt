# frp-openwrt

OpenWrt packages for [frp](https://github.com/fatedier/frp).

This repository follows the same feed-style layout used by `nps-openwrt`:

- `frpc/` and `frps/` provide prebuilt daemon packages.
- `luci-app-frpc/` and `luci-app-frps/` provide LuCI configuration pages.
- `frp.ver` stores the current upstream release version.

Runtime configuration is generated as TOML:

- `frpc` writes `/var/etc/frpc/frpc.toml`
- `frps` writes `/var/etc/frps/frps.toml`
- `frpc` proxies are emitted as `[[proxies]]` entries
- LuCI syncs common settings and proxies by TOML field name

## Packages

- `frpc`
- `frps`
- `luci-app-frpc`
- `luci-app-frps`

## Build

Add this repository as an OpenWrt feed:

```bash
# Local checkout
echo "src-link frp /path/to/frp-openwrt" >> feeds.conf

# Remote repository
echo "src-git frp https://github.com/<your-org>/frp-openwrt.git" >> feeds.conf

./scripts/feeds update -a
./scripts/feeds install -d n luci-app-frpc
./scripts/feeds install -d n luci-app-frps
./scripts/feeds install -d n luci-i18n-frpc-zh-cn
./scripts/feeds install -d n luci-i18n-frps-zh-cn
```

Then select the packages in `make menuconfig`, and build them with:

```bash
make package/luci-app-frpc/{clean,compile} V=s
make package/luci-app-frps/{clean,compile} V=s
```

The generated packages are written under `bin/packages/*/frp/`.

## Install & Update

### A. Install From Feed (Recommended)

#### 1. Add Feed

```bash
# only needs to be run once
wget -O - https://cdn.jsdelivr.net/gh/nullptrx/frp-openwrt@main/feed.sh | ash
```

#### 2. Install

```bash
# you can install from shell or `Software` menu in LuCI
# for opkg
opkg install frpc
opkg install frps
opkg install luci-app-frpc
opkg install luci-app-frps
opkg install luci-i18n-frpc-zh-cn
opkg install luci-i18n-frps-zh-cn

# for apk
apk add frpc
apk add frps
apk add luci-app-frpc
apk add luci-app-frps
apk add luci-i18n-frpc-zh-cn
apk add luci-i18n-frps-zh-cn
```

## GitHub Pages feed

- `ipk`: `https://nullptrx.github.io/frp-openwrt/openwrt-24.10/<target>/frp`
- `apk`: `https://nullptrx.github.io/frp-openwrt/SNAPSHOT/<target>/frp`

Published helper files:

- `https://nullptrx.github.io/frp-openwrt/feed.sh`
- `https://nullptrx.github.io/frp-openwrt/frp.pub`

For Pages publishing, configure these repository secrets:

- `USIGN_PUBLIC_KEY`
- `USIGN_PRIVATE_KEY` (optional, only required for `Packages.sig`)
