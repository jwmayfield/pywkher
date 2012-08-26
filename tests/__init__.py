from os import path as os_path
from unittest import TestCase

from mock import patch

from pywkher import generate_pdf


class PywkherTestCase(TestCase):
    @patch('pywkher.call_subprocess', return_value=0)
    def test_generate_pdf(self, mock_post):
        pdf_file = generate_pdf('<html><body>Is this thing on?</body></html>')
        self.assertTrue(os_path.exists(pdf_file.name))
