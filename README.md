# Ultrawide Conversor

Ultrawide Conversor trata-se de um script Pyhton para converter um lote de vídeos de proporção 21:9 para 16:9.

## Requisitos

* [Python 3](https://www.python.org/downloads/)
* [FFmpeg](https://ffmpeg.org)

## Utilização

Para utilizar, basta mover o script para a pasta onde estão os vídeos. Após executar o script, será criado um arquivo compactado com todos os vídeos convertidos. O script irá varrer todos os subdiretórios da pasta onde está, e irá compactar respitando essa hierarquia.

## Observações

* Vídeos que não sejam de proporção 21:9 não serão convertidos e nem compactados.
* Apenas vídeos de extensão **.mp4** serão convertidas.
