"""Scheduled discovery hints -> private Notion queue. No outreach or source scraping.
Python standard library; feed snippets are unverified until Thomas reviews the original.
"""
import hashlib
import html
import ipaddress
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

VERSION = '2025-09-03'
DATA_SOURCE = '372a2ce9-92a9-455f-8826-5f771be0350b'
BLOCKED = ('reddit.com', 'redd.it', 'linkedin.com', 'facebook.com', 'instagram.com')
REQUEST = re.compile(r'\b(?:looking for|seeking|searching for|need(?:ing)?|recommend(?:ations for)?|can anyone recommend)\b.{0,90}\b(?:life coach|personal coach|authenticity coach|spiritual coach|coaching|life coaching)\b', re.I)
GUIDANCE_REQUEST = re.compile(r'\b(?:looking for|seeking|searching for|need(?:ing)?|can anyone recommend)\b.{0,90}\b(?:guidance|a guide|a mentor|mentorship)\b', re.I)
AUDIENCE = re.compile(r'\b(?:spiritual awakening|personal awakening|paranormal|anomalous experience|authenticity|personal growth|life direction|life purpose)\b', re.I)
EXCLUDE = re.compile(r'\b(?:hiring|job opening|coach certification|become a coach|football coach|basketball coach|soccer coach)\b', re.I)
GROWTH = re.compile(r'\b(?:authenticity|genuine|values|purpose|direction|personal growth|life transition)\b', re.I)
PERSONAL = re.compile(r'\b(?:personalized|one.on.one|individual coaching|custom coaching)\b', re.I)

class SetupError(Exception):
    pass

def canonical(url):
    p = urlsplit(html.unescape(url.strip()))
    if p.hostname in ('www.google.com', 'google.com') and p.path == '/url':
        query = parse_qs(p.query)
        return canonical((query.get('url') or query.get('q') or [''])[0])
    if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password:
        raise ValueError('Invalid source URL')
    host = p.hostname.lower()
    if host in ('localhost',) or '.' not in host:
        raise ValueError('Non-public source URL')
    try:
        if not ipaddress.ip_address(host).is_global:
            raise ValueError('Non-public source URL')
    except ValueError as e:
        if str(e) == 'Non-public source URL':
            raise
    try:
        port = p.port
    except ValueError:
        raise ValueError('Invalid port') from None
    netloc = host + (':' + str(port) if port and port not in (80, 443) else '')
    query = [(k, v) for k, values in parse_qs(p.query, keep_blank_values=True).items()
             if not k.lower().startswith('utm_') and k.lower() not in ('fbclid', 'gclid') for v in values]
    return urlunsplit((p.scheme.lower(), netloc, p.path or '/', urlencode(sorted(query)), ''))

def blocked(url):
    host = urlsplit(url).hostname
    return any(host == d or host.endswith('.' + d) for d in BLOCKED)

def clean(text):
    return ' '.join(html.unescape(re.sub(r'<[^>]*>', ' ', text or '')).split())

def date_value(value):
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        try:
            dt = parsedate_to_datetime(value)
        except (ValueError, TypeError, OverflowError):
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()

def parse_feed(raw):
    if len(raw) > 2000000 or b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():
        raise ValueError('Unsupported or oversized feed')
    root = ET.fromstring(raw)
    tag = lambda e: e.tag.rsplit('}', 1)[-1]
    for entry in root.iter():
        if tag(entry) not in ('entry', 'item'):
            continue
        fields = {}
        links = []
        for child in entry:
            key = tag(child)
            if key == 'link':
                if child.attrib.get('rel', 'alternate') == 'alternate':
                    links.append(child.attrib.get('href') or child.text or '')
            else:
                fields[key] = ''.join(child.itertext())
        if not links:
            continue
        try:
            url = canonical(links[0])
        except ValueError:
            continue
        yield {'url': url, 'title': clean(fields.get('title', '')),
               'excerpt': clean(fields.get('content') or fields.get('summary') or fields.get('description', '')),
               'published': date_value(fields.get('published') or fields.get('pubDate'))}
        # Atom 'updated' is not an original publication date; leave publication unknown.

def qualify(item, now=None):
    now = now or datetime.now(timezone.utc)
    text = item['title'] + ' ' + item['excerpt']
    request_found = REQUEST.search(text) or (GUIDANCE_REQUEST.search(text) and AUDIENCE.search(text))
    if blocked(item['url']) or EXCLUDE.search(text) or not request_found:
        return None
    if item['published']:
        age = now - datetime.fromisoformat(item['published'])
        if age > timedelta(days=30) or age < timedelta(days=-1):
            return None
    offer = 'Fits Like a Glove $400' if PERSONAL.search(text) else 'Genuine Self $150' if GROWTH.search(text) else 'Review fit'
    return {**item, 'key': hashlib.sha256(item['url'].encode()).hexdigest(),
            'offer': offer, 'queue': 'Qualification',
            'priority': 2 + int(offer != 'Review fit') + int(bool(item['published'])),
            'reason': 'Request language found in a discovery feed. Verify original author intent, date, adult eligibility, source-use permission, offer fit and reply rules. Payment evidence unknown. Priority is a review order, not purchase probability.'}

def feed_url(url):
    p = urlsplit(url)
    if p.scheme != 'https' or p.hostname != 'www.google.com' or not p.path.startswith('/alerts/feeds/') or p.username or p.password or p.port not in (None, 443):
        raise SetupError('Use an HTTPS Google Alerts feed URL, not a search page or sign-in URL.')
    return url

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise SetupError('Feed redirected. Check the saved feed URL.')

