execute 'asterisk' do
    command 'sudo systemctl restart asterisk'
  end
  
  execute 'apache-download' do
    command 'sudo apt update'
    command 'sudo apt install apache2'
  end

  file '/var/www/html/index.html' do
    content '<html>Server1.</html>'
  end

    execute 'apache-init' do
    command 'sudo a2ensite 000-default.conf'
    command 'sudo service apache2 reload'
  end
  
  execute 'pbx' do
    command 'sudo sed -i \'s/^\(User\|Group\).*/\1 asterisk/\' /etc/apache2/apache2.conf' # Se define el usuario de Asterisk dentro de apache
    command 'sudo sed -i \'s/AllowOverride None/AllowOverride All/\' /etc/apache2/apache2.conf'
    command 'sudo sed -i \'s/\(^upload_max_filesize = \).*/\120M/\' /etc/php/5.6/apache2/php.ini' # Se incrementa el tamaño máximo de php.ini
    command 'sudo sed -i \'s/\(^upload_max_filesize = \).*/\120M/\' /etc/php/5.6/cli/php.ini'
    command 'sudo rm -Rf /var/www/html/admin/modules/extensionroutes/'
    command 'sudo a2enmod rewrite'
    command 'sudo systemctl restart apache2'
  end

#if blank screen
#fwconsole ma enableall
#fwconsole ma upgradeall
#fwconsole ma upgrade framework --edge
#fwconsole restart