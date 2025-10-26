import os

from common.database import write_audio, create_tbl_audio, read_audio

file_path = 'files/audios/никто_назв_вдох_выдох.mp3'


if __name__ == '__main__':
    work_directory = os.getcwd()

    if 'chopik.db' not in work_directory:
        create_tbl_audio()

    write_audio(file_path, 'Вдох-Выдох')





