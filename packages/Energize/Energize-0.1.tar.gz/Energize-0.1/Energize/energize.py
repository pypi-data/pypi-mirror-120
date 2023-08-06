import os, io, json, struct, shutil


class Energize:

    """
        Class used to interact with Electron ASAR files.

        ...

        Attributes
        ----------
        path : str
            Path to ASAR file.
        file_handle : str
            Data that was read from ASAR file.
        header : str
            The JSON header data from the ASAR archive.
        offset : int
            The offset of the next file in the archive.

    """

    def __init__(self, path, file_handle, header, offset):
        self.file_handle = file_handle
        self.base_offset = offset
        self.header = header
        self.path = path

    @classmethod
    def open(cls, path):
        """
        Parameters
         ----------
        path : str
            The path to the desired ASAR file.
        """

        file_handle = open(path, 'rb')
        header_string_size = struct.unpack('<4I', file_handle.read(16))[3]
        header_json = file_handle.read(header_string_size).decode('utf-8')
        return cls(path=path, file_handle=file_handle, header=json.loads(header_json), offset=(16 + header_string_size + 4 - 1) & ~(4 - 1))

    @classmethod
    def build_asar(cls, path):
        """
        Parameters
        ----------
        path : str
            The folder you want the contents of the ASAR file to be extracted too.
        """

        offset = 0
        concatenated_files = b''

        def _path_to_dict(path):
            nonlocal concatenated_files, offset
            result = {'files': {}}

            for f in os.scandir(path):
                if os.path.isdir(f.path):
                    result['files'][f.name] = _path_to_dict(f.path)
                elif f.is_symlink():
                    result['files'][f.name] = {'link': os.path.realpath(f.name)}
                else:
                    size = f.stat().st_size

                    result['files'][f.name] = {'size': size, 'offset': str(offset)}

                    with open(f.path, 'rb') as file_handle:
                        concatenated_files += file_handle.read()

                    offset += size

            return result

        header = _path_to_dict(path)
        header_json = json.dumps(header, sort_keys=True, separators=(',', ':')).encode('utf-8')

        header_string_size = len(header_json)
        data_size = 4
        aligned_size = (header_string_size + data_size - 1) & ~(data_size - 1)
        header_size = aligned_size + 8
        header_object_size = aligned_size + data_size

        diff = aligned_size - header_string_size
        header_json = header_json + b'\0' * (diff) if diff else header_json

        file_handle = io.BytesIO()
        file_handle.write(struct.pack('<4I', data_size, header_size, header_object_size, header_string_size))
        file_handle.write(header_json)
        file_handle.write(concatenated_files)

        return cls(path=path, file_handle=file_handle, header=header, offset=(16 + header_string_size + 4 - 1) & ~(4 - 1))

    def _copy_unpacked_file(self, source, destination):
        """
        Parameters
        ----------
        source : str
            The location of the ASAR file.
        destination : str
            The destination of the extracted files.
        """
        unpacked_dir = self.path + '.unpacked'

        src = os.path.join(unpacked_dir, source)

        dest = os.path.join(destination, source)
        shutil.copyfile(src, dest)

    def _extract_file(self, source, info, destination):
        """
        Parameters
        ----------
        source : str
            The location of the ASAR file.
        info : str
            The info about the file packed in the ASAR archive. (offset, size in bytes)
        destination : str
            The destination of the extracted files.
        """
        if 'offset' not in info:
            self._copy_unpacked_file(source, destination)
            return

        self.file_handle.seek(self.base_offset + int(info['offset']))
        r = self.file_handle.read(int(info['size']))

        dest = os.path.join(destination, source)
        with open(dest, 'wb') as f:
            f.write(r)

    def _extract_asar(self, source, files, destination):
        """
        Parameters
        ----------
        source : str
            The location of the ASAR file.
        files : str
            The JSON header inside ASAR file, containing file information.
        destination : str
            The destination of the extracted files.
        """
        dest = os.path.normpath(os.path.join(destination, source))

        if not os.path.exists(dest):
            os.makedirs(dest)

        for name, info in files.items():
            item_path = os.path.join(source, name)

            if 'files' in info:
                self._extract_asar(item_path, info['files'], destination)
            else:
                self._extract_file(item_path, info, destination)

    def extract(self, path):
        self._extract_asar('.', self.header['files'], path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file_handle.close()
