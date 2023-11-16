import datetime
import logging
import os

from plugins.read_application import get_application_config, get_project_path


class Logger:
    _instance = None

    @staticmethod
    def get_instance():
        if Logger._instance is None:
            Logger._instance = Logger()
        return Logger._instance

    def __init__(self):
        if Logger._instance is not None:
            raise Exception("Logger is a singleton class. Use Logger.get_instance() to get the instance.")

        Logger._instance = self

        # 检索日志配置
        log_config = get_application_config().get("log")
        log_dir = log_config.get("path")
        # 如果日志文件目录不存在，则创建它
        os.makedirs(f"{get_project_path()}/{log_dir}", exist_ok=True)

        # 设置日志格式和日期格式
        log_format = log_config.get("format")
        date_format = "%Y-%m-%d %H:%M:%S"
        level = log_config.get("level")

        # 创建文件处理程序
        log_file = os.path.join(log_dir, f"{datetime.date.today()}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(log_format, date_format))

        # 创建控制台处理程序
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(log_format, date_format))

        # 创建记录器并设置其级别
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)

        # 将处理程序添加到记录器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message: str, case_name: str = ""):
        try:
            log_message = f"{case_name}-{message}" if case_name else message
            self.logger.debug(log_message)
        except Exception as e:
            print(f"日志记录失败，错误信息：{e}")

    def info(self, message: str, case_name: str = ""):
        log_message = f"{case_name}-{message}" if case_name else message
        self.logger.info(log_message)

    def warning(self, message: str, case_name: str = ""):
        log_message = f"{case_name}-{message}" if case_name else message
        self.logger.warning(log_message)

    def error(self, message: str, case_name: str = ""):
        log_message = f"{case_name}-{message}" if case_name else message
        self.logger.error(log_message)


logger = Logger.get_instance()
