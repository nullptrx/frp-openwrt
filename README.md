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

## GitHub Pages feed

The `Build OpenWrt` workflow also publishes `ipk` feeds to GitHub Pages with
this layout:

```text
https://frpfrp.pages.dev/openwrt-24.10/<target>/frp
```

Example:

```bash
echo 'src/gz frp https://frpfrp.pages.dev/openwrt-24.10/aarch64_cortex-a53/frp' >> /etc/opkg/customfeeds.conf
opkg update
opkg install frpc luci-app-frpc
```

Each feed directory contains the package files together with `Packages`,
`Packages.gz`, and `Packages.manifest`.
