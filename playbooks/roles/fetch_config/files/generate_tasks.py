import yaml
import os
import json

def load_config_files(base_path):
    configs = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.yml'):
                with open(os.path.join(root, file), 'r') as f:
                    config = yaml.safe_load(f)
                    configs.append((config, root.split('/')[-1], file))
    return configs

def main():
    base_path = '/tmp/config_files/'
    tasks = []
    errors = []

    configs = load_config_files(base_path)
    for config, server, filename in configs:
        for app in config.get('app-list', []):
            for module in app.get('module-list', []):
                try:
                    task = {
                        'app': app['name'],
                        'module': module['name'],
                        'server': server,
                        'profile': module['profile'],
                        'npa_list': [npa for npa in module.get('npa-list', [])],
                        'restart_command': module.get('restart-command'),
                        'mail': module['mail']
                    }
                    tasks.append(task)
                except Exception as e:
                    errors.append({
                        'app': app.get('name'),
                        'module': module.get('name'),
                        'server': server,
                        'mail': module.get('mail', 'infra@ing-test.com'),
                        'config_file': filename,
                        'error': str(e)
                    })

    with open('/tmp/tasks.json', 'w') as f:
        json.dump({'tasks': tasks}, f)

    with open('/tmp/errors.json', 'w') as f:
        json.dump({'errors': errors}, f)

if __name__ == '__main__':
    main()
