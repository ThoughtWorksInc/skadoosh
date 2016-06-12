from fabric.api import *

# the user to use for the remote commands
env.user = 'ubuntu'
env.key_filename = '~/gladosapp.pem'

# the servers where the commands are executed
env.hosts = ['52.34.28.187']

def pack():
    # create a new source distribution as tarball
    local('python engine/src/setup.py sdist --formats=gztar', capture=False)

def deploy():
    # figure out the release name and version
    # pack()
    dist = local('python engine/src/setup.py --fullname', capture=True).strip()
    # upload the source tarball to the temporary folder on the server
    put('dist/%s.tar.gz' % dist, '~/glados.tar.gz')
    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    run('mkdir -p ~/glados')
    run('pip3 install -r ~/requirements.txt')
    with cd('~/glados'):
        run('tar xzf ~/glados.tar.gz')
        with cd(dist):
            # now setup the package with our virtual environment's
            # python interpreter
            run('python3 engine/src/setup.py install')
            run('python3 ~/engine/src/api/manager.py prod')
    # now that all is set up, delete the folder again
    # run('rm -rf ~/glados.tar.gz')
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    # run('touch /home/ubuntu/fbeazt/glados_wsgi.py')
