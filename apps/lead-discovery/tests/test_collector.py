import unittest
from datetime import datetime, timezone
from unittest.mock import patch
import collector

class CollectorTests(unittest.TestCase):
    def item(self, text='I am looking for a life coach to clarify my values', url='https://example.org/request'):
        return dict(title=text,excerpt='',url=url,published=None)
    def test_google_wrapper_and_tracking_dedup(self):
        self.assertEqual(collector.canonical('https://www.google.com/url?url=https%3A%2F%2Fexample.org%2Fp%3Futm_source%3Dalert%26id%3D7'), 'https://example.org/p?id=7')
    def test_no_assumed_payment_or_contact(self):
        item=collector.qualify(self.item('Looking for a life coach, budget $200, need authenticity'))
        self.assertEqual(item['queue'],'Qualification')
        self.assertEqual(item['offer'],'Genuine Self $150')
    def test_marketing_and_restricted_sources(self):
        self.assertIsNone(collector.qualify(self.item('Become a coach: looking for life coaching clients')))
        self.assertIsNone(collector.qualify(self.item(url='https://www.reddit.com/r/test/1')))
    def test_dates_not_fabricated(self):
        raw=b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Looking for a life coach</title><link href="https://example.org/p"/><updated>2026-10-06T12:00:00Z</updated><summary>test fixture only</summary></entry></feed>'
        self.assertIsNone(list(collector.parse_feed(raw))[0]['published'])
    def test_old_posts_skipped(self):
        item=self.item();item['published']='2025-01-01T00:00:00+00:00'
        self.assertIsNone(collector.qualify(item, datetime(2026,10,6,tzinfo=timezone.utc)))
    def test_unsafe_feeds(self):
        for url in ['http://127.0.0.1/x','https://evil.org/feed','https://www.google.com/search?q=coach']:
            with self.assertRaises(collector.SetupError): collector.feed_url(url)
        with self.assertRaises(ValueError): list(collector.parse_feed(b'<!DOCTYPE feed><feed/>'))
    def test_idempotent_collections(self):
        class Sink:
            def __init__(self): self.keys=set();self.validated=False
            def validate(self): self.validated=True
            def save(self,item):
                if item['key'] in self.keys:return False
                self.keys.add(item['key']);return True
        sink=Sink()
        with patch('collector.fetch_feed',return_value=[self.item(),self.item()]):
            first=collector.collect(['fixture'],sink)
            second=collector.collect(['fixture'],sink)
        self.assertTrue(sink.validated)
        self.assertEqual(first['saved'],1);self.assertEqual(second['saved'],0)
    def test_notion_payload_and_review_preservation(self):
        sink=collector.Notion('fixture-not-a-token')
        calls=[]
        def fake(method,path,data=None):
            calls.append((method,path,data))
            if path.endswith('/query'): return {'results':[]}
            return {'id':'fixture'}
        sink.call=fake
        self.assertTrue(sink.save(collector.qualify(self.item())))
        props=calls[-1][2]['properties']
        self.assertEqual(props['Queue']['select']['name'],'Qualification')
        self.assertEqual(props['Payment Evidence']['rich_text'][0]['text']['content'],'Unknown')
        sink.call=lambda *a,**k:{'results':[{'id':'existing-suppressed'}]}
        self.assertFalse(sink.save(collector.qualify(self.item())))

if __name__=='__main__': unittest.main()
