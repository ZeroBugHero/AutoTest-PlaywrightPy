import os


class ReadData:
    """
    读取data文件,返回数据
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def read_yaml(self):
        import yaml
        project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = f"{project_path}/{self.file_path}"

        if not os.path.exists(file_path):  # 判断文件是否存在
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        with open(f"{project_path}/{self.file_path}", 'r', encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        return data


def get_user_info(self):
    data = self.read_yaml()
    return data.get('userinfo')


readData = ReadData('data/data.yaml')
print(readData.get_user_info())
