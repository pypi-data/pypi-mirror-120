import os
import shutil
from typing import Dict, Union
import json


class ScriptDirRunnerJob:
    def __init__(self, directory):
        import kachery_client as kc
        self._directory = directory
        self._status = ''
        self._script: Union[None, kc.ShellScript] = None
        self._set_status('pending')

    @property
    def status(self):
        return self._status

    def start(self):
        import kachery_client as kc
        assert self._status == 'pending'
        source_env_str = 'source ./env' if os.path.isfile(f'{self._directory}/env') else ''
        self._script = kc.ShellScript(f'''
        #!/bin/bash

        set -e

        # if the run file disappears we will end the process
        export HITHER_RUNNING_FILE="{self._directory}/run"

        cd {self._directory}
        {source_env_str}
        exec ./run
        ''')
        self._set_status('running')
        self._script.start()

    def iterate(self):
        if self._status == 'running':
            retcode = self._script.wait(0)
            if retcode is not None:
                self._retcode = retcode
                if retcode == 0:
                    self._set_status('complete')
                else:
                    print(f'WARNING: Unexpected return code in ScriptDirRunnerJob: {retcode}')
                    self._set_status('complete')
            if not os.path.isdir(self._directory):
                print(f'Stopping scriptdir script because directory does not exist: {self._directory}')
                self._script.stop()

    def _set_status(self, status):
        if self._status == status:
            return
        with open(f'{self._directory}/status', 'w') as f:
            f.write(status)
        self._status = status


class ScriptDirRunner:
    def __init__(self, directory: str):
        import yaml
        self._directory = directory
        self._jobs: Dict[str, ScriptDirRunnerJob] = {}
        config_path = f'{directory}/config.yaml'
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

    def iterate(self):
        jobs_path = f'{self._directory}/jobs'
        if not os.path.isdir(jobs_path):
            os.mkdir(jobs_path)
        fnames = os.listdir(jobs_path)
        for fname in fnames:
            job_path = f'{jobs_path}/{fname}'
            if os.path.isdir(job_path):
                job_id = fname
                if job_id not in self._jobs:
                    if os.path.isfile(f'{job_path}/run') and (not os.path.isfile(f'{job_path}/status')):
                        self._jobs[job_id] = ScriptDirRunnerJob(job_path)
        job_ids = list(self._jobs.keys())
        for job_id in job_ids:
            job = self._jobs[job_id]
            if job.status == 'pending':
                job.start()
            elif job.status == 'running':
                job.iterate()
        self._write_state()

    def _write_state(self):
        state = {
            'job_counts': {
                'pending': 0,
                'running': 0,
                'complete': 0
            },
            'jobs': {}
        }
        job_ids = list(self._jobs.keys())
        for job_id in job_ids:
            job = self._jobs[job_id]
            state['job_counts'][job.status] += 1
            state['jobs'][job_id] = {
                'status': job.status
            }
        txt = json.dumps(state, indent=4)
        state_path = f'{self._directory}/state.json'
        _write_text_file_if_changed(state_path, txt)

def _write_text_file_if_changed(path: str, txt: str):
    if os.path.isfile(path):
        with open(path, 'r') as f:
            txt_existing = f.read()
            if txt_existing == txt:
                return
    with open(path + '.writing', 'w') as f:
        f.write(txt)
    shutil.move(path + '.writing', path)
