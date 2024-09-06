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

# UltraSinger

> ⚠️ _Este projeto parmanece em desenvolvimento!_

_Este é um fork do projeto UltraSinger que traduz a interface do projeto para português do Brasil e adiciona a possibilidade de criar uma versão do karaoke com notas transposta (ainda em desenvolvimento)._

UltraSinger é uma ferramenta que cria aytomaticamente UltraStar.txt, midi and notes de uma música. 
Ele lança automaticamente arquivos UltraStar, adicionando texto e tocando em arquivos UltraStar e cria arquivos de karaokê UltraStar separados.
Ele também pode relançar os arquivos UltraStar atuais e calcular a possível pontuação no jogo.

Vários modelos de IA são usados para extrair texto da voz e determinar o tom.

Por favor, mencione o UltraSinger em seu arquivo UltraStar.txt se você usá-lo. Isso ajuda outras pessoas a encontrar essa ferramenta e ajuda essa ferramenta a ser aprimorada e mantida. Você só deve usá-lo em músicas licenciadas pela Creative Commons.

## ❤️ Suporte
Existem muitas maneiras de apoiar este projeto. Atribuir estrelas ⭐️ o repositório é apenas um 🙏

Você também pode apoiar este trabalho em <a href="https://github.com/sponsors/rakuri255">Apoiadores do Github</a> ou <a href="https://patreon.com/Rakuri">Patreon</a> ou <a href="https://www.buymeacoffee.com/rakuri255" target="_blank">Buy Me a Coffee</a>.

Isso vai me ajudar muito a manter este projeto vivo e melhorá-lo.

<a href="https://www.buymeacoffee.com/rakuri255" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me a Coffee" style="height: 60px !important;width: 217px !important;" ></a>
<a href="https://patreon.com/Rakuri"><img src="https://raw.githubusercontent.com/rakuri255/UltraSinger/main/assets/patreon.png" alt="Become a Patron" style="height: 60px !important;width: 217px !important;"/> </a>
<a href="https://github.com/sponsors/rakuri255"><img src="https://raw.githubusercontent.com/rakuri255/UltraSinger/main/assets/mona-heart-featured.webp" alt="GitHub Sponsor" style="height: 60px !important;width: auto;"/> </a>

## Índice

