﻿#
# This is free software, lisence use MIT.
# 
# Copyright (C) 2019 P3TERX <https://p3terx.com>
# Copyright (C) 2019 KFERMercer <KFER.Mercer@gmail.com>
# 
# <https://github.com/KFERMercer/OpenWrt-CI>
# 

name: AIXAN自用编译内容

on:
  schedule:
    - cron: 0 20 * * *
  push:
    branches: 
      - master

jobs:

  build_openwrt:

    name: 开始构建Openwrt
    runs-on: ubuntu-18.04

    steps:
      - name: Checkout
        uses: actions/checkout@v2
        with:
          ref: master

      - name: 初始化环境
        env:
          DEBIAN_FRONTEND: noninteractive
        run: |
          docker rmi `docker images -q`
          sudo rm -rf /usr/share/dotnet /etc/mysql /etc/php /etc/apt/sources.list.d
          sudo -E apt-get -y purge azure-cli ghc* zulu* hhvm llvm* firefox google* dotnet* powershell openjdk* mysql* php*
          sudo -E apt-get update
          sudo -E apt-get -y install build-essential asciidoc binutils bzip2 gawk gettext git libncurses5-dev libz-dev patch python3 unzip zlib1g-dev lib32gcc1 libc6-dev-i386 subversion flex uglifyjs gcc-multilib g++-multilib p7zip p7zip-full msmtp libssl-dev texinfo libglib2.0-dev xmlto qemu-utils upx libelf-dev autoconf automake libtool autopoint device-tree-compiler antlr3 gperf
          sudo -E apt-get -y autoremove --purge
          sudo -E apt-get clean
          df -h
      - name: 更新 feeds
        run: |
          ./scripts/feeds update -a
          ./scripts/feeds install -a
      - name: 生成配置文件
        run: |
          rm -rf ./.config*
          touch ./config
          #
          # ========================固件定制部分========================
          #
          #
          # 如果不对本区块做出任何编辑, 则生成默认配置固件.
          #
          # 以下为定制化固件选项和说明:
          #
          #
          # 有些插件/选项是默认开启的, 如果想要关闭, 请参照以下示例进行编写:
          #
          #          =========================================
          #         |  # 取消编译VMware镜像:                   |
          #         |  cat >> .config <<EOF                   |
          #         |  # CONFIG_VMDK_IMAGES is not set        |
          #         |  EOF                                    |
          #          =========================================
          #
          #
          # 以下是一些提前准备好的一些插件选项.
          # 直接取消注释相应代码块即可应用. 不要取消注释代码块上的汉字说明.
          # 如果不需要代码块里的某一项配置, 只需要删除相应行.
          #
          # 如果需要其他插件, 请按照示例自行添加.
          # 注意, 只需添加依赖链顶端的包. 如果你需要插件 A, 同时 A 依赖 B, 即只需要添加 A.
          #
          # 无论你想要对固件进行怎样的定制, 都需要且只需要修改 EOF 回环内的内容.
          #
          # 编译x64固件:
          cat >> .config <<EOF
          CONFIG_TARGET_x86=y
          CONFIG_TARGET_x86_64=y
          CONFIG_TARGET_x86_64_Generic=y
          EOF
          # 固件压缩:
          cat >> .config <<EOF
          CONFIG_TARGET_ROOTFS_EXT4FS=y
          CONFIG_TARGET_EXT4_RESERVED_PCT=0
          CONFIG_TARGET_EXT4_BLOCKSIZE_4K=y
          # CONFIG_TARGET_EXT4_BLOCKSIZE_2K is not set
          # CONFIG_TARGET_EXT4_BLOCKSIZE_1K is not set
          CONFIG_TARGET_EXT4_BLOCKSIZE=4096
          # CONFIG_TARGET_ROOTFS_SQUASHFS is not set
          CONFIG_TARGET_IMAGES_GZIP=y
          CONFIG_TARGET_KERNEL_PARTSIZE=30
          CONFIG_TARGET_ROOTFS_PARTSIZE=1024
          EOF
          # 编译UEFI固件:
          # cat >> .config <<EOF
          # CONFIG_EFI_IMAGES=y
          # EOF
          # IPv6支持:
          cat >> .config <<EOF
          CONFIG_PACKAGE_dnsmasq_full_dhcpv6=y
          CONFIG_PACKAGE_ipv6helper=y
          EOF
          # 多文件系统支持:
          cat >> .config <<EOF
          CONFIG_PACKAGE_kmod-fs-ext4=y
          CONFIG_PACKAGE_kmod-fs-nfs=y
          CONFIG_PACKAGE_kmod-fs-nfs-common=y
          CONFIG_PACKAGE_kmod-fs-nfs-v3=y
          CONFIG_PACKAGE_kmod-fs-nfs-v4=y
          CONFIG_PACKAGE_kmod-fs-ntfs=y
          EOF
          # USB3.0支持:
          cat >> .config <<EOF
          CONFIG_PACKAGE_kmod-usb-ohci=y
          CONFIG_PACKAGE_kmod-usb-ohci-pci=y
          CONFIG_PACKAGE_kmod-usb2=y
          CONFIG_PACKAGE_kmod-usb2-pci=y
          CONFIG_PACKAGE_kmod-usb3=y
          EOF
          # 常用LuCI插件选择:
          cat >> .config <<EOF
          CONFIG_PACKAGE_luci-app-diskman=y
          CONFIG_PACKAGE_luci-app-adbyby-plus=y
          CONFIG_PACKAGE_luci-app-aria2=y
          CONFIG_PACKAGE_luci-app-baidupcs-web=y
          CONFIG_PACKAGE_luci-app-frpc=y
          CONFIG_PACKAGE_luci-app-hd-idle=y
          CONFIG_PACKAGE_luci-app-kodexplorer=y
          CONFIG_PACKAGE_luci-app-minidlna=y
          CONFIG_PACKAGE_luci-app-qbittorrent=y
          CONFIG_PACKAGE_luci-app-wol=y
          CONFIG_PACKAGE_luci-app-ssr-plus=y
          CONFIG_PACKAGE_luci-app-ssr-plus_INCLUDE_V2ray_plugin=y
          CONFIG_PACKAGE_luci-app-ssr-plus_INCLUDE_Kcptun=y
          CONFIG_PACKAGE_luci-app-ssr-plus_INCLUDE_Shadowsocks=y
          CONFIG_PACKAGE_luci-app-ssr-plus_INCLUDE_ShadowsocksR_Socks=y
          CONFIG_PACKAGE_luci-app-ssr-plus_INCLUDE_V2ray=y
          CONFIG_PACKAGE_luci-app-ssr-plus_INCLUDE_Trojan=y
          CONFIG_PACKAGE_luci-app-ssr-plus_INCLUDE_Redsocks2=y
          CONFIG_PACKAGE_luci-app-ssr-plus_INCLUDE_ShadowsocksR_Server=y
          CONFIG_PACKAGE_luci-app-ttyd=y
          CONFIG_PACKAGE_luci-app-verysync=y
          CONFIG_PACKAGE_luci-app-webadmin=y
          CONFIG_PACKAGE_luci-app-wireguard=y
          CONFIG_PACKAGE_luci-app-wrtbwmon=y
          # CONFIG_PACKAGE_luci-app-openvpn is not set
          # CONFIG_PACKAGE_luci-app-openvpn-server is not set
          # CONFIG_PACKAGE_luci-app-vlmcsd is not set
          # CONFIG_PACKAGE_luci-app-zerotier is not set
          # CONFIG_DEFAULT_luci-app-ipsec-vpnd is not set
          # CONFIG_PACKAGE_luci-app-kodexplorer is not set
          EOF
          # LuCI主题:
          cat >> .config <<EOF
          CONFIG_PACKAGE_luci-theme-material=y
          EOF
          # 常用软件包:
          cat >> .config <<EOF
          CONFIG_PACKAGE_curl=y
          CONFIG_PACKAGE_htop=y
          CONFIG_PACKAGE_nano=y
          CONFIG_PACKAGE_screen=y
          CONFIG_PACKAGE_tree=y
          CONFIG_PACKAGE_vim-fuller=y
          CONFIG_PACKAGE_wget=y
          EOF
          # OpenSSH
          cat >> .config <<EOF
          CONFIG_PACKAGE_bash=y
          CONFIG_PACKAGE_openssh-client=y
          CONFIG_PACKAGE_openssh-client-utils=y
          CONFIG_PACKAGE_openssh-keygen=y
          CONFIG_PACKAGE_openssh-server=y
          CONFIG_PACKAGE_openssh-sftp-avahi-service=y
          CONFIG_PACKAGE_openssh-sftp-client=y
          CONFIG_PACKAGE_openssh-sftp-server=y
          EOF
          # 取消编译VMware镜像以及镜像填充 (不要删除被缩进的注释符号):
          # cat >> .config <<EOF
          # CONFIG_TARGET_IMAGES_PAD is not set
          # CONFIG_VMDK_IMAGES is not set
          # EOF
          #
          # ========================固件定制部分结束========================
          #
          sed -i 's/^[ \t]*//g' ./.config
          make defconfig
      - name: 下载编译源代码
        run: |
          make download -j8
          find dl -size -1024c -exec rm -f {} \;
      - name: 开始编译固件
        run: |
          make -j$(nproc) || make -j1 V=s
          echo "======================="
          echo "Space usage:"
          echo "======================="
          df -h
          echo "======================="
          du -h --max-depth=1 ./ --exclude=build_dir --exclude=bin
          du -h --max-depth=1 ./build_dir
          du -h --max-depth=1 ./bin
      - name: 准备工作
        run: find ./bin/targets/ -type d -name "packages" | xargs rm -rf {}

      - name: 上传固件
        uses: actions/upload-artifact@master
        with:
          name: AIXAN
          path: ./bin/targets/

      - name: 创建发布
        if: github.event == 'push'
        id: create_release
        uses: actions/create-release@v1.0.1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: ${{ github.ref }}
          draft: false
          prerelease: false      

      - name: 上传发布内容
        if: github.event == 'push'
        id: upload-release-asset 
        uses: actions/upload-release-asset@v1.0.2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./bin/targets/*/*/