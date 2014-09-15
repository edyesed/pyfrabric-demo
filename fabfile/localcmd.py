from fabric.api import local, puts, env, task


@task
def listhosts():
    puts("%s" % env.host)
    #local("/sbin/ifconfig -a | grep ether; echo %s >/dev/null" % (env.host))

