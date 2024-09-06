"""Common Prints"""

from modules.console_colors import ULTRASINGER_HEAD, gold_highlighted, light_blue_highlighted


def print_help() -> None:
    """Print help text"""
    help_string = """
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
    """
    print(help_string)


def print_support() -> None:
    """Print support text"""
    print()
    print(
        f"{ULTRASINGER_HEAD} {gold_highlighted('Gosta do UltraSinger? Quer melhorar? então ajuste com seu')} {light_blue_highlighted('apoio')}{gold_highlighted('!')}"
    )
    print(
        f"{ULTRASINGER_HEAD} Acesse a página do projeto -> https://github.com/kazzttor/UltraSinger"
    )
    print(
        f"{ULTRASINGER_HEAD} {gold_highlighted('Isto ajudará a manter e melhorar o projeto.')}"
    )


def print_version(app_version: str) -> None:
    """Print version text"""
    print()
    print(f"{ULTRASINGER_HEAD} {gold_highlighted('*****************************')}")
    print(f"{ULTRASINGER_HEAD} {gold_highlighted('UltraSinger Versão:')} {light_blue_highlighted(app_version)}")
    print(f"{ULTRASINGER_HEAD} {gold_highlighted('*****************************')}")
