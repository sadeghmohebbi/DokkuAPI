from sys import stdout
from commands.ssh import run_command, run_root_command


def __execute_command(command):
    stdout.write(f'\nExecuting command: {command}\n')
    success, message = run_command(command)
    stdout.write(f'Result: {success}\n')
    stdout.write(f'Output: {message}\n')
    return True


def __execute_root_command(command):
    stdout.write(f'\nExecuting root command: {command}\n')
    success, message = run_root_command(command)
    stdout.write(f'Result: {success}\n')
    stdout.write(f'Output: {message}\n')
    return True


# Creates an application
def create_app(app_name):
    command = f'apps:create {app_name}'
    return __execute_command(command)


# Deletes an application
def delete_app(app_name):
    command = f'--force apps:destroy {app_name}'
    return __execute_command(command)


# Lists all applications
def list_apps():
    command = 'apps:list'
    return __execute_command(command)


# List plugins
def list_plugins():
    command = 'plugin:list'
    return __execute_command(command)


# Check if a plugin is installed
def is_plugin_installed(plugin_name):
    success, message = list_plugins()
    if success:
        for plugin in message.split('\n'):
            if plugin_name in plugin:
                return True
        stdout.write('Result: Plugin is not installed\n')
    return False


# Install a plugin
def install_plugin(plugin_name):
    if plugin_name == 'postgres':
        command = 'plugin:install https://github.com/dokku/dokku-postgres.git'
    elif plugin_name == 'mysql':
        command = 'plugin:install https://github.com/dokku/dokku-mysql.git mysql'
    elif plugin_name == 'letsencrypt':
        command = 'plugin:install https://github.com/dokku/dokku-letsencrypt.git'
    else:
        stdout.write('Result: Plugin not found\n')
        return False
    return __execute_root_command(command)


# Uninstall a plugin
def uninstall_plugin(plugin_name):
    command = f'plugin:uninstall {plugin_name}'
    return __execute_root_command(command)


# Create a database
def create_database(plugin_name, database_name):
    if plugin_name != 'postgres' and plugin_name != 'mysql':
        stdout.write('Result: Plugin not found\n')
        return False
    command = f'{plugin_name}:create {database_name}'
    return __execute_command(command)


# List databases
def list_databases(plugin_name):
    if plugin_name != 'postgres' and plugin_name != 'mysql':
        stdout.write('Result: Plugin not found\n')
        return False
    command = f'{plugin_name}:list'
    return __execute_command(command)


# Check if a database exists
def database_exists(plugin_name, database_name):
    if plugin_name != 'postgres' and plugin_name != 'mysql':
        stdout.write('Result: Plugin not found\n')
        return False
    success, message = list_databases(plugin_name)
    if success:
        for database in message.split('\n'):
            if database_name in database:
                return True
        stdout.write('Result: Database does not exist\n')
    return False


# Delete a database
def delete_database(plugin_name, database_name):
    if plugin_name != 'postgres' and plugin_name != 'mysql':
        stdout.write('Result: Plugin not found\n')
        return False
    command = f'--force {plugin_name}:destroy {database_name}'
    return __execute_command(command)


# List linked apps
def database_linked_apps(plugin_name, database_name):
    if plugin_name != 'postgres' and plugin_name != 'mysql':
        stdout.write('Result: Plugin not found\n')
        return False
    command = f'{plugin_name}:links {database_name}'
    return __execute_command(command)


# Link database to an app
def link_database(plugin_name, database_name, app_name):
    if plugin_name != 'postgres' and plugin_name != 'mysql':
        stdout.write('Result: Plugin not found\n')
        return False
    command = f'--no-restart {plugin_name}:link {database_name} {app_name}'
    return __execute_command(command)


# Unlink database from an app
def unlink_database(plugin_name, database_name, app_name):
    if plugin_name != 'postgres' and plugin_name != 'mysql':
        stdout.write('Result: Plugin not found\n')
        return False
    command = f'--no-restart {plugin_name}:unlink {database_name} {app_name}'
    return __execute_command(command)


# Set domain for an app
def set_domain(app_name, domain):
    command = f'domains:set {app_name} {domain}'
    return __execute_command(command)


# Remove domain for an app
def remove_domain(app_name, domain):
    command = f'domains:remove {app_name} {domain}'
    return __execute_command(command)


# Set LetsEncrypt mail
def set_letsencrypt_mail(email):
    command = f'config:set --global DOKKU_LETSENCRYPT_EMAIL={email}'
    return __execute_command(command)


# Enable LetsEncrypt for an app
def enable_letsencrypt(app_name):
    command = f'letsencrypt:enable {app_name}'
    return __execute_command(command)


# Enable LetsEncrypt auto renewal
def enable_letsencrypt_auto_renewal():
    command = f'letsencrypt:cron-job --add'
    return __execute_command(command)


# List application configurations
def config_show(app_name):
    command = f'config:show {app_name}'
    return __execute_command(command)


# Set application configuration key
def config_set(app_name, key, value):
    command = f'config:set --no-restart {app_name} {key}={value}'
    return __execute_command(command)


# Unset application configuration key
def config_unset(app_name, key):
    command = f'config:unset --no-restart {app_name} {key}'
    return __execute_command(command)


# Set application configuration from file
def config_file(app_name, contents):
    keys = ''
    cleaned_contents = contents.decode('utf-8').replace('\r', '')
    list_of_lines = cleaned_contents.split('\n')
    for line in list_of_lines:
        if line != '':
            if line.startswith('#'):
                continue
            keys = keys + line + ' '
    command = f'config:set --no-restart {app_name} {keys}'
    return __execute_command(command)


# Apply application configuration
def config_apply(app_name):
    command = f'ps:rebuild {app_name}'
    return __execute_command(command)


# create a storage
def storage_create(volume_name):
    command = f'storage:ensure-directory {volume_name} --chown false'
    return __execute_command(command)


# mount a storage
def storage_mount(app_name, mount_point_left, mount_point_right):
    command = f'storage:mount {app_name} {mount_point_left}:{mount_point_right}'
    return __execute_command(command)


# authenticate git server
def git_auth(host, username, password):
    command = f'git:auth {host} {username} {password}'
    return __execute_command(command)


# clone for docker image
def git_from_image(app_name, docker_image):
    command = f'git:from-image {app_name} {docker_image}'
    return __execute_command(command)


def proxy_set_ports(app_name, port_mappings):
    command = f'proxy:ports-set {app_name} {port_mappings}'
    return __execute_command(command)
