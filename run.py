import subprocess
import os
import platform
import json

THINK_ITERATIONS = int(os.environ.get('THINK_ITERATIONS', 100))
WAIT_ITERATIONS = int(os.environ.get('WAIT_ITERATIONS', 50))

DIR = os.path.abspath(os.path.dirname(__file__))

BINARY = 'deeprole_darwin_avx' if platform.system() == 'Darwin' else 'deeprole_linux_avx'

BINARY_PATH = os.path.join(DIR, 'bin', BINARY)
MODEL_DIR = os.path.join(DIR, 'models')

def run_deeprole(node):
    command = [
        BINARY_PATH,
        '--play',
        '--proposer={}'.format(node['proposer']),
        '--succeeds={}'.format(node['succeeds']),
        '--fails={}'.format(node['fails']),
        '--propose_count={}'.format(node['propose_count']),
        '--depth=1',
        '--iterations={}'.format(THINK_ITERATIONS),
        '--witers={}'.format(WAIT_ITERATIONS),
        '--modeldir={}'.format(MODEL_DIR)
    ]
    process = subprocess.run(
        command,
        input=str(node['new_belief']) + "\n",
        text=True,
        capture_output=True
    )

    result = json.loads(process.stdout)
    return result
