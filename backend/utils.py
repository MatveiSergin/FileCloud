from app.settings.settings import settings


def get_unique_files(folder: list[dict[str:str]]) -> list[dict]:
    file_names = []
    unique_folder = []

    for file in folder:
        if file['Key'] not in file_names:
            file_names.append(file['Key'])
            unique_folder.append(file)

    return unique_folder

def get_path_without_domain(path: str, domain: str = settings.DOMAIN) -> str: #ftp://ru.com/files
    end_domain_ind = path.index(domain) + len(domain)
    return path[end_domain_ind:]
