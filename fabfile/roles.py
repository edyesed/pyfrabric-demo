from __future__ import with_statement
from boto.ec2 import EC2Connection as ec2c
from fabric.api import local, abort, run, cd, task, env, puts
from fabric.api import settings as fab_settings
import re


HERP=eval(open('/Users/edanderson/.creds/fabric_demo').read())
EC2 = ec2c(HERP['ID'], HERP['SECRET'])

class BaseRole(object):
    """Roll your own roles
    """
    def __init__(self, port=None):
        if port is None:
            port = 22
        self.port = port

    def instances(self):
        raise NotImplementedError()

    def __iter__(self):
        for instance in self.instances():
            yield "%s:%d" % (instance.ip_address, self.port)
            

class RegexRole(BaseRole):
    """Roles by Regex
    """
    def __init__(self, host_re):
        super(RegexRole, self).__init__()
        self.hostre = host_re
        self._re = re.compile(host_re)
        self._hosts = None

    def instances(self):
        rez = EC2.get_all_instances(filters={"instance-state-name":"running"})
        for r in rez:
            for i in r.instances:
                name =  i.tags.get('Name','')
                if self._re.match(name):
                   yield i


env.roledefs.update({
    'dars': RegexRole('^dar'),
    'erps': RegexRole('erp$'),
    'all': RegexRole('.')
    })

@task
def list_roles():
    printstr = "{0:10} | {1:20}"
    puts(printstr.format("#ROLE", "RE_PATTERN"))
    for role in env.roledefs:
        puts(printstr.format(role, env.roledefs[role]._re.pattern))
