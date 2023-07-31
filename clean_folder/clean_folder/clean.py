import re
from shutil import move, unpack_archive
import pathlib
import sys
import concurrent.futures

# Константи розширеннь файлів
IMAGES_EXT = (".jpeg", ".png", ".jpg", ".svg")
VIDEO_EXT = (".avi", ".mp4", ".mov", ".mkv")
DOC_EXT = (".doc", ".docx", ".txt", ".pdf", ".lsx", ".pptx")
MUSIC_EXT = (".mp3", ".ogg", ".wav", ".amr")
ARCHIVES_EXT = (".zip", ".gz", ".tar")

FOLDERS_NAMES = ("images", "documents", "audio", "video", "archives")
# Глобальні змінні
TRANS = {}
known_ext = []
unknown_ext = []
DEFAULT_FOLDERS = []


# Опис усіх необхідних функцій
# -----------------------------------------------------------
# Підготуємо один раз словник для транслітерації імені файлу
def prepare_translate_dict():
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()


# Проводимо транслітерацію та заміну усіх частин зберігаючи розширення файлу
def normalize(s):
    s2 = s.translate(TRANS)
    l = s2.split(".")
    if len(l) > 1:
        ext = "." + l.pop()
        s2 = ".".join(l)
    else:
        ext = ""
    return re.sub(r"[^a-zA-Z0-9]", "_", s2) + ext


# Створення базових категорійних папок
def create_default_folders(path):
    dic = {}
    if path.is_dir():
        for i in FOLDERS_NAMES:
            new_folder = path / i
            if not new_folder.exists():
                new_folder.mkdir(parents=True)
            dic.update({new_folder.name: new_folder})
    return dic


def analisis_file_object_dir(file_object, category_folders):
    if file_object.name in FOLDERS_NAMES:
        return None
    elif not any(file_object.iterdir()):
        file_object.rmdir()
    else:
        analisis_folder_contents(file_object, category_folders)
        if not any(file_object.iterdir()):
            file_object.rmdir()
        else:
            file_object.rename(file_object.with_name(normalize(file_object.name)))


def process_file(file_object, path):
    suffix = file_object.suffix

    # Using the match statement to implement the switch-like behavior
    match suffix:
        case ext if ext in IMAGES_EXT:
            move_file_to_folder(file_object, FOLDERS_NAMES[0], path)
        case ext if ext in VIDEO_EXT:
            move_file_to_folder(file_object, FOLDERS_NAMES[3], path)
        case ext if ext in MUSIC_EXT:
            move_file_to_folder(file_object, FOLDERS_NAMES[2], path)
        case ext if ext in DOC_EXT:
            move_file_to_folder(file_object, FOLDERS_NAMES[1], path)
        case ext if ext in ARCHIVES_EXT:
            unpack_and_remove_archive(file_object)
        case _:
            add_to_unknown_ext_list(file_object)


def move_file_to_folder(file_object, folder_name, path):
    move(
        file_object,
        DEFAULT_FOLDERS.get(folder_name, path) / normalize(file_object.name),
    )
    if file_object.suffix not in known_ext:
        known_ext.append(file_object.suffix)


def unpack_and_remove_archive(file_object):
    unpack_archive(file_object, DEFAULT_FOLDERS.get(FOLDERS_NAMES[4]))
    if file_object.suffix not in known_ext:
        known_ext.append(file_object.suffix)
    file_object.unlink()


def add_to_unknown_ext_list(file_object):
    if file_object.suffix not in unknown_ext:
        unknown_ext.append(file_object.suffix)

def analisis_folder_contents(path):
    if path.is_dir():
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for file_object in path.iterdir():
                if file_object.is_dir():
                    future = executor.submit(analisis_file_object_dir, file_object)
                    futures.append(future)
                else:
                    future = executor.submit(process_file, file_object, path)
                    futures.append(future)
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print(e)


def sort_path(path):
    prepare_translate_dict()
    path = sys.argv[1]
    work_file = pathlib.Path(path)
    DEFAULT_FOLDERS = create_default_folders(work_file)
    analisis_folder_contents(work_file)
    for k, v in DEFAULT_FOLDERS.items():
        num_files = len(list(v.glob("*")))
        print(f"{k} folder have {num_files} files")
    print(unknown_ext)
    print(known_ext)


def main():
    if len(sys.argv) <= 1:
        print("Sort was failed. No argument with path to folder")
    else:
        sort_path(sys.argv[1])


# -----------------------------------------------------------
# Основна (main) частина
if __name__ == "__main__":
    main()
