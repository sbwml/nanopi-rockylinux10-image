**Rocky Linux 10 SBC (NanoPi R76s) Minimal Image Instructions**

* **Image file**: `Rocky-10-SBC-friendlyarm_nanopi-r76s-10.0-aarch64-minimal.img`
* **Default account**:

  * Username: `root`
  * Password: `password`
* **Network**: WAN / LAN Ethernet ports are set to **DHCP** by default
* **Auto expansion**: Root partition will automatically expand to fill the entire storage device on first boot
* **Kernel version**: `Linux 6.12.42`
* **U-Boot version**: `v2025.07`
* **ARM Trusted Firmware (ATF) version**: `v2.13.0`
* **TPL version**: `rk3576_ddr_lp4_1866MHz_lp5_2736MHz_v1.09.bin`
* **Install to eMMC**:

  ```bash
  emmc-install Rocky-10-SBC-friendlyarm_nanopi-r76s-10.0-aarch64-minimal.img
  ```
