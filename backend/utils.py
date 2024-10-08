from app.settings.settings import settings


def get_unique_files(folder: list[dict[str:str]]) -> list[dict]:
    file_names = []
    unique_folder = []

    for file in folder:
        if file['Key'] not in file_names:
            file_names.append(file['Key'])
            unique_folder.append(file)

    return unique_folder

def has_substring_in_strings(sub_string: str, strings: list):
    for string in strings:
        if sub_string in string:
            return True
    return False