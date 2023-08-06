import configparser


def write_configuration(filename):
    config = configparser.ConfigParser()
    config['api'] = dict()
    config['api']['username'] = 'admin'
    config['api']['password'] = 'admin'
    config['api']['base_url'] = 'https://emr-practice-staging.herokuapp.com/'

    with open(filename, 'w') as ini_file:
        config.write(ini_file)


if __name__ == '__main__':
    filename = 'emr_sdk.ini'
    write_configuration(filename)
