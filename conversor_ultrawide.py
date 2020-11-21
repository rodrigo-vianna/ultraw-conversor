from zipfile import ZipFile
from datetime import datetime
import os
import ffmpeg
import shutil
import json

# Data atual do sistema
date_time = datetime.now().strftime("%d%m%Y_%H%M%S")

# Nome do arquivo zip que será criado
DIR_ZIP = os.path.normpath('./videos'+date_time+'.zip')
# Diretório onde está sendo executado o script que servirá de base para pegar os vídeos
DIR_ORIGEM = os.path.normpath('./')
# Diretório temporário
DIR_TMP = os.path.normpath('./tmp')

# Proporção 16:9
PROP_REF = 1.777777777777778

# Metadados dos videos
# probe = ffmpeg.probe("./GeForceExperience/Valorant/rinha-de-faca.mp4")
# video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
# info = json.dumps(video_streams[0], indent=4)
# print(info)

def apagarDiretorioTemporario():
    """
    Apaga o direótio temporário, caso ele exista
    """
    if os.path.exists(DIR_TMP):
        shutil.rmtree(DIR_TMP)


def converter():
    """
    Cria o arquivo ZIP e realiza a conversão dos vídeos. Faz a conversão do vídeo para o arquivo temporário, adiciona
    no arquivo ZIP, apaga do diretório temporário e realiza essa iteração com todos os vídeos no diretório onde se encontra
    o script e seus subdiretórios.
    Apenas realiza a conversão e compactação de vídeo que sejam no formato 21:9
    """
    with ZipFile(DIR_ZIP, 'w') as zip:
        for path, subdirs, files in os.walk(DIR_ORIGEM):
            destPath = os.path.normcase(os.path.join(
                DIR_TMP, *(path.split(os.path.sep)[1:])))
            if not os.path.exists(destPath):
                os.makedirs(destPath)

            for name in files:
                arquivo = os.path.join(path, name)
                if os.path.isdir(arquivo) or not arquivo.endswith('.mp4'):
                    continue

                probe = ffmpeg.probe(arquivo)
                video_streams = [
                    stream for stream in probe["streams"] if stream["codec_type"] == "video"]

                widthOriginal = video_streams[0]['width']
                height = video_streams[0]['height']

                proporcao = widthOriginal / video_streams[0]['height']
                proporcao = float('%.3f' % (proporcao))
                if proporcao < 2.370:
                    continue

                width = int(PROP_REF*height)
                posX = (widthOriginal-width)/2

                file = os.path.normpath(os.path.join(
                    destPath, os.path.basename(arquivo)))
                input = ffmpeg.input(arquivo)
                video = input.video.crop(posX, 0, width, height)
                ffmpeg.output(input.audio, video, file).run()

                zip.write(file, os.path.normcase(arquivo.replace(DIR_TMP, "")))

                os.remove(file)


def main():
    """
    Função principal
    """
    # Se já existir um diretório temporário, o deleta
    apagarDiretorioTemporario()

    # Cria um diretório temporário
    os.makedirs(DIR_TMP)

    # Converte os arquivos
    converter()

    # Deleta o diretório temporário
    apagarDiretorioTemporario()


if __name__ == "__main__":
    main()