def fetch_feed(url):
    req = urllib.request.Request(feed_url(url), headers={'User-Agent': 'EnergyCultureLeadReview/1.0'})
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=25) as response:
            raw = response.read(2000001)
        return list(parse_feed(raw))
    except (urllib.error.URLError, OSError, ET.ParseError, ValueError):
        # Do not expose private feed URL/token in exceptions or Actions logs.
        raise SetupError('Feed could not be read. Check access and RSS format.') from None

class Notion:
    def __init__(self, token, data_source=DATA_SOURCE):
        if not token:
            raise SetupError('Missing NOTION_LEADS_TOKEN')
        self.token, self.data_source = token, data_source
    def call(self, method, path, data=None):
        req = urllib.request.Request('https://api.notion.com/v1/' + path,
            data=json.dumps(data).encode() if data is not None else None,
            method=method, headers={'Authorization': 'Bearer ' + self.token,
            'Notion-Version': VERSION, 'Content-Type': 'application/json'})
        # POST create is not blindly retried: an uncertain response is resolved by dedup next run.
        for attempt in range(3):
            time.sleep(0.4)
            try:
                with urllib.request.urlopen(req, timeout=25) as res:
                    return json.load(res)
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < 2:
                    time.sleep(min(float(e.headers.get('Retry-After', '2')), 10))
                    continue
                raise SetupError('Notion request failed (HTTP %s). Check connection access and schema.' % e.code) from None
            except (urllib.error.URLError, OSError):
                raise SetupError('Notion connection failed; retry the run after checking access.') from None
        raise SetupError('Notion rate limit')
    def validate(self):
        schema = self.call('GET', 'data_sources/' + self.data_source)['properties']
        expected = {'Name':'title','Source Link':'url','Evidence':'rich_text','Source':'rich_text',
                    'Key':'rich_text','Observed':'date','Published':'date','Offer':'select',
                    'Queue':'select','Status':'select','Priority':'number','Reason':'rich_text',
                    'Payment Evidence':'rich_text','Contact Permission':'rich_text','Suppressed':'checkbox'}
        if any(schema.get(k, {}).get('type') != v for k,v in expected.items()):
            raise SetupError('Notion queue schema changed. Restore required properties before collecting.')
    def exists(self, key):
        rows = self.call('POST', 'data_sources/' + self.data_source + '/query',
            {'page_size': 1, 'filter': {'property':'Key','rich_text':{'equals':key}}})
        return bool(rows['results'])
    def save(self, item):
        if self.exists(item['key']):
            return False  # Never overwrite suppression, review decisions or outcomes.
        rt = lambda value: [{'type':'text','text':{'content':str(value)[:1900]}}]
        props = {'Name':{'title':rt(item['title'][:180] or 'Coaching request — review')},
            'Source Link':{'url':item['url']},'Evidence':{'rich_text':rt('Discovery snippet (unverified): ' + ' '.join(item['excerpt'].split()[:50]))},
            'Source':{'rich_text':rt('Google Alerts discovery feed; original source requires review')},
            'Observed':{'date':{'start':datetime.now(timezone.utc).isoformat()}},
            'Offer':{'select':{'name':item['offer']}},'Queue':{'select':{'name':'Qualification'}},
            'Status':{'select':{'name':'New'}},'Priority':{'number':item['priority']},
            'Reason':{'rich_text':rt(item['reason'])}, 'Payment Evidence':{'rich_text':rt('Unknown')},
            'Contact Permission':{'rich_text':rt('Unknown — original source and community rules require review')},
            'Suppressed':{'checkbox':False},'Key':{'rich_text':rt(item['key'])}}
        if item['published']:
            props['Published'] = {'date':{'start':item['published']}}
        self.call('POST','pages',{'parent':{'type':'data_source_id','data_source_id':self.data_source},'properties':props})
        return True

def collect(feed_urls, sink):
    sink.validate()  # Fail before collecting if private storage is unavailable.
    seen, counts = set(), {'feeds':0,'candidates':0,'saved':0,'duplicates':0,'skipped':0}
    for url in feed_urls:
        entries = fetch_feed(url)
        counts['feeds'] += 1
        for entry in entries[:100]:
            item = qualify(entry)
            if not item:
                counts['skipped'] += 1
                continue
            counts['candidates'] += 1
            if item['key'] in seen:
                counts['duplicates'] += 1
                continue
            seen.add(item['key'])
            if sink.save(item):
                counts['saved'] += 1
            else:
                counts['duplicates'] += 1
    return counts

def main():
    urls = [s.strip() for s in os.environ.get('LEAD_ALERT_FEEDS','').splitlines() if s.strip()]
    if not urls:
        raise SetupError('Missing LEAD_ALERT_FEEDS — add at least one Google Alerts RSS feed.')
    if len(urls) > 5:
        raise SetupError('Maximum five feeds for the pilot')
    for url in urls:
        feed_url(url)
    counts = collect(urls, Notion(os.environ.get('NOTION_LEADS_TOKEN',''), os.environ.get('NOTION_LEADS_DATA_SOURCE',DATA_SOURCE)))
    print(json.dumps({'status':'completed', **counts}))  # Counts only; no identities or excerpts in logs.

if __name__ == '__main__':
    try:
        main()
    except SetupError as e:
        print('SETUP BLOCKED: ' + str(e), file=sys.stderr)
        sys.exit(2)
    except Exception:
        print('Collection failed. No lead details logged; inspect configuration and rerun.', file=sys.stderr)
        sys.exit(1)
