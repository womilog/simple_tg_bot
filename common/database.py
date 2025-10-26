import re
import sqlite3 as sq
from typing import Optional, Any


class AudioDatabase:
    def __init__(self, db_name: str = 'chopik.db') -> None:
        """
        Инициализация объекта базы данных.

        :param db_name: Название файла базы данных.
        """
        self.db_name = db_name

    def execute_query(self, query: str, params: Optional[tuple] = None) -> bool:
        """
        Выполняет запросы к базе данных, которые не возвращают данные
        :param query: SQL-запрос
        :param params: Параметры для SQL-запроса.
        :return: True, если запрос выполнен успешно, иначе False.
        """
        try:
            with sq.connect(self.db_name) as con:
                cur = con.cursor()
                cur.execute(query, params or ())
                con.commit()
            return True
        except sq.Error as ex:
            print(f"Ошибка выполнения запроса: {ex}")
            return False

    def fetch_query(self, query: str, params: Optional[tuple] = None) -> Optional[Any]:
        """
        Выполняет запрос к базе данных, который возвращает данные.
        :param query: SQL-запрос.
        :param params: Параметры для SQL-запроса.
        :return: Результат запроса или None, если произошла
        """
        try:
            with sq.connect(self.db_name) as con:
                cur = con.cursor()
                cur.execute(query, params or ())
                return cur.fetchone()
        except sq.Error as ex:
            print(f"Ошибка выполнения запроса: {ex}")
            return None

    def fetch_queries(self, query: str, params: Optional[tuple] = None) -> Optional[Any]:
        """
        Выполняет запросы к базе данных, которые возвращают данные.
        :param query: SQL-запрос.
        :param params: Параметры для SQL-запроса.
        :return: Результат запроса или None, если произошла
        """
        try:
            with sq.connect(self.db_name) as con:
                cur = con.cursor()
                cur.execute(query, params or ())
                return cur.fetchall()
        except sq.Error as ex:
            print(f"Ошибка выполнения запроса: {ex}")
            return None

    def create_table(self) -> bool:
        """
        Созадает таблицу scheduler.
        :return: True, если таблица успешно создана или уже существует, иначе False
        """
        query = """
        CREATE TABLE IF NOT EXISTS audio (
            audio_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            author TEXT,
            data BLOB
        )
        """
        return self.execute_query(query)

    def get_audio_name(self, path_audio):
        res = re.findall(r'назв_(\w+)\.mp3', path_audio)
        return res[0]

    def get_author(self, path_audio):
        res = re.findall(r'audios[/|\\]([^_]+)', path_audio)
        return res[0]

    def write_audio(self, path_audio: str) -> bool:
        """
        Записывает новую запись в таблицу расписания.

        :param path_audio: Путь к аудио.
        :return: True, если запись успешно добавлена, иначе False.
        """
        name = self.get_audio_name(path_audio)
        author = self.get_author(path_audio)

        with sq.connect('chopik.db') as con:
            cur = con.cursor()

            try:
                with open(path_audio, 'rb') as f:
                    binary_audio = f.read()
            except sq.Error as e:
                print(f"Ошибка при чтении аудио файла: {e}")

            try:
                cur.execute("""
                    INSERT INTO audio VALUES(NULL, ?, ?, ?)
                """, (name, author, binary_audio))
                return True
            except sq.Error as e:
                print(f"Ошибка при записе аудио в бд: {e}")
                return False

    def read_audio(self, name: str) -> Optional[str]:
        """
        Возвращает последний добавленный список из таблицы расписания.
        :
        param name: имя аудио.
        :return: Последняя запись или None, если произошла ошибка.
        """

        query = """
        SELECT data FROM audio 
        WHERE name=? 
        """

        result = self.fetch_query(query, (name, ))
        return result[0] if result else None

    def all_audios_name(self) -> str:
        """
        Возвращает все названия аудио, вместе с авторами
        :return:
        """

        query = """
        SELECT author, name FROM audio
        """

        result = self.fetch_queries(query, ())
        return '\n'.join([f"{para[0]}: {para[1]}" for para in sorted(result, key=lambda x: x[0])]) if result else None

    def author_audios_name(self, author: str) -> str:
        """
        Возвращает все названия аудио определенного автора
        :return:
        """

        query = """
        SELECT name FROM audio
        WHERE author=?
        """

        result = self.fetch_queries(query, (author, ))
        return '\n'.join([obj[0] for obj in result]) if result else None


