# Copyright 2015–2020 Ben Sturmfels
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import io
import sys
import os

import invoke
from jinja2 import Template
from patchwork.files import exists


def transfer_files_git(c, push_to_origin=True):
    if push_to_origin:
        c.local(f'git push origin {c.env.branch}')
    c.sudo(f'mkdir -p {c.env.project_dir}')
    c.sudo(f'chown {c.user} {c.env.project_dir}')

    with c.cd(c.env.project_dir):
        c.run('git init --quiet')
        c.run('git config receive.denyCurrentBranch ignore')

    c.local("git push {c.user}@{c.host}:{env.project_dir} {env.branch}".format(
        env=c.env,
        c=c,
    ))
    with c.cd(c.env.project_dir):
        c.run(f"git reset --hard {c.env.branch} --")


def transfer_files_git_pull(c):
    """A custom transfer_files_git that pulls rather than pushes changes.

    If the repository is private, you may need some sort of token. For GitLab,
    this would be a "deploy token" deploy token in the configuration of the
    "origin" remote, eg.

    git remote add origin https://gitlab+deploy-token-XXXXXX:YYYYYYYYYYYYYYYYYYYY@gitlab.com/your-project/your-repo.git

    """
    c.sudo(f'mkdir -p {c.env.project_dir}')
    c.sudo('chown {env.user} {env.project_dir}'.format(env=c.env))

    with c.cd(c.env.project_dir):
        c.run('git init --quiet')
        c.run('git config receive.denyCurrentBranch ignore')
        c.run(f'git fetch origin {c.env.branch}')
        c.run(f'git reset --hard origin/{c.env.branch}')


def init(c):
    """Misc first-time run things."""
    if not exists(c, f'{c.env.project_dir}/env'):
        c.run(f'touch {c.env.project_dir}/env')
    media_dir = os.path.join(c.env.project_dir, c.env.media_dir)
    if not exists(c, media_dir):
        c.run(f'mkdir -p {media_dir}')


def prepare_virtualenv(c):
    """Initialise a virtualenv and install required Python modules."""

    if not exists(c, c.env.virtualenv):
        c.sudo(f"mkdir -p $(dirname {c.env.virtualenv})")
        c.sudo(f'chown {c.user} $(dirname {c.env.virtualenv})')

        c.run("{env.python} -m venv --system-site-packages {env.virtualenv}".format(env=c.env))
    with c.cd(c.env.project_dir):
        c.run("{env.virtualenv}/bin/python -m pip install -r {env.requirements}".format(
            env=c.env))


def prepare_django(c, fail_level='WARNING'):
    # Clear all Python bytecode, just in case we've upgraded Python.
    c.sudo(f'find {c.env.project_dir} -type d -name __pycache__ -exec rm -rf {{}} +') # Python 3

    with c.cd(c.env.project_dir):
        with c.prefix(f'source {c.env.project_dir}/env'):
            # Test configuration before we attempt to restart the application server.
            fail_level_arg = ''
            if fail_level:
                fail_level_arg = f'--fail-level={fail_level}'
            c.run('{env.virtualenv}/bin/python manage.py check --deploy {fail_level_arg} --settings={env.settings}'.format(
                env=c.env, fail_level_arg=fail_level_arg, user=c.env.app_user))

            # Collect static files.
            c.run('{env.virtualenv}/bin/python manage.py collectstatic --settings={env.settings} -v0 --noinput --clear'.format(
                env=c.env))

            # Migrate.
            #
            # Printing unicode characters during a migration can fail if remote
            # locale is something like "POSIX". Run `locale` to check.
            with c.prefix('LC_ALL=en_AU.utf8'):
                c.run('{env.virtualenv}/bin/python manage.py migrate --settings={env.settings}'.format(
                    env=c.env))


