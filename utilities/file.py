class FileUtility:
    @staticmethod
    def sanitize_filename(filename):
        new_filename = "".join(i for i in filename if i.isalnum())
        return new_filename

    @staticmethod
    def get_data_file_name(type, tone):
        file = f"{type}_{FileUtility.sanitize_filename(tone['style'])}.dat"
        return file
