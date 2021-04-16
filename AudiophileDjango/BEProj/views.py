import PyPDF2 as PyPDF2
from rest_framework import status
from rest_framework.response import Response
import os
from django.http import HttpResponse
from rest_framework.views import APIView
import io
import numpy as np
from scipy.io.wavfile import write
import torch
import pdfreader
from pdfreader import PDFDocument
import pdfplumber
from django.core.files.storage import default_storage
from django.http import FileResponse




class AudioBook(APIView):

    def post(self, request):

        file = request.FILES["ebook"]
        file_name = default_storage.save(file.name, file)

        i = 0
        total_content = ''
        with pdfplumber.open(default_storage.open(file_name)) as pdf:
            while i<len(pdf.pages):
            # print("Length = ",len(pdf.pages))
                page = pdf.pages[i]
                i+=1
                total_content += page.extract_text()
        total_content = total_content.replace("\n","").split(".")
        total_content = list(filter(None, total_content))
        total_content = [' ' + s for s in total_content]

        print("Content is here")
        print(total_content)
        audio_list = []


        tacotron2 = torch.hub.load('nvidia/DeepLearningExamples:torchhub', 'nvidia_tacotron2')
        tacotron2 = tacotron2.to('cuda')
        tacotron2.eval()

        melgan = torch.hub.load('seungwonpark/melgan', 'melgan')
        melgan.eval()
        # content = 'My name is Nirav'
        for content in total_content:

            sequence = np.array(tacotron2.text_to_sequence(content, ['english_cleaners']))[None, :]
            sequence = torch.from_numpy(sequence).to(device='cuda', dtype=torch.int64)
            print(sequence)

            with torch.no_grad():
                _, mel, _, _ = tacotron2.infer(sequence)

                if torch.cuda.is_available():
                    melgan = melgan.cuda()
                    mel = mel.cuda()

                # print(mel.shape)
                audio = melgan.inference(mel)

            audio_list.append(audio.cpu().detach().numpy())

        audio = np.concatenate(audio_list)
        rate = 22050

        write("BEProj/audios/audio.wav", rate, audio)

        # audio = open('/home/nirav/Desktop/Workspace/AudioPhile-old/AudiophileDjango/audio.wav', 'rb')

        # response = FileResponse(audio)

        # return response

        # from IPython.display import Audio

        # Audio(audio_numpy, rate=rate)
        return Response({
            'url':"http://127.0.0.1:8000/audio/"
            })

    def get(self, response):
        fname="BEProj/audios/audio.wav"
        f = open(fname,"rb") 
        response = HttpResponse()
        response.write(f.read())
        response['Content-Type'] ='audio/mp3'
        response['Content-Length'] =os.path.getsize(fname )
        return response


