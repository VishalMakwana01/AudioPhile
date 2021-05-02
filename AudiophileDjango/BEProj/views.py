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
from pydub import AudioSegment
from scipy.io.wavfile import read
# import pydub

import json



class AudioBook(APIView):

    def post(self, request):

        tacotron2 = torch.hub.load('nvidia/DeepLearningExamples:torchhub', 'nvidia_tacotron2')
        tacotron2 = tacotron2.to('cuda')
        tacotron2.eval()

        melgan = torch.hub.load('seungwonpark/melgan', 'melgan')
        melgan.eval()

        if(request.data and ('text' in request.data)):
            total_content=(request.data['text'])
        else:

            file = request.FILES["ebook"]
            file_name = default_storage.save(file.name, file)

            i = 0
            total_content = ''
            with pdfplumber.open(default_storage.open(file_name)) as pdf:
                while i<len(pdf.pages):
                    page = pdf.pages[i]
                    i+=1
                    total_content += page.extract_text()
            default_storage.delete(file.name)
        total_content = total_content.replace("\n","").split(".")
        total_content = list(filter(None, total_content))

        

        rate = 22050
        _, signal = read("BEProj/audios/1-second-of-silence.wav")
        channel1 = signal[:] 

        pause_segment = AudioSegment(
            channel1.tobytes(), 
            frame_rate=rate,
            sample_width=channel1.dtype.itemsize, 
            channels=1
        )

        combined = pause_segment
        for content in total_content:

            sequence = np.array(tacotron2.text_to_sequence(content, ['english_cleaners']))[None, :]
            sequence = torch.from_numpy(sequence).to(device='cuda', dtype=torch.int64)
            print(sequence)
 

            with torch.no_grad():
                _, mel, _, _ = tacotron2.infer(sequence)

                if torch.cuda.is_available():
                    melgan = melgan.cuda()
                    mel = mel.cuda()

                audio = melgan.inference(mel)
            np_audio = audio.cpu().detach().numpy()

            channel = np_audio[:]

            audio_segment = AudioSegment(
            channel.tobytes(), 
            frame_rate=rate,
            sample_width=channel.dtype.itemsize, 
            channels=1
            )

            combined += audio_segment + pause_segment
            

        combined.export("BEProj/audios/audio.wav", format='wav')

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