- [UltraSinger](#ultrasinger)
  - [❤️ Suporte](#️-support)
  - [Índice](#table-of-contents)
  - [💻 Como usar o código-fonte](#-how-to-use-this-source-code)
    - [Instalação](#installation)
    - [Executando](#run)
  - [📖 Como usar](#-how-to-use-the-app)
    - [🎶 Entrada](#-input)
      - [Áudio (totalmente automático)](#audio-full-automatic)
        - [Arquivo Local](#local-file)
        - [Youtube](#youtube)
      - [UltraStar (regerar)](#ultrastar-re-pitch)
    - [🗣 Transcritor](#-transcriber)
      - [Whisper](#whisper)
        - [Idiomas do Whisper](#whisper-languages)
      - [✍️ Hifenização](#️-hyphenation)
    - [👂 Pitcher](#-pitcher)
    - [👄 Separação](#-separation)
    - [Planilha da música](#sheet-music)
    - [Versão de formato](#format-version)
    - [🏆 Cálculo de pontuação do UltraStar](#-ultrastar-score-calculation)
    - [📟 Uso da GPU](#-use-gpu)
      - [Consideraçoes para usuários do Windows](#considerations-for-windows-users)
      - [Informações](#info)
      - [Uso com Docker](#docker)

## 💻 Como usar o código-fonte

### Instalação

* Instale o Python 3.10 **(Versões anteriores e recentes podem apresentar problemas)**. [Download](https://www.python.org/downloads/)
* Instale também ffmpeg separadamente com registro no PATH. [Download](https://www.ffmpeg.org/download.html)
* Vá para a pasta `install` e execute o script de sistalação de acordo com o Sistema Operacional.
  * Escolha `GPU` se possui uma GPU nvidia CUDA.
  * Escolha `CPU` se não possui uma GPU nvidia CUDA.

### Executando

* Na pasta raiz execute `run_on_windows.bat` ou `run_on_linux.sh` para iniciar o aplicativo.
* Agora voce pode usar o arquivo fonte do UltraSinger com `py UltraSinger.py [opcoes] [modo] [transcrição] [pitcher] [extra]`. veja [Como usar](#how-to-use) para maiores informações.

## 📖 Como usar o aplicativo

_Nem todas as funções estão funcionando!_
```commandline
 UltraSinger.py [opcoes] [modo] [transcrição] [pitcher] [extra]
    
    [opcoes]
    -h      Este texto de ajuda.
    -i      dado de entrada 
            Ex: Ultrastar.txt áudio como .mp3, .wav, link do youtube
    -o      Pasta de saída
    
    [modo]
    ## DADO DE ENTRADA é áudio ##
    default  (padrão) - Cria tudo
    
    # Criação de arquivo único em desenvolvimento, somente possível criar tudo!
    (-u      Criar arquivo txt para o UltraStar) # Em desenvolvimento 
    (-m      Criar arquivo MIDI) # Em desenvolvimento
    (-s      Criar Planilha) # Em desenvolvimento
    
    ## DADO DE ENTRADA é ultrastar.txt ##
    default  (padrão) - Cria tudo

    # Criação de arquivo único em desenvolvimento, somente possível criar tudo!
    (-r      regerar Ultrastar.txt (entrada precisa ser arquivo de áudio)) # Em desenvolvimento 
    (-p      Verificar o pitch de Ultrastar.txt fornecido) # Em desenvolvimento 
    (-m      Criar arquivo MIDI) # Em desenvolvimento 

    [transcrição]
    # Transcritor padrão é o whisper
    --whisper               Modelo multi-idioma > tiny|base|small|medium|large-v1|large-v2  >> ((padrão) é large-v2)
                            Modelo somente em inglês > tiny.en|base.en|small.en|medium.en
    --whisper_align_model   Usar outro modelo de idioma Whisper fornecido por huggingface.co
    --language              Forçaro o idioma detectado pelo whisper, não afeta a transcrição, mas os passos depois
    --whisper_batch_size    Reduza se pouca memória da GPU >> ((padrão) é 16)
    --whisper_compute_type  Mude para "int8" se pouca memória da GPU (pode reduzir accurácia) >> ((padrão) é "float16" para dispositivos cuda, "int8" para cpu)
    
    [pitcher]
    # Picher padrão é Crepe
    --crepe            tiny|full >> ((padrão) é full)
    --crepe_step_size  unit is miliseconds >> ((padrão) é 10)
    
    [extra]
    --hyphenation           (hifenização) True|False >> ((padrão) é True)
    --disable_separation    (desabilitar separação) True|False >> ((padrão) é False)
    --disable_karaoke       (desabilitar versão karaoke) True|False >> ((padrão) é False)
    --create_audio_chunks   (criar partes de áudio) True|False >> ((padrão) é False)
    --keep_cache            (manter cache) True|False >> ((padrão) é False)
    --plot                  (plotar) True|False >> ((padrão) é False)
    --format_version        (versão do formato UltraStar) 0.3.0|1.0.0|1.1.0 >> ((padrão) é 1.0.0)
    --musescore_path        local do executável MuseScore
    
    [dispositivo]
    --force_cpu             True|False >> ((padrão) é False)  Forçar todo o processamento por cpu
    --force_whisper_cpu     True|False >> ((padrão) é False)  Forçar somente processamento do Whisper por cpu
    --force_crepe_cpu       True|False >> ((padrão) é False)  Forçar somente processamento do crepe por cpu

```

Para o uso normal, basta usar os argumentos de [opcoes]. Os demais parâmetros são opcionais.

### 🎶 Entrada

#### Áudio (totalmente automático)

##### Arquivo local

```commandline
-i "input/music.mp3"
```

##### Youtube

```commandline
-i https://www.youtube.com/watch?v=BaW_jenozKc
```

#### UltraStar (re-pitch)

This re-pitch the audio and creates a new txt file.

```commandline
-i "input/ultrastar.txt"
```

### 🗣 Transcriber

Keep in mind that while a larger model is more accurate, it also takes longer to transcribe.

#### Whisper

For the first test run, use the `tiny`, to be accurate use the `large-v2` model.

```commandline
-i XYZ --whisper large-v2
```

##### Whisper languages

Currently provided default language models are `en, fr, de, es, it, ja, zh, nl, uk, pt`. 
If the language is not in this list, you need to find a phoneme-based ASR model from 
[🤗 huggingface model hub](https://huggingface.co). It will download automatically.

Example for romanian:
```commandline
-i XYZ --whisper_align_model "gigant/romanian-wav2vec2"
```

#### ✍️ Hyphenation

Is on by default. Can also be deactivated if hyphenation does not produce 
anything useful. Note that the word is simply split, 
without paying attention to whether the separated word really 
starts at the place or is heard.  

```commandline
-i XYZ --hyphenation True
```

### 👂 Pitcher

Pitching is done with the `crepe` model.
Also consider that a bigger model is more accurate, but also takes longer to pitch.
For just testing you should use `tiny`.
If you want solid accurate, then use the `full` model.

```commandline
-i XYZ --crepe full
```

### 👄 Separation

The vocals are separated from the audio before they are passed to the models. If problems occur with this, 
you have the option to disable this function; in which case the original audio file is used instead.

```commandline
-i XYZ --disable_separation True
```

### Sheet Music

For Sheet Music generation you need to have `MuseScore` installed on your system.
Or provide the path to the `MuseScore` executable.

```commandline
-i XYZ --musescore_path "C:/Program Files/MuseScore 4/bin/MuseScore4.exe"
```

### Format Version

This defines the format version of the UltraStar.txt file. For more info see [Official UltraStar format specification](https://usdx.eu/format/).

You can choose between 3 different format versions. The default is `1.0.0`.
* `0.3.0` is the old format version. Use this if you have problems with the new format.
* `1.0.0` is the current format version.
* `1.1.0` is the upcoming format version. It is not finished yet.

```commandline
-i XYZ --format_version 1.0.0
```

### 🏆 Ultrastar Score Calculation

The score that the singer in the audio would receive will be measured. 
You get 2 scores, simple and accurate. You wonder where the difference is? 
Ultrastar is not interested in pitch hights. As long as it is in the pitch range A-G you get one point. 
This makes sense for the game, because otherwise men don't get points for high female voices and women don't get points 
for low male voices. Accurate is the real tone specified in the txt. I had txt files where the pitch was in a range not 
singable by humans, but you could still reach the 10k points in the game. The accuracy is important here, because from
this MIDI and sheet are created. And you also want to have accurate files


### 📟 Use GPU

With a GPU you can speed up the process. Also the quality of the transcription and pitching is better.

You need a cuda device for this to work. Sorry, there is no cuda device for macOS.

It is optional (but recommended) to install the cuda driver for your gpu: see [driver](https://developer.nvidia.com/cuda-downloads).
Install torch with cuda separately in your `venv`. See [tourch+cuda](https://pytorch.org/get-started/locally/).
Also check you GPU cuda support. See [cuda support](https://gist.github.com/standaloneSA/99788f30466516dbcc00338b36ad5acf)

Command for `pip`:
```
pip3 install torch==2.0.1+cu117 torchvision==0.15.2+cu117 torchaudio==2.0.2+cu117 --index-url https://download.pytorch.org/whl/cu117
```

When you want to use `conda` instead you need a [different installation command](https://pytorch.org/get-started/locally/).

#### Considerations for Windows users

The pitch tracker used by UltraSinger (crepe) uses TensorFlow as its backend.
TensorFlow dropped GPU support for Windows for versions >2.10 as you can see in this [release note](https://github.com/tensorflow/tensorflow/releases/tag/v2.11.1) and their [installation instructions](https://www.tensorflow.org/install/pip#windows-native).

For now UltraSinger runs the latest version available that still supports GPUs on windows.

For running later versions of TensorFlow on windows while still taking advantage of GPU support the suggested solution is:

* [install WSL2](https://learn.microsoft.com/en-us/windows/wsl/install)
* within the Ubuntu WSL2 installation
  * run `sudo apt update && sudo apt install nvidia-cuda-toolkit`
  * follow the setup instructions for UltraSinger at the top of this document

#### Info

If something crashes because of low VRAM then use a smaller model.
Whisper needs more than 8GB VRAM in the `large` model!

You can also force cpu usage with the extra option `--force_cpu`.

#### Docker
to run the docker run `git clone https://github.com/rakuri255/UltraSinger.git`
enter the UltraSinger folder.
run this command to build the docker
`docker build -t ultrasinger .` make sure to include the "." at the end
let this run till complete.
then run this command
`docker run --gpus all -it --name UltraSinger -v  $pwd/src/output:/app/src/output ultrasinger`

Docker-Compose
there are two files that you can pick from.
cd into `docker-compose` folder and then cd into `Nvidia` or `NonGPU`
Run `docker-compose up` to download and setup

Nvidia is for if you have a nvidia gpu to use with UltraSinger.
NonGPU is for if you wish to only use the CPU for UltraSinger.

Output
by default the docker-compose will setup the output folder as `/output` inside the docker.
on the host machine it will map to the folder with the `docker-compose.yml` file under `output`
you may chnage this by editing the `docker-compose.yml`

to edit the file.
use any text editor you wish. i would recoment nano.
run `nano docker-compose.yml`
then change this line
`            -  ./output:/app/UltraSinger/src/output`
to anything you line for on your host machine.
`            -  /yourfolderpathhere:/app/UltraSinger/src/output`
sample
`            -  /mnt/user/appdata/UltraSinger:/output`
note the blank space before the `-`
formating is important here in this file.

this will create and drop you into the docker.
now run this command.
`python3 UltraSinger.py -i file`
or
`python3 UltraSinger.py -i youtube_url`
to use mp3's in the folder you git cloned you must place all songs you like in UltraSinger/src/output.
this will be the place for youtube links aswell.


to quit the docker just type exit.

to reenter docker run this command
`docker start UltraSinger && Docker exec -it UltraSinger /bin/bash`

