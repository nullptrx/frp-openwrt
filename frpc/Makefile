# Copyright (C) 2008-2014 The LuCI Team <luci@lists.subsignal.org>
# Copyright (C) 2024-2026 frp-openwrt contributors

include $(TOPDIR)/rules.mk

PKG_NAME:=frpc
PKG_VERSION:=0.68.1
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
  amd64=4a4e88987d39561e1b3b3b23d0ede48a457eebf76a87231999957e870f5f02b6 \
  arm64=e7ad15b0cfe4cf0125df4217778b66cb4426179270967b59900ecb2362d8cd01 \
  arm_hf=63954351f92337fedd26c966d1085480cba26cbb87976e545f8515fd350cb5f3 \
  arm=50b187e66c1b9366532bda25326ca75e2f0dffbb474431310321a705cea9810f \
  loong64=8f69cd6707b9c90b8e291879b1bfe2465056464ef770c4f95a2b3ee6a9489dd5 \
  mips=3393effe2937b9d92e9b2489fa8c64e860ffd028e119017f72bc1f538c0773f9 \
  mips64=be64ee6f168ec038064a4a2c96aa3b5fbba96463668095bcb0491280314a4e84 \
  mips64le=928f57c0f29c3fdede305144f62e5eb557fe10120775ed43c204c4fa9cfd220b \
  mipsle=097ad98dd165c028577064e9b7277de652c2649efaf8f6e835ab4510bce93ddf \
  riscv64=95e0924b54e90d607ef4b70b6ce27b26c73de2f4fbebeab2c97a849863918a52
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
