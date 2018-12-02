__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from flask import request
from util.response import intercept, Response
from controller.base import BaseController
from util.injector import inject
from service.plag_dao import PlagiarismDAO
from util.constants.error_codes import HttpErrorCode
from util.error_handlers.exceptions import ExceptionBuilder, BadRequest

class Document(BaseController):
    plag_dao: PlagiarismDAO = inject(PlagiarismDAO)

    @intercept()
    def post(self, *args, **kwargs):
        """Adds a new document to repo"""

        data = request.get_json(force=True)

        content = data.get('content', '')
        title = data.get('title', '')
        description = data.get('description', '')
        author = data.get('author', '')

        if content and title:
            doc = self.plag_dao.create_doc(content, title, description=description, author=author)
        else:
            ExceptionBuilder(BadRequest).error(HttpErrorCode.REQUIRED_FIELD, 'content', 'title').throw()

        return Response(status_code=201, message='Document added successfully!')

    @intercept()
    def get(self):
        """
        Fetches all the documents(paginated).
        :return:
        """
        res = self.plag_dao.get_docs(page=int(request.args.get("page", 1)),
                                    per_page=int(request.args.get("per_page", 10)), all='all' in request.args)
        docs_info = dict(data=[d.to_dict() for d in res['data']], count=res['count'])
        print(docs_info)
        return Response(data=docs_info)
