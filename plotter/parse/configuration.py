import os
import yaml

from plotter.utilities.exceptions import InvalidYAMLConfigException

CONFIG_LOCATION = 'S:/Cloud Storage/Github/plotter/config.yaml'


def _get_config():
    if not os.path.exists(CONFIG_LOCATION):
        raise FileNotFoundError("Was unable to find the config.yaml file.")
    f = open(CONFIG_LOCATION, 'r')
    config = yaml.load(stream=f, Loader=yaml.Loader)
    f.close()
    return config


def _get_chia_location(config):
    return config.get('chia_location', 'chia')


def _get_log_location(config):
    if 'log_location' not in config:
        raise InvalidYAMLConfigException('Failed to find the log_location parameter in the YAML.')
    log_location = config['log_location']
    failed_checks = []
    checks = ['folder_path', 'check_seconds']
    for check in checks:
        if check in log_location:
            continue
        failed_checks.append(check)

    if failed_checks:
        raise InvalidYAMLConfigException(f'Failed to find the following parameters in log_location: '
                                         f'{", ".join(failed_checks)}')

    return log_location['folder_path'], log_location['check_seconds']


def _get_jobs(config):
    if 'jobs' not in config:
        raise InvalidYAMLConfigException('Failed to find the jobs parameter in the YAML.')
    return config['jobs']


def get_config_info():
    config = _get_config()
    chia_location = _get_chia_location(config=config)
    log_directory, log_check_seconds = _get_log_location(config=config)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    jobs = _get_jobs(config=config)
    return chia_location, log_directory, jobs, log_check_seconds