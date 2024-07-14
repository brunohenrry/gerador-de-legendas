import gradio as gr
import ffmpeg
import faster_whisper
import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def transcribe_audio(video_path):
    model = faster_whisper.WhisperModel("medium")
    segments, _ = model.transcribe(video_path, language="en", beam_size=5)
    return segments

def generate_subtitles(segments):
    subtitles = []
    for segment in segments:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        subtitles.append((start, end, text))
    return subtitles

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

def process_video(video_path):
    output_path = "output.mp4"
    
    segments = transcribe_audio(video_path)
    subtitles = generate_subtitles(segments)
    add_subtitles_to_video(video_path, subtitles, output_path)
    
    return output_path

iface = gr.Interface(
    fn=process_video,
    inputs=gr.Video(),
    outputs=gr.Video(),
    title="Subtitle Generator",
    description="Upload a video to generate subtitles and add them to the video.",
)

iface.launch()
