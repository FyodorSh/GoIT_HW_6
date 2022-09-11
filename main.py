# Завдання
# У багатьох на робочому столі є папка, яка називається якось ніби "Розібрати". Як правило, розібрати цю папку руки
# ніколи так і не доходять.
#
# Ми з вами напишемо скрипт, який розбере цю папку. Зрештою ви зможете настроїти цю програму під себе і вона
# виконуватиме індивідуальний сценарій, що відповідає вашим потребам. Для цього наш додаток буде перевіряти розширення
# файлу (останні символи у імені файлу, як правило, після крапки) і, залежно від розширення, приймати рішення,
# до якої категорії віднести цей файл.
#
# Скрипт приймає один аргумент при запуску — це ім'я папки, в якій він буде проводити сортування. Допустимо файл з
# програмою називається sort.py, тоді, щоб відсортувати папку /user/Desktop/Мотлох, треба запустити скрипт командою
# python sort.py /user/Desktop/Мотлох
#
# Для того щоб успішно впорається з цим завданням, ви повинні винести логіку обробки папки в окрему функцію.
# Щоб скрипт міг пройти на будь-яку глибину вкладеності, функція обробки папок повинна рекурсивно викликати сама себе,
# коли їй зустрічаються вкладенні папки.
# Скрипт повинен проходити по вказаній під час виклику папці та сортирувати всі файли по групам:
#
# зображення ('JPEG', 'PNG', 'JPG', 'SVG');
# відео файли ('AVI', 'MP4', 'MOV', 'MKV');
# документи ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX');
# музика ('MP3', 'OGG', 'WAV', 'AMR');
# архіви ('ZIP', 'GZ', 'TAR');
# невідомі розширення.
# Ви можете розширити та доповнити цей список, якщо хочете.
#
# В результатах роботи повинні бути:
#
# Список файлів в кожній категорії (музика, відео, фото и ін.)
# Перелік усіх відомих скрипту розширень, які зустрічаються в цільовій папці.
# Перелік всіх розширень, які скрипту невідомі.
# Після необхідно додати функції, які будуть відповідати за обробку кожного типу файлів.
#
# Крім того, всі файли та папки треба перейменувати, видалив із назви всі символи, що призводять до проблем. Для цього
# треба застосувати до імен файлів функцію normalize. Слід розуміти, що перейменувати файли треба так, щоб не змінити
# розширень файлів.
#
# Функція normalize:
#
# Проводить транслітерацію кирилічного алфавіту на латинський.
# Замінює всі символи крім латинських літер, цифр на '_'.
# Вимоги до функції normalize:
#
# приймає на вхід рядок та повертає рядок;
# проводить транслітерацію кирилічних символів на латиницю;
# замінює всі символи, крім літер латинського алфавіту та цифр, на символ '_';
# транслітерація може не відповідати стандарту, але бути читабельною;
# великі літери залишаються великими, а маленькі — маленькими після транслітерації.

# -----------------------------------------------
# Умови для обробки:
# зображення переносимо до папки images
# документи переносимо до папки documents
# аудіо файли переносимо до audio
# відео файли до video
# архіви розпаковуються та їх вміст переноситься до папки archives

# -----------------------------------------------
# Критерії прийому завдання:
# всі файли та папки перейменовуються за допомогою функції normalize.
# розширення файлів не змінюється після перейменування.
# порожні папки видаляються
# скрипт ігнорує папки archives, video, audio, documents, images;
# розпакований вміст архіву переноситься до папки archives у підпапку, названу так само, як і архів, але без розширення
# у кінці;
# файли, розширення яких невідомі, залишаються без зміни.

import re
import sys
import os
import zipfile
import py7zr
import patoolib

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

EXTENSIONS = {('JPEG', 'PNG', 'JPG', 'SVG'): "images", ('AVI', 'MP4', 'MOV', 'MKV'): "video",
              ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'): "documents",  ('MP3', 'OGG', 'WAV', 'AMR'): "audio",
              ('ZIP', 'RAR', '7ZIP', '7Z', 'GZ', 'TAR'): "archives"}

SORT_DIRS = {}
SORT_DIRS_LIST = []

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def translit(input_string: str) -> str:
    return input_string.translate(TRANS)


def normalize(file_name: str):
    regex = r"[^a-zA-Z0-9.]"
    subst = "_"
    file_name = re.sub(regex, subst, translit(file_name), 0, re.MULTILINE)
    return file_name


def check_dir(current_path: str, if_empty_delete=False):
    for file in os.listdir(current_path):
        file_path = os.path.join(current_path, file)
        if file_path in SORT_DIRS_LIST:
            continue

        if os.path.isdir(file_path):
            if len(os.listdir(file_path)) == 0:
                if if_empty_delete:
                    os.removedirs(file_path)
                    continue
            else:
                check_dir(file_path)
                continue
        file_name_split = os.path.splitext(file)
        file_ext = file_name_split[1].replace(".", "").upper()

        for ext in EXTENSIONS:
            if file_ext in ext:
                directory = EXTENSIONS.get(ext)
                sort_dir = SORT_DIRS.get(directory)
                new_file_name = os.path.join(sort_dir, normalize(file))
                os.replace(file_path, new_file_name)
                if directory == "archives":
                    try:
                        extract_path = os.path.join(sort_dir, normalize(file_name_split[0]))
                        if file_ext == "7Z":
                            archive = py7zr.SevenZipFile(new_file_name, mode='r')
                            archive.extractall(path = extract_path)
                            archive.close()
                        elif file_ext == "RAR":
                            patoolib.extract_archive(new_file_name, outdir=extract_path, interactive=False)
                        else:
                            with zipfile.ZipFile(new_file_name, 'r') as zip_ref:
                                zip_ref.extractall(extract_path)
                        os.remove(new_file_name)
                        print(f"{new_file_name} extracted")
                    except:
                        print(f"{file} not zip archive")
                else:
                    print(f'"{file}" removed and renamed to folder "{directory}"')


def create_sort_dir(start_path: str):
    for ext in EXTENSIONS:
        sort_dir = EXTENSIONS.get(ext)
        sort_dir_path = os.path.join(start_path, sort_dir)
        if not os.path.exists(sort_dir_path):
            os.mkdir(sort_dir_path)
        SORT_DIRS.update({sort_dir: sort_dir_path})
        SORT_DIRS_LIST.append(sort_dir_path)


def main(start_path: str):
    create_sort_dir(start_path)
    check_dir(start_path)
    check_dir(start_path, True) # delete empty folders
    print("Sorting complete.")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        start_path = sys.argv[1]
    else:
        start_path = "i:\\test_dir\\"

    main(start_path)