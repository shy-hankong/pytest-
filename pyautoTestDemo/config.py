import os
PRO_PATH = os.path.dirname(os.path.abspath(__file__))


class RunConfig:
    """
    运行测试配置
    """
    # 运行测试用例的目录或文件
    cases_path = os.path.join(PRO_PATH, "./test_dir/")

    # 配置浏览器驱动类型(chrome/firefox/chrome-headless/firefox-headless)。
    driver_type = "chrome"

    # 浏览器驱动（不需要修改）
    driver = None

    # 失败重跑次数
    rerun = "3"

    # 当达到最大失败数，停止执行
    max_fail = "5"

