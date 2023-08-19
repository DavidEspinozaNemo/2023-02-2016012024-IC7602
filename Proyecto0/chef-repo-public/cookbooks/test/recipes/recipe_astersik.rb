# Instalar Asterisk
execute 'download_asterisk' do
  cd Asterisk
  ldconfig
  groupadd asterisk
  useradd -r -d /var/lib/asterisk -g asterisk asterisk
  usermod -aG audio,dialout asterisk
  chown -R asterisk.asterisk /etc/asterisk
  chown -R asterisk.asterisk /var/{lib,log,spool}/asterisk
  chown -R asterisk.asterisk /usr/lib/asterisk
  systemctl restart asterisk
  systemctl status asterisk
  sed -i 's";\[radius\]"\[radius\]"g' /etc/asterisk/cdr.conf
  sed -i 's";radiuscfg => /usr/local/etc/radiusclient-ng/radiusclient.conf"radiuscfg => /etc/radcli/radiusclient.conf"g' /etc/asterisk/cdr.conf
  sed -i 's";radiuscfg => /usr/local/etc/radiusclient-ng/radiusclient.conf"radiuscfg => /etc/radcli/radiusclient.conf"g' /etc/asterisk/cel.conf
  systemctl restart asterisk

end