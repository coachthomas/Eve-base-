import importlib.util,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('worker',Path(__file__).parents[1]/'worker.py')
w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w)
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name)/'repo';self.state=Path(self.tmp.name)/'state'
  (self.root/'apps/lead-discovery/tests').mkdir(parents=True)
  self.file=self.root/'apps/lead-discovery/example.py';self.file.write_text('VALUE=1\n')
  (self.root/'apps/lead-discovery/tests/test_example.py').write_text('import unittest\nclass T(unittest.TestCase):\n def test_ok(self): self.assertTrue(True)\n')
  self.worker=w.Worker(self.root,self.state,lambda _:self.step(),daily_calls=4)
 def step(self,state='complete',writes=None):return dict(state=state,summary='fixture only',reason='',writes=writes or [])
 def test_dedup_restart_recovery(self):
  s=self.worker.store;s.enqueue('one','first');s.enqueue('one','duplicate');other=w.Store(self.state/'queue.sqlite3')
  self.assertEqual(other.claim()['prompt'],'first');self.assertIsNone(other.claim());other.recover();self.assertEqual(other.claim()['id'],'one')
 def test_persistent_call_cap(self):
  self.worker.store.reserve_call(1)
  with self.assertRaises(w.Blocked):w.Store(self.state/'queue.sqlite3').reserve_call(1)
 def test_no_calls_without_allowance(self):
  self.worker.daily_calls=0;calls=[];self.worker.api=lambda p:calls.append(p);self.worker.store.enqueue('one','test');self.worker.tick()
  self.assertEqual(calls,[]);self.assertEqual(self.worker.store.status()['jobs'][0]['status'],'blocked')
 def test_paths(self):
  for p in ['../x','/tmp/x','ops/continuous-worker/worker.py','apps/lead-discovery/.env.local','apps/lead-discovery/secret.json']:
   with self.subTest(p=p),self.assertRaises(w.Blocked):self.worker.target(p)
 def test_symlink(self):
  (self.root/'apps/lead-discovery/link.py').symlink_to('/tmp/outside')
  with self.assertRaises(w.Blocked):self.worker.target('apps/lead-discovery/link.py')
 def test_failed_checks_rollback(self):
  step=self.step(writes=[dict(path='apps/lead-discovery/example.py',content='changed'),dict(path='apps/lead-discovery/new.py',content='x=1')])
  with patch.object(self.worker,'verify',return_value=dict(ok=False,output='failure')):self.worker.apply('one',step)
  self.assertEqual(self.file.read_text(),'VALUE=1\n');self.assertFalse((self.file.parent/'new.py').exists())
 def test_crash_recovery(self):
  (self.state/'pending.json').write_text(json.dumps([dict(path='apps/lead-discovery/example.py',content='old')]))
  self.worker.rollback();self.assertEqual(self.file.read_text(),'old')
 def test_continues_without_new_prompt(self):
  calls=[]
  def api(prompt):
   calls.append(prompt);return self.step('complete' if len(calls)==2 else 'continue',[dict(path='apps/lead-discovery/example.py',content='VALUE='+str(len(calls)))])
  self.worker.api=api;self.worker.store.enqueue('one','fixture job');self.worker.tick()
  self.assertEqual(self.worker.store.status()['jobs'][0]['status'],'queued');self.worker.tick()
  self.assertEqual(self.worker.store.status()['jobs'][0]['status'],'done');self.assertEqual(len(calls),2);self.assertIn('checkpoint',calls[1])
 def test_three_failures_block(self):
  self.worker.api=lambda _:(_ for _ in ()).throw(TimeoutError());self.worker.store.enqueue('one','fixture')
  for _ in range(3):self.worker.tick();self.worker.store.update('one',due=0)
  self.assertEqual(self.worker.store.status()['jobs'][0]['status'],'blocked')
 def test_pause(self):
  self.worker.store.enqueue('one','test');(self.state/'PAUSE').touch();self.assertFalse(self.worker.tick())
  self.assertEqual(self.worker.store.status()['jobs'][0]['status'],'queued')
 def test_exclusive_lock(self):
  with self.worker.lock():
   with self.assertRaises(BlockingIOError):
    with self.worker.lock():pass
 def test_round_cap(self):
  self.worker.store.enqueue('one','test');self.worker.store.update('one',rounds=12);self.worker.tick()
  self.assertEqual(self.worker.store.status()['jobs'][0]['status'],'blocked')
 def test_test_process_has_no_secret(self):
  with patch('subprocess.run') as run:
   run.return_value.returncode=0;run.return_value.stdout='';run.return_value.stderr='';self.worker.verify()
   self.assertNotIn('OPENAI_API_KEY',run.call_args.kwargs['env'])
 def test_validate_before_writes(self):
  with self.assertRaises(w.Blocked):self.worker.apply('one',self.step(writes=[dict(path='apps/lead-discovery/example.py',content='changed'),dict(path='../escape',content='bad')]))
  self.assertEqual(self.file.read_text(),'VALUE=1\n')
if __name__=='__main__':unittest.main()
