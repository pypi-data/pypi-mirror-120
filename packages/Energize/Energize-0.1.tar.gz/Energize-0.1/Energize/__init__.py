from .energize import Energize


def extract_asar(asar_file, directory):
    with Energize.open(asar_file) as file:
        file.extract(directory)


def build_asar(directory, asar_file_name):
    with Energize.build_asar(directory) as folder:
        with open(asar_file_name, 'wb') as asar:
            folder.file_handle.seek(0)
            asar.write(folder.fp.read())
