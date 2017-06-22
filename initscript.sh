#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
echo "enable_uart=1" >> /boot/config.txt
echo "dtparam=i2c_arm_baudrate=8000" >> /boot/config.txt
