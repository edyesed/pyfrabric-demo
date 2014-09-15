from __future__ import with_statement
from boto.ec2 import EC2Connection as ec2c
from fabric.api import run, task, parallel, serial, execute, runs_once, hide, puts
from fabric.api import settings as fab_settings
from pprint import pprint


@task
@parallel
#@serial
def _get_uname():
    with fab_settings(warn_only=True):
    #with fab_settings(hide('running', 'stderr', 'stdout', 'warnings'),
    #                  warn_only=True):
        return run('uname -a')
        ### VS
        #run('uname -a')

    
@task
@runs_once
def puname(filter=None):
    with fab_settings(hide('running','stderr','stdout','warnings'),
                      warn_only=True):
        results = execute(_get_uname)
        #pprint(results)
        for r in results.iteritems():
            if filter is None:
                print("%s  -> %s" % (r[0], r[1].upper()))
            else:
                if filter.upper() in r[1].upper():
                    print("%s  -> %s" % (r[0], r[1].upper()))