def fix_permissions(c, read=None, read_write=None):
    """Ensure permissions are set correctly to run site as unprivileged user."""

    if read is None:
        read = []

    if read_write is None:
        read_write = []

    # Uploading user owns the files. Web server/app user has access via group.
    # Others have no access.
    c.sudo('chown --recursive {c.user}:{env.app_user} {env.project_dir}'.format(c=c, env=c.env))
    c.sudo(f'chmod --recursive u=rwX,g=,o= {c.env.project_dir}')

    # Assume we always need read access to project directory.
    c.sudo(f'chmod g+rX {c.env.project_dir}')

    for path in read:
        c.sudo(f'chmod --recursive g+rX {os.path.join(c.env.project_dir, path)}')
    for path in read_write:
        c.sudo(f'chmod --recursive g+rwX {os.path.join(c.env.project_dir, path)}')


def _sudo_upload_template(c, local_path, remote_path, mode, owner=None, group=None):
    # My hacked up replacement for upload template is permanently sudo and uses
    # full Jinja2 by default (both unlike Fabric 1).
    owner = c.user if owner is None else owner
    group = c.user if group is None else group
    with open(local_path) as f:
        content = f.read()
    t = Template(content)
    output = t.render(env=c.env, **c.env) # Both env.X and just X.
    m = io.StringIO(output)
    c.put(m, '/tmp/X')
    c.sudo(f'mv /tmp/X {remote_path}')
    c.sudo('chown {owner}:{group} {remote_path}'.format(
        owner=owner, group=group, mode=mode, remote_path=remote_path))
    c.sudo(f'chmod {mode} {remote_path}')


def reload_uwsgi(c):
    _sudo_upload_template(
        c, c.env.uwsgi_conf, f'/etc/uwsgi-emperor/vassals/{c.env.site_name}.ini', '644')

    # Append secrets to uWSGI config on-the-fly.
    #
    # uWSGI config format for environment variables is different to a file
    # you might `source`. It has "env = " at the start instead of export,
    # doesn't mind whitespace in the values and treats quotes literally.
    #
    # See here on getting quotes right in Fabric
    # https://lists.gnu.org/archive/html/fab-user/2013-01/msg00005.html.

    # Don't use percent characters in environment variables because uWSGI will
    # silently drop them unless they are doubled-up (meaning that you'll have a
    # hard time tracking down the subtle bug).
    try:
        c.run(f"! grep '%' {c.env.project_dir}/env")
    except invoke.exceptions.UnexpectedExit as e:
        print('Environment variables should not contain "%" due to its special use in uWSGI config.', file=sys.stderr)
        raise

    # Removes quotes as these are interpreted literally by uWSGI.
    c.sudo(f'echo "" >> /etc/uwsgi-emperor/vassals/{c.env.site_name}.ini')
    c.sudo("""sed 's/export/env =/' {env.project_dir}/env | sed "s/['\\"]//g" >> /etc/uwsgi-emperor/vassals/{env.site_name}.ini""".format(env=c.env))


def flush_memcached(c):
    """Clear cache by restarting the memcached server.

    By design, any user on the system can issue commands to memcached, including
    to flush the whole cache. Alternately, we could install libmemcached-tools
    and run `memcflush --servers localhost`.

    """
    c.run("echo flush_all | nc -w1 localhost 11211")


def update_nginx(c):
    _sudo_upload_template(
        c, c.env.nginx_conf, f'/etc/nginx/sites-available/{c.env.site_name}', '644')
    c.sudo("ln -s --force /etc/nginx/sites-available/{env.site_name} /etc/nginx/sites-enabled/{env.site_name}".format(
            env=c.env))
    c.sudo("/usr/sbin/nginx -t")
    c.sudo("/etc/init.d/nginx force-reload")


def download_postgres_db(c):
    tempfile = c.run('tempfile').stdout.strip()
    c.sudo('pg_dump --format=c {env.db_name} > {tempfile}'.format(
        env=c.env, tempfile=tempfile), user='postgres', pty=True)
    localtempfile = '{env.site_name}-{time:%Y-%m-%dT%H:%M:%S}.dump'.format(
        env=c.env, time=datetime.datetime.now())
    c.get(tempfile, localtempfile)
    # localtempfile = get(tempfile, local_path='%(basename)s')[0]
    c.sudo(f'rm -f {tempfile}')
    return localtempfile