# def create_tbl_audio():
#     with sq.connect('chopik.db') as con:
#         cur = con.cursor()
#
#         cur.execute("""CREATE TABLE IF NOT EXISTS audio(
#             audio_id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT,
#             data BLOB)
#         """)
#
#     return True
#
#
# def read_audio(name):
#     with sq.connect('chopik.db') as con:
#         cur = con.cursor()
#
#         cur.execute("""SELECT data FROM audio WHERE name=?""", (name,))
#         binary_audio = cur.fetchone()[0]
#
#     if binary_audio:
#         return binary_audio
#
#     return False
#
#
# def write_audio(path_audio, name):
#     with sq.connect('chopik.db') as con:
#         cur = con.cursor()
#
#         try:
#             with open(path_audio, 'rb') as f:
#                 binary_audio = f.read()
#         except sq.Error as e:
#             print(f"Ошибка при чтении аудио файла: {e}")
#
#         try:
#             cur.execute("""
#                 INSERT INTO audio VALUES(NULL, ?, ?)
#             """, (name, binary_audio))
#             return True
#         except sq.Error as e:
#             print(f"Ошибка при записе аудио в бд: {e}")
#             return False
#
#
# def read_all_audio():
#     with sq.connect('chopik.db') as con:
#         cur = con.cursor()
#
#         cur.execute("SELECT name FROM audio")
#         audio_names = [name[0] for name in cur]
#
#     return audio_names


class SchedulerDatabase:
    """Класс для работы с базой данных распорядка"""

    def __init__(self, db_name: str='chopik.db') -> None:
        """
        Инициализация объекта базы данных.

        :param db_name: Название файла базы данных.
        """
        self.db_name = db_name

    def execute_query(self, query:str, params: Optional[tuple]=None) -> bool:
        """
        Выполняет запросы к базе данных, которые не возвращают данные
        :param query: SQL-запрос
        :param params: Параметры для SQL-запроса.
        :return: True, если запрос выполнен успешно, иначе False.
        """
        try:
            with sq.connect(self.db_name) as con:
                cur = con.cursor()
                cur.execute(query, params or ())
                con.commit()
            return True
        except sq.Error as ex:
            print(f"Ошибка выполнения запроса: {ex}")
            return False

    def fetch_query(self, query: str, params: Optional[tuple] = None) -> Optional[Any]:
        """
        Выполняет запросы к базе данных, которые возвращают данные.
        :param query: SQL-запрос.
        :param params: Параметры для SQL-запроса.
        :return: Результат запроса или None, если произошла
        """
        try:
            with sq.connect(self.db_name) as con:
                cur = con.cursor()
                cur.execute(query, params or ())
                return cur.fetchone()
        except sq.Error as ex:
            print(f"Ошибка выполнения запроса: {ex}")
            return None

    def create_table(self) -> bool:
        """
        Созадает таблицу scheduler.
        :return: True, если таблица успешно создана или уже существует, иначе False
        """
        query = """
        CREATE TABLE IF NOT EXISTS scheduler (
            schdl_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            list TEXT 
        )
        """
        return self.execute_query(query)

    def write_schedule(self, data: str) -> bool:
        """
        Записывает новую запись в таблицу расписания.

        :param data: Список/данные для записи.
        :return: True, если запись успешно добавлена, иначе False.
        """
        query = """
        INSERT INTO scheduler (date, list) 
        VALUES (DATE('now'), ?)
        """
        return self.execute_query(query, (data,))

    def read_last_schedule(self) -> Optional[str]:
        """
        Возвращает последний добавленный список из таблицы расписания.

        :return: Последняя запись или None, если произошла ошибка.
        """
        query = """
        SELECT list FROM scheduler 
        ORDER BY date DESC 
        LIMIT 1
        """
        result = self.fetch_query(query)
        return result[0] if result else None