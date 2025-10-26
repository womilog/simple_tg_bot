import os
import ffmpeg
import subprocess


video_root_path = "files/videos/"
audio_root_path = 'files/audios/'

def download_youtube_video(url, output_path='video.mp4'):
    # Используем yt-dlp для скачивания видео
    command = f'yt-dlp -f best -o "{output_path}" {url}'
    subprocess.run(command, shell=True)
    print(f"Видео скачано: {output_path}")


def extract_audio_segment(video_path, output_audio_path, start_time, end_time):
    input_stream = ffmpeg.input(video_path, ss=start_time, to=end_time)
    audio = input_stream.audio
    ffmpeg.output(audio, output_audio_path).run(overwrite_output=True)
    print(f"Аудио сохранено: {output_audio_path}")


def main():
    # Укажите URL видео с YouTube
    video_url = "https://www.youtube.com/watch?v=eRWtytSjKZs"

    # Укажите временной промежуток: начало и конец (в формате ЧЧ:ММ:СС)
    start_time = "00:00:00"
    end_time = "00:05:00"

    # Пути для сохранения файлов
    video_path = f"{video_root_path}video.mp4"
    audio_path = "audio_segment.mp3"

    # Скачиваем видео
    download_youtube_video(video_url, video_path)

    # Извлекаем аудио из определённого временного промежутка
    extract_audio_segment(video_path, audio_path, start_time, end_time)


if __name__ == "__main__":
    main()