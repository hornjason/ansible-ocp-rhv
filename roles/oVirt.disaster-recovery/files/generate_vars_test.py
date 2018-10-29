import subprocess
import pexpect
import os

from contextlib import contextmanager

import pytest


@contextmanager
def generator(tmpdir):
    env = dict(os.environ)
    env["PYTHONUNBUFFERED"] = "x"
    env["GENERATE_VARS_CONF_DIR"] = str(tmpdir)
    env["GENERATE_VARS_OUT_DIR"] = str(tmpdir)
    gen = pexpect.spawn('./generate-vars', env=env)
    try:
        yield gen
    finally:
        gen.terminate(force=True)


INITIAL_CONF = """
[generate_vars]
"""


def test_initial_conf(tmpdir):
    conf = tmpdir.join("dr.conf")
    conf.write(INITIAL_CONF)
    with generator(tmpdir) as g:
        # TODO: Use regex
        g.expect('override')
        # Add dry run
        g.sendline('y')
        # "/tmp/dr_ovirt-ansible/mapping_vars.yml"
        assert os.path.exists("/tmp/dr_ovirt-ansible/mapping_vars.yml")
