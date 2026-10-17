"""Install the worker for the current Linux user; never starts billable work."""
import argparse
import importlib.util
import os
from pathlib import Path
import subprocess
import sys

def quoted(path):
    return '"'+str(path).replace('\\','\\\\').replace('"','\\"').replace('%','%%')+'"'

def install(root, home, dry_run=False):
    root=Path(root).resolve();home=Path(home).resolve()
    config=home/'.config/energy-culture-worker'
    state=home/'.local/state/energy-culture-worker'
    units=home/'.config/systemd/user'
    unit=units/'energy-culture-worker.service'
    env=config/'worker.env'
    for p in [config,state,units]:
        if p.is_symlink(): raise RuntimeError('Refusing a symlink configuration directory')
        p.mkdir(parents=True,exist_ok=True,mode=0o700)
    if env.is_symlink() or unit.is_symlink():raise RuntimeError('Refusing a symlink configuration file')
    if not env.exists():
        fd=os.open(env,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w') as out:
            out.write('OPENAI_API_KEY=\nOPENAI_MODEL=gpt-5-mini\nWORKER_DAILY_CALLS=0\nWORKER_MAX_ROUNDS=12\n')
    env.chmod(0o600)
    unit.write_text('[Unit]\nDescription=Energy Culture continuous worker\n\n[Service]\nType=simple\n'
        +'WorkingDirectory='+str(root).replace('%','%%')+'\nEnvironmentFile='+str(env).replace('%','%%')+'\n'
        +'ExecStart='+quoted(sys.executable)+' '+quoted(root/'ops/continuous-worker/worker.py')
        +' run --root '+quoted(root)+' --state '+quoted(state)+'\n'
        +'Restart=on-failure\nRestartSec=10\nTimeoutStopSec=150\nUMask=0077\n'
        +'NoNewPrivileges=true\n\n[Install]\nWantedBy=default.target\n')
    spec=importlib.util.spec_from_file_location('ecworker',root/'ops/continuous-worker/worker.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    store=module.Store(state/'queue.sqlite3')
    store.enqueue('lead-runner-build-1',(root/'ops/continuous-worker/lead-runner-job.md').read_text())
    if not dry_run:
        subprocess.run(['systemctl','--user','daemon-reload'],check=True)
        subprocess.run(['systemctl','--user','enable','energy-culture-worker.service'],check=True)
    print('Worker service installed; build job saved. Service NOT started.')
    print('Paid API calls remain disabled. Credentials and a usage allowance are still needed.')
    print('Environment file:',env)
    print('State directory:',state)
    print('ChromeOS must keep Linux running; this does not start Linux after a Chromebook restart.')
    return unit,env,state

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args();install(Path(__file__).resolve().parents[2],Path.home(),args.dry_run)
