# Web UI 项目

## 概览

本项目设计用于对 Web 应用程序进行端到端测试。它使用 [Playwright](https://playwright.dev/)
进行浏览器自动化，使用 [pytest](https://docs.pytest.org/) 作为测试框架。

## 需求

需要 Python 3.7 或更高版本。必要的 Python 包列在 `requirements.txt` 文件中。你可以使用 pip 安装这些包：

```bash
pip install -r requirements.txt
```

## 结构

项目的主要目录和文件包括：

* `cases`：包含测试用例。
* `pages`：包含与页面相关的代码。
* `utils`：包含实用函数和类。
* `plugins`：包含自定义的 pytest 插件。
* `auth`：包含与用户认证相关的代码。
* `config`：包含配置文件。
* pytest.ini：pytest 配置文件。

## pytest 配置

pytest 配置文件位于 `pytest.ini` 文件中。它定义了测试报告的格式和输出目录。

```ini
[pytest]
addopts = --tracing=retain-on-failure
          --screenshot=only-on-failure
          --video=retain-on-failure
          --headed
```

#### 解释说明

```
tracing # 启用跟踪模式，    retain-on-failure 表示失败时保留跟踪
screenshot # 启用截图模式， only-on-failure 表示只在失败时截图
video # 启用视频模式，      retain-on-failure 表示失败时保留视频
headed # 启动GUI显示模式，不配置则默认不显示
```

## 运行测试

你可以通过执行 `run_tests.py` 脚本来运行测试：

```bash
python run_tests.py
```

该脚本会检查浏览器客户端是否已安装。如果没有安装，它会尝试安装。然后，它运行测试用例并生成报告。