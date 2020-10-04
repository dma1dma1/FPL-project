from configparser import ConfigParser

def config(filename = 'database.ini', section = 'postgresql'):
    '''
    Gets postgreSQL credentials from 'database.ini' file
    '''
    parser = ConfigParser()
    parser.read(filename)

    creds = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            creds[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in {1}'.format(section, filename))

    return creds