# frp-openwrt

OpenWrt packages for [frp](https://github.com/fatedier/frp).

This repository follows the same feed-style layout used by `nps-openwrt`:

- `frpc/` and `frps/` provide prebuilt daemon packages.
- `luci-app-frpc/` and `luci-app-frps/` provide LuCI configuration pages.
- `frp.ver` stores the current upstream release version.

## Packages

- `frpc`
- `frps`
- `luci-app-frpc`
- `luci-app-frps`

## Build

Add this repository as an OpenWrt feed:

```bash
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
make package/luci-i18n-frpc-zh-cn/{clean,compile} V=s
make package/luci-i18n-frps-zh-cn/{clean,compile} V=s
```

The generated packages are written under `bin/packages/*/frp/`.
