import re
import shutil
import pathlib
import sys

#Константи розширеннь файлів
IMAGES_EXT = ('.jpeg', '.png', '.jpg', '.svg')
VIDEO_EXT = ('.avi', '.mp4', '.mov', '.mkv')
DOC_EXT = ('.doc', '.docx', '.txt', '.pdf', '.lsx', '.pptx')
MUSIC_EXT = ('.mp3', '.ogg', '.wav', '.amr')
ARCHIVES_EXT = ('.zip', '.gz', '.tar')

FOLDERS_NAMES = ('images','documents','audio','video','archives')
#Глобальні змінні
TRANS = {}
known_ext = []
unknown_ext = []

# Опис усіх необхідних функцій
#-----------------------------------------------------------
# Підготуємо один раз словник для транслітерації імені файлу
def prepare_translate_dict():
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

#Проводимо транслітерацію та заміну усіх частин зберігаючи розширення файлу
def normalize(s):
    s2 = s.translate(TRANS)
    l = s2.split('.')
    if len(l) > 1:
        ext = '.' + l.pop()
        s2 = '.'.join(l)
    else:
        ext =''
    return re.sub(r'[^a-zA-Z0-9]', '_', s2) + ext

#Створення базових категорійних папок
def create_default_folders(path):
    dic = {}
    if path.is_dir():
        for i in FOLDERS_NAMES:
            new_folder = path / i
            if not new_folder.exists():
                new_folder.mkdir(parents=True)
            dic.update({new_folder.name: new_folder})
    return dic 

# def normalize_all_tree_in(path):
#     other_folders = []
#     if path.is_dir():
#         for file_object in path.iterdir():
#             file_object.rename(file_object.with_name(normalize(file_object.name)))
#             if file_object.is_dir():
#                 other_folders.append(file_object)
#         for i in other_folders:
#             normalize_all_tree_in(path)


def analisis_folder_contents(path,category_folders):   
    if path.is_dir():
        for file_object in path.iterdir():
            if file_object.is_dir():
                if file_object.name in FOLDERS_NAMES:
                    continue
                elif not any(file_object.iterdir()):
                    file_object.rmdir()
                else:
                    analisis_folder_contents(file_object,category_folders)
                    if not any(file_object.iterdir()):
                        file_object.rmdir()
                    else:
                        file_object.rename(file_object.with_name(normalize(file_object.name)))
            else:
                if file_object.suffix in IMAGES_EXT:
                    shutil.move(file_object,category_folders.get(FOLDERS_NAMES[0],path)  / normalize(file_object.name))
                    if not file_object.suffix in known_ext:
                        known_ext.append(file_object.suffix)
                elif file_object.suffix in VIDEO_EXT:
                    shutil.move(file_object, category_folders.get(FOLDERS_NAMES[3],path)/ normalize(file_object.name))
                    if not file_object.suffix in known_ext:
                        known_ext.append(file_object.suffix)
                elif file_object.suffix in MUSIC_EXT:
                    shutil.move(file_object, category_folders.get(FOLDERS_NAMES[2],path) / normalize(file_object.name))
                    if not file_object.suffix in known_ext:
                        known_ext.append(file_object.suffix)
                elif file_object.suffix in DOC_EXT:
                    shutil.move(file_object,category_folders.get(FOLDERS_NAMES[1],path) / normalize(file_object.name))
                    if not file_object.suffix in known_ext:
                        known_ext.append(file_object.suffix)
                elif file_object.suffix in ARCHIVES_EXT:
                    shutil.unpack_archive(file_object,category_folders.get(FOLDERS_NAMES[4]))
                    if not file_object.suffix in known_ext:
                        known_ext.append(file_object.suffix)
                    file_object.unlink()
                else:
                    if not file_object.suffix in unknown_ext:
                        unknown_ext.append(file_object.suffix)

def main():
    if len(sys.argv) <= 1:
        print('Sort was failed. No argument with path to folder')
    else:
        prepare_translate_dict()
        path = sys.argv[1]
        work_file = pathlib.Path(path)
        list_of_default_folders = create_default_folders(work_file)
        analisis_folder_contents(work_file, list_of_default_folders)
        for k, v in list_of_default_folders.items():
            num_files = len(list(v.glob('*')))
            print(f'{k} folder have {num_files} files')
        print(unknown_ext)
        print(known_ext)


#-----------------------------------------------------------
# Основна (main) частина
if __name__ == '__main__':
    main()

