# chef-solo-recipe.rb

# Instalar Asterisk
execute 'download_asterisk' do
    command 'sudo apt-get install subversion'
    command 'wget http://downloads.asterisk.org/pub/telephony/asterisk/asterisk-18-current.tar.gz'
    command 'tar -xvzf asterisk-18-current.tar.gz'
    command 'cd asterisk-18.19.0'
    command 'sudo contrib/scripts/get_mp3_source.sh'
    command 'sudo contrib/scripts/install_prereq install'
    command ' apt-get install gcc'
    command './configure'
    command 'sudo apt install make'
    command 'make menuselect'
  end
  
  # Configurar Asterisk
  group 'asterisk'
  
  user 'asterisk' do
    system true
    home '/var/lib/asterisk'
    gid 'asterisk'
  end
  
  execute 'change_asterisk_user_group' do
    command 'chown -R asterisk.asterisk /etc/asterisk'
  end
  
  execute 'change_asterisk_var' do
    command 'chown -R asterisk.asterisk /var/{lib,log,spool}/asterisk'
  end
  
  execute 'change_asterisk_lib' do
    command 'chown -R asterisk.asterisk /usr/lib/asterisk'
  end
  
  template '/etc/default/asterisk' do
    source 'asterisk_default.erb'
  end
  
  template '/etc/asterisk/asterisk.conf' do
    source 'asterisk_conf.erb'
  end
  
  service 'asterisk' do
    action :restart
  end
  
  execute 'fix_cdr_conf' do
    command "sed -i 's/\";\\[radius\\]\"/\"[radius]\"/g' /etc/asterisk/cdr.conf"
  end
  
  execute 'fix_radiuscfg' do
    command "sed -i 's/\"radiuscfg => \\/usr\\/local\\/etc\\/radiusclient-ng\\/radiusclient.conf\"/\"radiuscfg => \\/etc\\/radcli\\/radiusclient.conf\"/g' /etc/asterisk/cdr.conf"
  end
  
  execute 'fix_radiuscfg_cel' do
    command "sed -i 's/\"radiuscfg => \\/usr\\/local\\/etc\\/radiusclient-ng\\/radiusclient.conf\"/\"radiuscfg => \\/etc\\/radcli\\/radiusclient.conf\"/g' /etc/asterisk/cel.conf"
  end
  
  service 'asterisk' do
    action :restart
  end
  
  # Instalar FreePBX
  package 'software-properties-common'
  
  execute 'add_php_ppa' do
    command 'add-apt-repository ppa:ondrej/php -y'
  end
  
  package %w(apache2 mariadb-server libapache2-mod-php7.2 php7.2 php-pear php7.2-cgi php7.2-common php7.2-curl php7.2-mbstring php7.2-gd php7.2-mysql php7.2-bcmath php7.2-zip php7.2-xml php7.2-imap php7.2-json php7.2-snmp) do
    action :install
  end
  
  execute 'download_freepbx' do
    command 'wget http://mirror.freepbx.org/modules/packages/freepbx/freepbx-15.0-latest.tgz'
    cwd '/tmp'
  end
  
  execute 'extract_freepbx' do
    command 'tar -xvzf freepbx-15.0-latest.tgz'
    cwd '/tmp/freepbx'
  end
  
  package %w(nodejs npm) do
    action :install
  end
  
  execute 'install_freepbx' do
    command './install -n'
    cwd '/tmp/freepbx'
  end
  
  execute 'install_pm2' do
    command 'fwconsole ma install pm2'
  end
  
  execute 'modify_apache_user' do
    command "sed -i 's/^\\(User\\|Group\\).*/\\1 asterisk/' /etc/apache2/apache2.conf"
  end
  
  execute 'modify_apache_allowoverride' do
    command "sed -i 's/AllowOverride None/AllowOverride All/' /etc/apache2/apache2.conf"
  end
  
  execute 'increase_upload_max_filesize' do
    command "sed -i 's/^\\(upload_max_filesize = \\).*/\\120M/' /etc/php/7.2/apache2/php.ini"
  end
  
  execute 'increase_upload_max_filesize_cli' do
    command "sed -i 's/^\\(upload_max_filesize = \\).*/\\120M/' /etc/php/7.2/cli/php.ini"
  end
  
  execute 'enable_apache_rewrite_module' do
    command 'a2enmod rewrite'
  end
  
  service 'apache2' do
    action :restart
  end
  