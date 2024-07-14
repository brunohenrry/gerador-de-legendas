# Gerador de Legendas

Este projeto é uma aplicação web que gera automaticamente legendas para um vídeo fornecido e as integra ao vídeo. A aplicação utiliza o modelo `faster_whisper` para transcrever o áudio em texto e `moviepy` para adicionar as legendas ao vídeo. A interface é construída usando `Gradio` para uma aplicação web interativa e fácil de usar.

## Funcionalidades

- **Transcrição Automática**: Transcreve o áudio do vídeo usando o modelo `faster_whisper`.
- **Geração de Legendas**: Gera segmentos de legendas com tempos de início e fim.
- **Integração de Legendas**: Adiciona as legendas geradas ao vídeo usando `moviepy`.
- **Interface Interativa**: Fornece uma interface web fácil de usar para carregar vídeos e baixar o resultado com legendas.

## Instalação

Para executar este projeto, você precisa ter o Python instalado juntamente com as bibliotecas necessárias. Você pode instalar as bibliotecas necessárias usando o `pip`.

1. Clone o repositório:

    ```sh
    git clone https://github.com/seuusuario/gerador-de-legendas.git
    cd gerador-de-legendas
    ```

2. Crie um ambiente virtual (opcional, mas recomendado):

    ```sh
    python -m venv env
    source env/bin/activate  # No Windows, use `env\Scripts\activate`
    ```

3. Instale as dependências necessárias:

    ```sh
    pip install gradio faster-whisper moviepy ffmpeg-python
    ```

## Uso

Para iniciar a aplicação, execute o seguinte comando:

```sh
python app.py
```

Isso irá iniciar um servidor web com a interface Gradio. Abra seu navegador e vá para o URL fornecido pelo Gradio (geralmente `http://127.0.0.1:7860/`).

## Como Funciona

### Transcrição de Áudio

A função `transcribe_audio` usa o modelo `faster_whisper` para transcrever o áudio do vídeo em texto. 

```python
def transcribe_audio(video_path):
    model = faster_whisper.WhisperModel("medium")
    segments, _ = model.transcribe(video_path, language="en", beam_size=5)
    return segments
```

### Geração de Legendas

A função `generate_subtitles` converte os segmentos transcritos em legendas com tempos de início e fim.

```python
def generate_subtitles(segments):
    subtitles = []
    for segment in segments:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        subtitles.append((start, end, text))
    return subtitles
```

### Adicionar Legendas ao Vídeo

A função `add_subtitles_to_video` adiciona as legendas geradas ao vídeo usando `moviepy`.

```python
def add_subtitles_to_video(video_path, subtitles, output_path):
    video = VideoFileClip(video_path)
    subtitle_clips = []

    for start, end, text in subtitles:
        txt_clip = (TextClip(text, fontsize=24, color='white', size=video.size)
                    .set_position(('center', 'bottom'))
                    .set_start(start)
                    .set_duration(end - start))
        subtitle_clips.append(txt_clip)

    video = CompositeVideoClip([video, *subtitle_clips])
    video.write_videofile(output_path, codec='libx264')
```

### Processar Vídeo

A função `process_video` gerencia todo o processo de transcrição do áudio, geração de legendas e adição das legendas ao vídeo.

```python
def process_video(video_path):
    output_path = "output.mp4"
    
    segments = transcribe_audio(video_path)
    subtitles = generate_subtitles(segments)
    add_subtitles_to_video(video_path, subtitles, output_path)
    
    return output_path
```

### Interface Gradio

A interface Gradio fornece uma maneira interativa para o usuário carregar um vídeo e obter o vídeo legendado de volta.

```python
iface = gr.Interface(
    fn=process_video,
    inputs=gr.Video(),
    outputs=gr.Video(),
    title="Gerador de Legendas",
    description="Carregue um vídeo para gerar legendas e adicioná-las ao vídeo.",
)

iface.launch()
```

## Contribuição

Se você quiser contribuir para este projeto, sinta-se à vontade para abrir issues ou enviar pull requests no [repositório do GitHub](https://github.com/brunohenrry/gerador-de-legendas).

---
