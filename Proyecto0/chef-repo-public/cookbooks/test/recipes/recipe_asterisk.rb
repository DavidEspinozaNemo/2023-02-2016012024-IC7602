# Receta para la instalación y configuración de Asterisk

execute 'download_asterisk' do

  command 'cd 2023-02-2016012024-IC7602/Proyecto0/chef-repo-public/asterisk-18.19.0'
  command 'ldconfig'

end

execute 'asterisk_permissions' do

  command 'groupadd asterisk' # Se crea un usuario y grupo dedicado
  command 'useradd -r -d /var/lib/asterisk -g asterisk asterisk'
  command 'usermod -aG audio,dialout asterisk' # Se da audio al grupo
  command 'chown -R asterisk.asterisk /etc/asterisk' # Se configuran los permisos
  command 'chown -R asterisk.asterisk /var/{lib,log,spool}/asterisk'
  command 'chown -R asterisk.asterisk /usr/lib/asterisk'

end

execute 'error_fix' do

  command 'systemctl status asterisk'
  command 'sed -i \'s";\[radius\]"\[radius\]"g\' /etc/asterisk/cdr.conf'
  command 'sed -i \'s";radiuscfg => /usr/local/etc/radiusclient-ng/radiusclient.conf"radiuscfg => /etc/radcli/radiusclient.conf"g\' /etc/asterisk/cdr.conf'
  command 'sed -i \'s";radiuscfg => /usr/local/etc/radiusclient-ng/radiusclient.conf"radiuscfg => /etc/radcli/radiusclient.conf"g\' /etc/asterisk/cel.conf'
  command 'systemctl restart asterisk'

end