import PyPDF2 as PyPDF2
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import io

class AudioBook(APIView):

    def post(self, request):

        file = request.FILES.get("ebook", None)
        pdfFileObj = file.read()
        pdfReader = PyPDF2.PdfFileReader(io.BytesIO(pdfFileObj))
        pages = pdfReader.numPages

        i=0
        content = ""
        while (i<pages):
            text = pdfReader.getPage(i)
            content += text.extractText()
            i +=1
        print(content)
        #text to audio

        return Response()