def mirror_postgres_db(c):
    localtempfile = download_postgres_db(c)
    c.local(f'dropdb --if-exists {c.env.db_name}')
    c.local(f'createdb {c.env.db_name}')

    # Using sudo here avoids permission errors relating to extensions.
    #
    # Tried removing the above drop and create and adding --clean --create
    # below, but I get a whole bunch of errors relating to things already being
    # in the database.
    c.local('pg_restore --no-owner --no-privileges --dbname={env.db_name} {localtempfile}'.format(
        env=c.env, localtempfile=localtempfile), warn=True)

    c.local(f"""psql {c.env.db_name} -c "update django_site set domain = '127.0.0.1:8000'" """, warn=True)
    print('You may want to run:\npython3 -m django createsuperuser --username=admin --email=sysadmin@sturm.com.au')


def mirror_media(c):
    c.local('rsync -avz {c.user}@{c.host}:{env.project_dir}/{env.media_dir}/ {env.media_dir}'.format(
        c=c, env=c.env))


def lint(c):
    """Run Pylint over everything."""

    # --jobs=0 enable parallelism based on number of cores available.
    c.local("git ls-files '*.py' | xargs python3 -m pylint --jobs=0 --rcfile=pylint.conf")


def flake8_test(c):
    # See .flake8 for excluded checks.
    c.local("git ls-files '*.py' | xargs python3 -m flake8")


def mypy_test(c):
    c.local("git ls-files '*.py' | xargs python3 -m mypy --config-file mypy.ini")


def grep_for_pdb(c, exclude=None):
    """Check that code doesn't ever call the debugger.

    Doing so in production would lock up worker processes.

    """
    if exclude is None:
        exclude = []
    elif isinstance(exclude, str):
        exclude = exclude.split(',')
    exclude += ['fabfile.py']
    exclusions = ' '.join([f"-path './{ex}' -prune -o" for ex in exclude])
    c.local(f"! find {exclusions} -name '*.py' -exec grep -n '\\bpdb\\b' {{}} +")


def django_test(c):
    c.local('python3 manage.py test --keepdb')


def check_site_online(c):
    """Perform a basic check so we know immediately if the website is down."""

    # TODO: Is there a better way to make invoke fail loudly?
    try:
        c.run(f'curl --silent --head {c.env.url} | grep --perl-regexp "^HTTP/.+ 200"')
    except invoke.UnexpectedExit:
        raise invoke.Exit('Site check failed!')


def install_scheduled_jobs(c, periodic_jobs=None, crontabs=None):
    periodic_jobs = [] if periodic_jobs is None else periodic_jobs
    crontabs = [] if crontabs is None else crontabs

    typical_periodic_jobs = {
        'cron.hourly',
        'cron.daily',
        'cron.weekly',
        'cron.monthly',
    }
    for job in periodic_jobs:
        basename = os.path.basename(job)
        if basename in typical_periodic_jobs:
            _sudo_upload_template(
                c,
                job,
                f'/etc/{basename}/{c.env.site_name}',
                '755',
            )
        else:
            raise RuntimeError(f'Unexpected periodic job: {job}')
    for crontab in crontabs:
        name = os.path.basename(crontab).replace('cron.', '')
        _sudo_upload_template(
            c,
            crontab,
            f'/etc/cron.d/{c.env.site_name}-{name}',
            '644',
            'root',
            'root',
        )


def django_shell(c):
    with c.cd(c.env.project_dir):
        c.run('source ./env && DJANGO_SETTINGS_MODULE={env.settings} {env.virtualenv}/bin/python manage.py shell'.format(env=c.env), pty=True)


def bash(c):
    with c.cd(c.env.project_dir):
        c.run('bash', pty=True)
