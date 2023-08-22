execute 'apache-download' do
  command 'sudo apt update'
  command 'sudo apt install apache2'
end

file '/var/www/html/index.html' do
  content '<html>Server2.</html>'
end

execute 'apache-init' do
  command 'sudo a2ensite 000-default.conf'
  command 'sudo service apache2 reload'
end
  

#if blank screen
#fwconsole ma enableall
#fwconsole ma upgradeall
#fwconsole ma upgrade framework --edge
#fwconsole restart