# checkmAIt

## Requirements

- pyusb

Also: 
	groupadd lego 
	usermod -a -G lego [username] 
	echo 'BUS=="usb", SYSFS{idVendor}=="0694", GROUP="lego", MODE="0660"' /etc/udev/rules.d/70-lego.rules 
