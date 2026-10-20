import unittest

import server

class ServerTests(unittest.TestCase):
    def test_canonicalize_google_wrapper(self):
        data = {'url': 'https://www.google.com/url?url=https%3A%2F%2Fexample.org%2Fp%3Futm_source%3Dalert%26id%3D7',
                'excerpt': 'x', 'need': 'y', 'fit': 'uncertain', 'intent': ''}
        res = server.validate(data)
        self.assertEqual(res['url'], 'https://example.org/p?id=7')

    def test_rejects_credentials(self):
        data = {'url': 'http://user:pass@example.org/', 'excerpt': 'x', 'need': 'y', 'fit': 'uncertain', 'intent': ''}
        with self.assertRaises(ValueError):
            server.validate(data)

    def test_rejects_google_search_page(self):
        data = {'url': 'https://www.google.com/search?q=life+coach', 'excerpt': 'x', 'need': 'y', 'fit': 'uncertain', 'intent': ''}
        with self.assertRaises(ValueError):
            server.validate(data)

if __name__ == '__main__':
    unittest.main()
