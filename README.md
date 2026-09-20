[![Discord](https://img.shields.io/discord/1048892118732656731?logo=discord)](https://discord.gg/Jm5ZttZT)
![Status](https://img.shields.io/badge/status-development-yellow)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/rakuri255/UltraSinger/main.yml)
[![GitHub](https://img.shields.io/github/license/rakuri255/UltraSinger)](https://github.com/rakuri255/UltraSinger/blob/main/LICENSE)
[![CodeFactor](https://www.codefactor.io/repository/github/rakuri255/ultrasinger/badge)](https://www.codefactor.io/repository/github/rakuri255/ultrasinger)

[![Check Requirements](https://github.com/rakuri255/UltraSinger/actions/workflows/main.yml/badge.svg)](https://github.com/rakuri255/UltraSinger/actions/workflows/main.yml)
[![Pytest](https://github.com/rakuri255/UltraSinger/actions/workflows/pytest.yml/badge.svg)](https://github.com/rakuri255/UltraSinger/actions/workflows/pytest.yml)
[![docker](https://github.com/rakuri255/UltraSinger/actions/workflows/docker.yml/badge.svg)](https://hub.docker.com/r/rakuri255/ultrasinger)

<p align="center" dir="auto">
<img src="https://repository-images.githubusercontent.com/594208922/4befe3da-a448-4cbc-b6ef-93899119071b" style="height: 300px;width: auto;" alt="UltraSinger Logo">
</p>

# UltraSinger (DarkKaraoke edition)

> ⚠️ _Este projeto parmanece em desenvolvimento!_

_Este é um fork do projeto UltraSinger que traduz a interface do projeto para português do Brasil e adiciona playback de karaoke, transposição opcional e geração de lyrics videos._

UltraSinger é uma ferramenta que cria automaticamente arquivos UltraStar.txt, MIDI e partituras a partir de uma música.
Ele transcreve a letra, detecta as notas e gera um playback de karaoke sem a voz original do artista.
Quando solicitado, também cria uma segunda versão transposta da música.
Ele também pode relançar os arquivos UltraStar atuais e calcular a possível pontuação no jogo.

Vários modelos de IA são usados para extrair texto da voz e determinar o tom.

Por favor, mencione o UltraSinger em seu arquivo UltraStar.txt se você usá-lo. Isso ajuda outras pessoas a encontrar essa ferramenta e ajuda essa ferramenta a ser aprimorada e mantida. Você só deve usá-lo em músicas licenciadas pela Creative Commons.

## ❤️ Créditos e projeto original
Este fork parte do trabalho original do UltraSinger, criado por
[Rakuri](https://github.com/rakuri255). A ideia, a arquitetura inicial e a maior
parte do processamento de áudio pertencem ao projeto original.

Para conhecer, apoiar ou contribuir com o projeto inicial, acesse o
[repositório original do UltraSinger](https://github.com/rakuri255/UltraSinger).

## Índice

- [UltraSinger](#ultrasinger)
  - [❤️ Créditos e projeto original](#️-créditos-e-projeto-original)
  - [Índice](#índice)
  - [💻 Como usar o código-fonte](#-como-usar-o-código-fonte)
    - [Instalação](#instalação)
    - [Execução](#execução)
  - [📖 Como usar o aplicativo](#-como-usar-o-aplicativo)
    - [🎶 Entrada](#-entrada)
      - [Áudio (modo automático)](#áudio-modo-automático)
        - [Arquivo local](#arquivo-local)
        - [YouTube](#youtube)
      - [UltraStar (regerar)](#ultrastar-regerar)
    - [🗣 Transcrição](#-transcrição)
      - [Whisper](#whisper)
        - [Idiomas do Whisper](#idiomas-do-whisper)
      - [✍️ Hifenização](#️-hifenização)
    - [👂 Detecção de notas](#-detecção-de-notas)
    - [👄 Separação de áudio](#-separação-de-áudio)
    - [🎼 Partitura](#-partitura)
    - [🎵 Transposição](#-transposição)
    - [🎬 Lyrics video](#-lyrics-video)
    - [Versão do formato](#versão-do-formato)
    - [🏆 Cálculo de pontuação do UltraStar](#-cálculo-de-pontuação-do-ultrastar)
    - [📟 Uso da GPU](#-uso-da-gpu)
      - [Considerações para usuários do Windows](#considerações-para-usuários-do-windows)
      - [Informações](#informações)
      - [Uso com Docker](#uso-com-docker)

## 💻 Como usar o código-fonte

### Instalação

* Instale o Python 3.10, 3.11 ou 3.12. [Download](https://www.python.org/downloads/)
* Instale também ffmpeg separadamente com registro no PATH. [Download](https://www.ffmpeg.org/download.html)
* Vá para a pasta `install` e execute o script de sistalação de acordo com o Sistema Operacional.
  * Escolha `GPU` se possui uma GPU nvidia CUDA.
  * Escolha `CPU` se não possui uma GPU nvidia CUDA.

### Execução

* Na pasta raiz execute `run_on_windows.bat` ou `run_on_linux.sh` para iniciar o aplicativo.
* Agora você pode usar o arquivo-fonte do UltraSinger com `py UltraSinger.py [opções] [modo] [transcrição] [detecção de notas] [extra]`. Consulte [Como usar o aplicativo](#-como-usar-o-aplicativo) para mais informações.

## 📖 Como usar o aplicativo

_Algumas funções ainda estão em desenvolvimento._
```commandline
 UltraSinger.py [opcoes] [modo] [transcrição] [pitcher] [extra]
    
    [opcoes]
    -h      Exibe este texto de ajuda.
    -i      Dado de entrada.
            Ex.: arquivo UltraStar.txt, áudio .mp3/.wav ou link do YouTube.
    -o      Pasta de saída.
    
    [modo]
    ## O DADO DE ENTRADA É ÁUDIO ##
    padrão   Cria todos os arquivos.
    
    # Criação de arquivo único em desenvolvimento; atualmente o fluxo completo é executado.
    (-u      Criar arquivo TXT para o UltraStar)
    (-m      Criar arquivo MIDI)
    (-s      Criar partitura)
    
    ## O DADO DE ENTRADA É ULTRASTAR.TXT ##
    padrão   Reprocessa o arquivo e o áudio associado.

    (-r      Regerar UltraStar.txt (a entrada precisa ser um arquivo de áudio))
    (-p      Verificar as notas do UltraStar.txt fornecido)
    (-m      Criar arquivo MIDI)

    [transcrição]
    # O transcritor padrão é o Whisper.
    --whisper               Modelo multilíngue: tiny|base|small|medium|large-v1|large-v2
                            Modelo somente em inglês: tiny.en|base.en|small.en|medium.en
    --whisper_align_model   Usar outro modelo de idioma do Hugging Face.
    --language              Forçar o idioma usado nas etapas posteriores.
    --whisper_batch_size    Reduzir se houver pouca memória de GPU (padrão: 16).
    --whisper_compute_type  Usar "int8" em máquinas com pouca memória (padrão: float16 em CUDA, int8 em CPU).
    
    [pitcher]
    # O detector de notas padrão é o CREPE.
    --crepe            tiny|full (padrão: full)
    --crepe_step_size  Intervalo em milissegundos (padrão: 10)
    
    [extra]
    --hyphenation           (hifenização) True|False >> ((padrão) é True)
    --disable_separation    (desabilitar separação) True|False >> ((padrão) é False)
    --disable_karaoke       (desabilitar versão karaoke) True|False >> ((padrão) é False)
    --create_audio_chunks   (criar partes de áudio) True|False >> ((padrão) é False)
    --keep_cache            (manter cache) True|False >> ((padrão) é False)
    --plot                  (plotar) True|False >> ((padrão) é False)
    --format_version        (versão do formato UltraStar) 0.3.0|1.0.0|1.1.0 >> ((padrão) é 1.0.0)
    --musescore_path        local do executável MuseScore
    --changetone N          Gera uma versão adicional transposta em N semitons.
                            A bateria permanece original; baixo e outros instrumentos são transpostos.
    --create-lyrics-video   Gera um vídeo MP4 com legendas ASS sincronizadas pelas notas UltraStar.
    --video-background      Imagem ou vídeo opcional para o fundo do lyrics video.
    
    [dispositivo]
    --force_cpu             True|False >> ((padrão) é False)  Forçar todo o processamento por cpu
    --force_whisper_cpu     True|False >> ((padrão) é False)  Forçar somente processamento do Whisper por cpu
    --force_crepe_cpu       True|False >> ((padrão) é False)  Forçar somente processamento do crepe por cpu

```

Para o uso normal, basta usar os argumentos de [opcoes]. Os demais parâmetros são opcionais.

Quando `--changetone` é usado, o UltraSinger mantém a versão original e cria uma segunda
mixagem, arquivo UltraStar e áudio com o sufixo `[+N semitones]` (ou `[-N semitones]`).
O Demucs usa quatro fontes nesse modo (`vocals`, `drums`, `bass`, `other`): apenas `bass`
e `other` recebem pitch shift. `--create-lyrics-video` pode ser combinado com a transposição
para gerar os dois vídeos, usando FFmpeg instalado no PATH.

O playback padrão não contém os vocais do artista. A voz separada é usada apenas como
entrada para transcrição e detecção de notas. A saída é organizada por música:

```text
output/
└── Artista - Título/
    ├── Artista - Título.txt
    ├── Artista - Título.mp3
    ├── Artista - Título [+2 semitones].txt
    ├── Artista - Título [+2 semitones].mp3
    ├── Artista - Título.mp4
    └── Artista - Título [+2 semitones].mp4
```

Os arquivos com semitons e vídeos transpostos só são criados quando as opções
correspondentes são ativadas. Por exemplo:

```commandline
python src/UltraSinger.py -i "input/music.mp3" --changetone 2
python src/UltraSinger.py -i "input/music.mp3" --create-lyrics-video
python src/UltraSinger.py -i "input/music.mp3" --changetone -2 --create-lyrics-video
```

### 🎶 Entrada

#### Áudio (modo automático)

##### Arquivo local

```commandline
-i "input/music.mp3"
```

##### YouTube

```commandline
-i https://www.youtube.com/watch?v=BaW_jenozKc
```

#### UltraStar (regerar)

Esse modo reprocessa o áudio e cria um novo arquivo TXT.

```commandline
-i "input/ultrastar.txt"
```

### 🗣 Transcrição

Modelos maiores costumam ser mais precisos, mas também levam mais tempo para transcrever.

#### Whisper

Para um primeiro teste, use `tiny`. Para maior precisão, use `large-v2`.

```commandline
-i XYZ --whisper large-v2
```

##### Idiomas do Whisper

Os idiomas padrão disponíveis são `en, fr, de, es, it, ja, zh, nl, uk, pt`.
Para outros idiomas, é necessário encontrar um modelo de reconhecimento baseado em
fonemas no [🤗 Hugging Face Model Hub](https://huggingface.co). O modelo será baixado automaticamente.

Exemplo para romeno:
```commandline
-i XYZ --whisper_align_model "gigant/romanian-wav2vec2"
```

#### ✍️ Hifenização

É ativada por padrão. Pode ser desativada se não produzir um resultado útil.
As palavras são apenas divididas, sem verificar se cada sílaba começa exatamente
no ponto em que é cantada.

```commandline
-i XYZ --hyphenation True
```

### 👂 Detecção de notas

A detecção de altura é feita pelo `torchcrepe`, uma implementação PyTorch do modelo
CREPE.
Modelos maiores são mais precisos, mas demoram mais. Para testes, use `tiny`;
para maior precisão, use `full`.

```commandline
-i XYZ --crepe full
```

### 👄 Separação de áudio

Os vocais são separados antes de serem enviados aos modelos. Se ocorrerem problemas,
é possível desativar essa etapa; nesse caso, o áudio original será usado.

```commandline
-i XYZ --disable_separation True
```

### 🎼 Partitura

Para gerar partituras, instale o `MuseScore` ou informe o caminho do executável.

```commandline
-i XYZ --musescore_path "C:/Program Files/MuseScore 4/bin/MuseScore4.exe"
```

### 🎵 Transposição

Use `--changetone N` para gerar, além do playback original, uma segunda versão
transposta por `N` semitons. Valores positivos sobem o tom e valores negativos
abaixam o tom. A bateria permanece original; o baixo e os demais instrumentos
harmônicos recebem a transposição. As notas do arquivo UltraStar também são ajustadas.

```commandline
-i XYZ --changetone 2
-i XYZ --changetone -2
```

### 🎬 Lyrics video

Use `--create-lyrics-video` para gerar um vídeo MP4 com a letra sincronizada
diretamente a partir das notas do UltraStar. O FFmpeg precisa estar instalado e
disponível no `PATH`. Use `--video-background` para informar uma imagem ou vídeo
de fundo. Se a transposição também for ativada, o vídeo original e o transposto
serão gerados.

```commandline
-i XYZ --create-lyrics-video
-i XYZ --create-lyrics-video --video-background "input/background.jpg"
-i XYZ --changetone 2 --create-lyrics-video
```

### Versão do formato

Esta opção define a versão do formato do arquivo UltraStar.txt. Consulte a
[especificação oficial do formato UltraStar](https://usdx.eu/format/) para mais informações.

É possível escolher entre três versões. A padrão é `1.0.0`.
* `0.3.0` é a versão antiga; use-a se houver problemas com o formato novo.
* `1.0.0` é a versão atual.
* `1.1.0` é uma versão futura e ainda não está finalizada.

```commandline
-i XYZ --format_version 1.0.0
```

### 🏆 Cálculo de pontuação do UltraStar

É possível medir a pontuação que o cantor da gravação receberia. São exibidas
duas pontuações: simples e precisa. O UltraStar não considera a altura exata
da nota; enquanto ela estiver na faixa correspondente às notas A-G, o jogador
recebe o ponto. Isso permite que vozes masculinas e femininas cantem a mesma
música. A pontuação precisa usa a altura real especificada no TXT e é importante
para gerar MIDI e partituras mais fiéis.

### 📟 Uso da GPU

Uma GPU pode acelerar o processamento e melhorar a qualidade da transcrição e da
detecção de notas.

É necessário um dispositivo CUDA. Atualmente não há suporte CUDA nativo para macOS.

É recomendável instalar o [driver CUDA](https://developer.nvidia.com/cuda-downloads)
da sua GPU. Instale também o PyTorch com CUDA no ambiente virtual; consulte as
[instruções do PyTorch](https://pytorch.org/get-started/locally/) e verifique a
[compatibilidade da sua GPU](https://gist.github.com/standaloneSA/99788f30466516dbcc00338b36ad5acf).

Para GPU NVIDIA, substitua os wheels CPU instalados pelo script por:
```
pip install torch==2.8.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu126
```

Se preferir usar `conda`, consulte o [comando de instalação correspondente](https://pytorch.org/get-started/locally/).

#### Considerações para usuários do Windows

O detector de notas usa PyTorch por meio do `torchcrepe`, portanto a mesma stack
funciona em CPU e CUDA no Windows e no Linux. Não é necessário instalar TensorFlow
nem usar WSL2 para o processamento em CPU.

#### Informações

Se ocorrerem falhas por falta de VRAM, use um modelo menor.
O modelo `large` do Whisper precisa de mais de 8 GB de VRAM.

Também é possível forçar o uso da CPU com a opção `--force_cpu`.

#### Docker

Para usar o Docker, clone o repositório e entre na pasta do UltraSinger:

```commandline
git clone https://github.com/kazzttor/UltraSinger.git
cd UltraSinger
docker build -t ultrasinger .
docker run --gpus all -it --name UltraSinger -v $pwd/src/output:/app/src/output ultrasinger
```

Também há configurações do Docker Compose para GPU (`Nvidia`) e CPU
(`NonGPU`). Entre na pasta correspondente e execute:

```commandline
docker-compose up
```

Por padrão, a pasta `output` do Compose é compartilhada com a pasta `output`
do host. Para alterar esse caminho, edite o arquivo `docker-compose.yml`.
Por exemplo:

```yaml
- /caminho/da/sua/pasta:/app/UltraSinger/src/output
```

Depois de iniciar o contêiner, execute:

```commandline
python3 UltraSinger.py -i arquivo.mp3
python3 UltraSinger.py -i youtube_url
```

Para sair do contêiner, execute `exit`. Para entrar novamente:

```commandline
docker start UltraSinger
docker exec -it UltraSinger /bin/bash
```
