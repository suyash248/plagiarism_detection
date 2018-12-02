__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from flask import request
from util.response import intercept, Response
from controller.base import BaseController
from util.injector import inject
from service.plag_detector import PlagiarismDetector
from typing import Dict
from util.constants.error_codes import HttpErrorCode
from util.error_handlers.exceptions import ExceptionBuilder, BadRequest

class PlagiarismDetection(BaseController):
    plag_detector: PlagiarismDetector = inject(PlagiarismDetector)

    @intercept()
    def post(self, *args, **kwargs):
        """Detects plagiarism"""

        data = request.get_json(force=True)
        input_doc = data.get('text', None)
        if input_doc is None:
            ExceptionBuilder(BadRequest).error(HttpErrorCode.REQUIRED_FIELD, 'text').throw()
        most_similar_doc_info: Dict = self.plag_detector.compute_similarity(input_doc)

        most_similar_doc = most_similar_doc_info['doc']
        similarity_score = most_similar_doc_info['similarity_score']
        similarity_percentage = round(similarity_score * 100, 2)

        message = "Input text is {}% similar to the doc `{}` with similarity score of {}".format(
            similarity_percentage, most_similar_doc.title, similarity_score
        )

        res_data = {
            'similarity_score': similarity_score,
            'similarity_percentage': similarity_percentage,
            'doc': most_similar_doc.to_dict()
        }

        return Response(status_code=200, message=message, data=res_data)
