import os

import yaml

cases_path = "data/cases/login.yaml"


class ReadCases:

    def __init__(self, case_path):
        self.cases_path = case_path

    def read_yaml(self):
        project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(f"{project_path}/{self.cases_path}", 'r', encoding='utf-8') as f:
            cases = yaml.load(f, Loader=yaml.FullLoader)
        return cases


if __name__ == '__main__':
    readCases = ReadCases(case_path='/data/cases/数据资源浏览器/case.yaml')
    aa = readCases.read_yaml()
    print(aa)
