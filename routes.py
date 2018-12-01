__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from controller import plag_detection

def add_prefix(uri):
    return "{}{}".format('/api/v1', uri)

def register_urls(api):
    """
    Maps all the endpoints with controllers.
    """

    api.add_resource(plag_detection.PlagiarismDetection, add_prefix('/detect-plagiarism'))


