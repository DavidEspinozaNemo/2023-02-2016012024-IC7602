# Receta para la descarga y configuración de FreePBX

execute 'download_freepbx' do
  command 'cd ~'
  command 'cd 2023-02-2016012024-IC7602/Proyecto0/chef-repo-public/freepbx'
  command 'sudo apt-get install nodejs npm -y'
  command 'sudo ./install -n'
end

execute 'configure_freepbx' do
  command 'sed -i \'s/^\(User\|Group\).*/\1 asterisk/\' /etc/apache2/apache2.conf # Se define el usuario de Asterisk dentro de apache'
  command 'sed -i \'s/AllowOverride None/AllowOverride All/\' /etc/apache2/apache2.conf'
  command 'sed -i \'s/\(^upload_max_filesize = \).*/\120M/\' /etc/php/5.6/apache2/php.ini # Se incrementa el tamaño máximo de php.ini'
  command 'sed -i \'s/\(^upload_max_filesize = \).*/\120M/\' /etc/php/5.6/cli/php.ini'
  command 'a2enmod rewrite'
  command 'systemctl restart apache2'
end