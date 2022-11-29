import yaml


class Config(object):
    """Main app config"""
    def __init__(self, conf_file):
        self.conf_file = conf_file
        self.conf = self._read_config()
        self.conf = self._validate_config()

    def _read_config(self):
        cfg = None
        with open(self.conf_file, 'r') as conf_file:
            cfg = yaml.load(conf_file)
        return cfg

    def _validate_config(self):
        dashboards = self.conf['dashboards']
        drv_types = ['firefox', 'chrome']
        app_types = ['default', 'grafana', 'jenkins', 'monitor', 'hdb', 'bareos-dir', 'targetprocess']
        for i in dashboards:
            if not dashboards[i].get('url'):
                print("Bad 'url' settins defined in {section}".format(section=dashboards[i]['name']))
                return None

            if not dashboards[i].get('driver') or dashboards[i].get('driver') not in drv_types:
                print("Bad 'driver' settins defined in {section}".format(section=dashboards[i]['name']))
                return None

            if not dashboards[i].get('application') or dashboards[i].get('application') not in app_types:
                print("Bad 'application' settins defined in {section}".format(section=dashboards[i]['name']))
                return None

            if not dashboards[i].get('user') and not dashboards[i].get('password'):
                dashboards[i]['user'] = ""
                dashboards[i]['password'] = ""

            if dashboards[i].get('user') and not dashboards[i].get('password'):
                dashboards[i]['password'] = ""

            if not dashboards[i].get('tab'):
                dashboards[i]['tab'] = ""

            if not dashboards[i].get('x'):
                dashboards[i]['x'] = 0
            else:
                dashboards[i]['x'] = int(dashboards[i]['x'])

            if not dashboards[i].get('y'):
                dashboards[i]['y'] = 0
            else:
                dashboards[i]['y'] = int(dashboards[i]['y'])

            if not dashboards[i].get('height'):
                dashboards[i]['height'] = 200
            else:
                dashboards[i]['height'] = int(dashboards[i]['height'])

            if not dashboards[i].get('width'):
                dashboards[i]['width'] = 200
            else:
                dashboards[i]['width'] = int(dashboards[i]['width'])

            if not dashboards[i].get('refresh'):
                dashboards[i]['refresh'] = 600
            else:
                dashboards[i]['refresh'] = int(dashboards[i]['refresh'])

            if not dashboards[i].get('zoom'):
                dashboards[i]['zoom'] = 100
            else:
                dashboards[i]['zoom'] = int(dashboards[i]['zoom'])

            if not dashboards[i].get('fullscreen'):
                dashboards[i]['fullscreen'] = False

        return self.conf


    @property
    def dashboards(self):
        return self.conf['dashboards']
