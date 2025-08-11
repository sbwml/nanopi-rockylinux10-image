**Rocky Linux 10 SBC (NanoPi R76s) Minimal 镜像说明**

* **镜像文件**：`Rocky-10-SBC-friendlyarm_nanopi-r76s-10.0-aarch64-minimal.img`
* **默认账号**：

  * 用户名：`root`
  * 密码：`password`
* **网络设置**：WAN / LAN 以太网口默认为 **DHCP** 获取地址
* **自动扩容**：首次启动会自动扩容根分区至整张存储介质
* **内核版本**：`Linux 6.12.41`
* **U-Boot 版本**：`v2025.07`
* **ARM Trusted Firmware (ATF) 版本**：`v2.13.0`
* **TPL 版本**：`rk3576_ddr_lp4_1866MHz_lp5_2736MHz_v1.09.bin`
* **安装到 eMMC**：

  ```bash
  emmc-install Rocky-10-SBC-friendlyarm_nanopi-r76s-10.0-aarch64-minimal.img
  ```
