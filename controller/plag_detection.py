__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from flask import request
from util.response import intercept, Response
from controller.base import BaseController
from util.injector import inject
from service.plag_dao import PlagiarismDAO
from service.plag_detector import PlagiarismDetector

class PlagiarismDetection(BaseController):
    plag_dao = inject(PlagiarismDAO)
    plag_detector = inject(PlagiarismDetector)
