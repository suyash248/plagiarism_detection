__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import unittest
from service.plag_dao import PlagiarismDAO
from service.plag_detector import PlagiarismDetector
from sqlalchemy.exc import SQLAlchemyError
from util.injector import inject
import json
import requests
from uuid import uuid4

class TestPlagiarismDetection(unittest.TestCase):

    def setUp(self):
        self.plag_dao: PlagiarismDAO = inject(PlagiarismDAO)
        self.plag_detector: PlagiarismDetector = inject(PlagiarismDetector)
        self.host = 'http://0.0.0.0:5000'

    def test_1_validate_doc_title(self):
        url = '{}{}'.format(self.host, '/api/v1/plagiarism/documents')
        response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps({}))
        self.assertEqual(response.status_code, 400, msg='title and content are required!')

        url = '{}{}'.format(self.host, '/api/v1/plagiarism/documents')
        payload = {
            'title': str(uuid4()) * 6,
            'author': str(uuid4()) * 6,
            'content': str(uuid4()),
            'description': str(uuid4())

        }
        response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        self.assertRaises(SQLAlchemyError)

    def test_2_add_doc(self):
        url = '{}{}'.format(self.host, '/api/v1/plagiarism/documents')
        payload = {
            'title': 'test_title_{}'.format(str(uuid4())),
            'author': 'test_author_{}'.format(str(uuid4())),
            'content': 'test_content_{}'.format(str(uuid4())),
            'description': 'test_description_{}'.format(str(uuid4())),

        }
        response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        self.assertIn(response.status_code, (200, 201), msg='Document added successfully!')

    def test_3_different_docs(self):
        sim_score = self.plag_detector.cosine_similarity('test', 'check')
        self.assertEqual(sim_score, 0, msg='These 2 strings are completely different.')

    def test_4_identical_docs(self):
        sim_score = self.plag_detector.cosine_similarity('test', 'test')
        self.assertEqual(sim_score, 1.0, msg='These 2 strings are identical.')

    def test_5_similar_docs(self):
        sim_score = self.plag_detector.cosine_similarity('bird parrot', 'cockatiel bird')
        self.assertGreater(sim_score, 0, msg='These 2 strings are similar with similarity score of {}.'.format(sim_score))

if __name__ == '__main__':
    unittest.main()
    # python -m unittest discover -s 'tests' -p '*.py'