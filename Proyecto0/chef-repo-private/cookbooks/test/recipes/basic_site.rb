# Cambio en el recetario para hacer el deploy en AWS

# Instalación de Apache y módulos
apache2_install 'default' do
  notifies :restart, 'service[apache2]'
end

apache2_module 'deflate' do
  notifies :reload, 'service[apache2]'
end

apache2_module 'headers' do
  notifies :reload, 'service[apache2]'
end

app_dir = '/var/www/basic_site'

directory app_dir do
  recursive true
  owner 'root'
  group 'root'
end

file "#{app_dir}/index.html" do
  content 'Server 2'
  owner 'root'
  group 'root'
end

# Configuración del sitio
template '/etc/apache2/sites-available/basic_aws_site.conf' do
  source 'basic_aws_site.conf.erb'
  owner 'root'
  group 'root'
  mode '0644'
  variables(
    server_name: node['ec2']['public_ipv4'],
    document_root: app_dir,
    log_dir: '/var/log/apache2',
    site_name: 'basic_site'
  )
  notifies :reload, 'service[apache2]', :delayed
end

# Habilitar el sitio
apache2_site 'basic_site' do
  action :enable
end

# Deshabilitar otros sitios
apache2_site '000-default' do
  action :disable
  notifies :reload, 'service[apache2]'
end

# Habilitar y empezar el servicio de Apache
service 'apache2' do
  action %i(enable start)
end
