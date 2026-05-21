# Copyright (C) 2008-2014 The LuCI Team <luci@lists.subsignal.org>
# Copyright (C) 2024-2026 frp-openwrt contributors

include $(TOPDIR)/rules.mk

PKG_NAME:=frpc
PKG_VERSION:=0.69.0
PKG_RELEASE:=1
PKG_LICENSE:=Apache-2.0
PKG_MAINTAINER:=frp-openwrt contributors
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

FRP_URL:=https://github.com/fatedier/frp

FRP_ARCH:=
ifneq (,$(findstring x86_64,$(ARCH)))
	FRP_ARCH:=amd64
endif
ifneq (,$(findstring aarch64,$(ARCH)))
	FRP_ARCH:=arm64
endif
ifneq (,$(findstring armv8,$(ARCH)$(BOARD)$(TARGET)))
	FRP_ARCH:=arm64
endif
ifneq (,$(findstring cortexa53,$(ARCH)$(BOARD)$(TARGET)))
	FRP_ARCH:=arm64
endif
ifneq (,$(findstring cortexa72,$(ARCH)$(BOARD)$(TARGET)))
	FRP_ARCH:=arm64
endif
ifneq (,$(findstring arm,$(ARCH)))
	ifeq ($(BOARD),kirkwood)
		FRP_ARCH:=arm
	else
		FRP_ARCH:=arm_hf
	endif
endif
ifneq (,$(findstring mipsel,$(ARCH)))
	FRP_ARCH:=mipsle
endif
ifneq (,$(findstring mips64el,$(ARCH)))
	FRP_ARCH:=mips64le
endif
ifneq (,$(findstring mips64,$(ARCH)))
	FRP_ARCH:=mips64
endif
ifneq (,$(findstring mips,$(ARCH)))
	FRP_ARCH:=mips
endif
ifneq (,$(findstring loongarch64,$(ARCH)))
	FRP_ARCH:=loong64
endif
ifneq (,$(findstring riscv64,$(ARCH)))
	FRP_ARCH:=riscv64
endif

ifneq ($(strip $(ARCH)$(BOARD)$(TARGET)),)
ifeq ($(strip $(FRP_ARCH)),)
$(error Unsupported architecture for frp prebuilt package: ARCH=$(ARCH) BOARD=$(BOARD) TARGET=$(TARGET))
endif
endif

PKG_SOURCE:=frp_$(PKG_VERSION)_linux_$(FRP_ARCH).tar.gz
PKG_SOURCE_URL:=$(FRP_URL)/releases/download/v$(PKG_VERSION)/

# === FRPC_HASH_TABLE_START ===
FRPC_HASHES:= \
  amd64=6b90d1cd28fc661f170c0de90dde03d2c63e4fd7ce0ae2da2ca1c28014b8146e \
  arm64=24a4fc82b4c041835103419685ea124c4d6a7dbf83d0425481c5831b4ce4b3a4 \
  arm_hf=a42b004d1d56255e1c63b74223449165ac93fdca8bafdb60e5317282c05e71c6 \
  arm=8ee99ad9b09eafe5f77fea7cbd9db15deb056dc2857955477972ccb31a74e708 \
  loong64=c136cd4170b44e905ba2c88e0a5900be9fe5baf64f55befb516b18bce02b63a6 \
  mips=0dfe614709f6d12e9262a18d1ab68f8311b00430a2e822934b2ddb8d14f412bb \
  mips64=12167b501632f715dc7f18db3e6f44b61fd4ea5b09c99c155e44937a60fabf24 \
  mips64le=f0a34fab813228412f71360e2fd9816d91d88781b9fd68c88e05c79f5e9d8f89 \
  mipsle=baed218d2a44e796da2f6d943c627e6e5cb53fd4cd54b6f2818ad6d93842a9cd \
  riscv64=27e7b0eea947c2c1b17b2eb62b093e8f4d96185edf245da4699655c047d4a6d0
# === FRPC_HASH_TABLE_END ===

PKG_HASH:=$(strip $(foreach pair,$(FRPC_HASHES), $(if $(filter $(FRP_ARCH)=%,$(pair)),$(word 2, $(subst =, ,$(pair))))))

include $(INCLUDE_DIR)/package.mk

define Package/$(PKG_NAME)
	SECTION:=net
	CATEGORY:=Network
	TITLE:=frp client (precompiled for $(FRP_ARCH))
	URL:=$(FRP_URL)
endef

define Package/$(PKG_NAME)/conffiles
/etc/config/frpc
endef

define Package/$(PKG_NAME)/description
frpc is the frp client used to expose local services through NAT/firewall.
This package installs the precompiled frpc binary for the $(FRP_ARCH) architecture.
endef

define Build/Compile
	mkdir -p $(PKG_BUILD_DIR)
	tar -xzf $(DL_DIR)/$(PKG_SOURCE) -C $(PKG_BUILD_DIR)
endef

define Package/$(PKG_NAME)/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/frp_$(PKG_VERSION)_linux_$(FRP_ARCH)/frpc $(1)/usr/bin/frpc

	$(INSTALL_DIR) $(1)/etc/config
	$(INSTALL_CONF) ./root/etc/config/frpc $(1)/etc/config/frpc

	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./root/etc/init.d/frpc $(1)/etc/init.d/frpc

	$(INSTALL_DIR) $(1)/etc/uci-defaults
	$(INSTALL_BIN) ./root/etc/uci-defaults/40_luci-frpc $(1)/etc/uci-defaults/40_luci-frpc
endef

$(eval $(call BuildPackage,$(PKG_NAME)))
