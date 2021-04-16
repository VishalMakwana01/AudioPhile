import PyPDF2 as PyPDF2
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import io
import numpy as np
from scipy.io.wavfile import write
import torch


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

        tacotron2 = torch.hub.load('nvidia/DeepLearningExamples:torchhub', 'nvidia_tacotron2')
        tacotron2 = tacotron2.to('cuda')
        tacotron2.eval()

        melgan = torch.hub.load('seungwonpark/melgan', 'melgan')
        melgan.eval()

        sequence = np.array(tacotron2.text_to_sequence(content, ['english_cleaners']))[None, :]
        sequence = torch.from_numpy(sequence).to(device='cuda', dtype=torch.int64)

        with torch.no_grad():
            _, mel, _, _ = tacotron2.infer(sequence)

            if torch.cuda.is_available():
                melgan = melgan.cuda()
                mel = mel.cuda()

            # print(mel.shape)
            audio = melgan.inference(mel)

        audio_numpy = audio.cpu().detach().numpy()
        rate = 22050

        write("audio.wav", rate, audio_numpy)

        from IPython.display import Audio
        Audio(audio_numpy, rate=rate)

        return Response()