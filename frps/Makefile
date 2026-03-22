# Copyright (C) 2008-2014 The LuCI Team <luci@lists.subsignal.org>
# Copyright (C) 2024-2026 frp-openwrt contributors

include $(TOPDIR)/rules.mk

PKG_NAME:=frps
PKG_VERSION:=0.68.0
PKG_RELEASE:=1
PKG_LICENSE:=Apache-2.0
PKG_MAINTAINER:=frp-openwrt contributors
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

FRP_URL:=https://github.com/fatedier/frp

FRP_ARCH:=
ifeq ($(ARCH),x86_64)
	FRP_ARCH:=amd64
endif
ifeq ($(ARCH),aarch64)
	FRP_ARCH:=arm64
endif
ifeq ($(findstring armv8,$(BOARD)),armv8)
	FRP_ARCH:=arm64
endif
ifeq ($(ARCH),arm)
	ifeq ($(BOARD),kirkwood)
		FRP_ARCH:=arm
	else
		FRP_ARCH:=arm_hf
	endif
endif
ifeq ($(filter mipsel,$(ARCH)),mipsel)
	FRP_ARCH:=mipsle
endif
ifeq ($(filter mips64el,$(ARCH)),mips64el)
	FRP_ARCH:=mips64le
endif
ifeq ($(filter mips64,$(ARCH)),mips64)
	FRP_ARCH:=mips64
endif
ifeq ($(filter mips,$(ARCH)),mips)
	FRP_ARCH:=mips
endif
ifeq ($(filter loongarch64,$(ARCH)),loongarch64)
	FRP_ARCH:=loong64
endif
ifeq ($(filter riscv64,$(ARCH)),riscv64)
	FRP_ARCH:=riscv64
endif

ifeq ($(strip $(FRP_ARCH)),)
$(error Unsupported architecture for frp prebuilt package)
endif

PKG_SOURCE:=frp_$(PKG_VERSION)_linux_$(FRP_ARCH).tar.gz
PKG_SOURCE_URL:=$(FRP_URL)/releases/download/v$(PKG_VERSION)/

# === FRPS_HASH_TABLE_START ===
FRPS_HASHES:= \
  amd64=3cf934477f4fb1ee9e19e49c31fb33f5ffe3283300076f59afad8b8ccf1e1621 \
  arm64=8855bd3537adf6f456b4073a1fb6f119885060f3c8b714fd56a842db42b4c097 \
  arm_hf=0a103ea2f2492441a8c2b951dcbd59f812391ab9915eacdb3be4016f67ecfa1e \
  arm=3944595c77cc8242a9d94a840b59966f018ddaeb3e93e4301d803e7c7ed31b8e \
  loong64=457d0b31f1f6516b18d2139310e87dd1d58c75621aeefdbfd01d96e7de415227 \
  mips=00dcb661d9e438f491eff1827173f7296355555245ec36d62298e1ba39c9566d \
  mips64=564e39a2b6663c1752dd44c11a0603b8e260fab7bda42191a0f74cae751359e3 \
  mips64le=33a6c0d4dc5cc2e17f22141d8f438ff0683abaa3d91f2beb5e7bfce052026d19 \
  mipsle=efa2ecc1144b413e85f3e00e7b7ac382d0e2d752455d609072cc2b7969e44356 \
  riscv64=18b468db9e2a597927b4033e151a7130598ee217da1fd27b8d7274d9d678e45d
# === FRPS_HASH_TABLE_END ===

PKG_HASH:=$(strip $(foreach pair,$(FRPS_HASHES), $(if $(filter $(FRP_ARCH)=%,$(pair)),$(word 2, $(subst =, ,$(pair))))))

include $(INCLUDE_DIR)/package.mk

define Package/$(PKG_NAME)
	SECTION:=net
	CATEGORY:=Network
	TITLE:=frp server (precompiled for $(FRP_ARCH))
	URL:=$(FRP_URL)
endef

define Package/$(PKG_NAME)/conffiles
/etc/config/frps
endef

define Package/$(PKG_NAME)/description
frps is the frp server used to expose services to the internet.
This package installs the precompiled frps binary for the $(FRP_ARCH) architecture.
endef

define Build/Compile
	mkdir -p $(PKG_BUILD_DIR)
	tar -xzf $(DL_DIR)/$(PKG_SOURCE) -C $(PKG_BUILD_DIR)
endef

define Package/$(PKG_NAME)/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/frp_$(PKG_VERSION)_linux_$(FRP_ARCH)/frps $(1)/usr/bin/frps

	$(INSTALL_DIR) $(1)/etc/config
	$(INSTALL_CONF) ./root/etc/config/frps $(1)/etc/config/frps

	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./root/etc/init.d/frps $(1)/etc/init.d/frps

	$(INSTALL_DIR) $(1)/etc/uci-defaults
	$(INSTALL_BIN) ./root/etc/uci-defaults/40_luci-frps $(1)/etc/uci-defaults/40_luci-frps
endef

$(eval $(call BuildPackage,$(PKG_NAME)))
