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
import pdfplumber
from django.core.files.storage import default_storage
from django.http import FileResponse
import json



class AudioBook(APIView):

    def post(self, request):
        print(request.data)
        tacotron2 = torch.hub.load('nvidia/DeepLearningExamples:torchhub', 'nvidia_tacotron2')
        tacotron2 = tacotron2.to('cuda')
        tacotron2.eval()

        melgan = torch.hub.load('seungwonpark/melgan', 'melgan')
        melgan.eval()
        if(request.data and ('text' in request.data)):
            content=(request.data['text'])
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
            audio=audio.cpu().detach().numpy()
            
            rate = 22050

            write("BEProj/audios/audio.wav", rate, audio)
            return Response({
            'url':"http://127.0.0.1:8000/audio/"
            })
        else:
            print('Ebook')
            file = request.FILES["ebook"]
            file_name = default_storage.save(file.name, file)

            i = 0
            total_content = ''
            with pdfplumber.open(default_storage.open(file_name)) as pdf:
                while i<len(pdf.pages):
                # print("Length = ",len(pdf.pages))
                    page = pdf.pages[i]
                    i+=1
                    total_content += (" "+ page.extract_text())
                    print(total_content)
            total_content = total_content.split(".")
            total_content = list(filter(None, total_content))
            total_content = [". "+s for s in total_content]
            #total_content=". ".join(total_content)
            print("Content is here")
            print(total_content)
            audio_list = []
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
                    #audio_list.append(np.zeros(50000))
            
            audio = np.concatenate(audio_list)
            rate = 22050

            write("BEProj/audios/audio.wav", rate, audio)

            # audio = open('/home/nirav/Desktop/Workspace/AudioPhile-old/AudiophileDjango/audio.wav', 'rb')

            # response = FileResponse(audio)

            # return response

            # from IPython.display import Audio

            # Audio(audio_numpy, rate=rate)'''
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