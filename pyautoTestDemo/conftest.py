import pytest
import os
from selenium import webdriver
from py.xml import html
from config import RunConfig


# 项目目录配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = BASE_DIR + "/test_report/"

# 启动浏览器
@pytest.fixture(scope='session')
def browser():
    """
    全局定义浏览器驱动
    :return:
    """
    global driver
    if RunConfig.driver_type == "chrome":
        # 本地chrome浏览器
        driver = webdriver.Chrome()
        driver.maximize_window()
    else:
        raise NameError("driver驱动类型定义错误！")
    RunConfig.driver = driver

    yield driver

    driver.quit()
    print("test end!")

@pytest.mark.hookwrapper  # 当pytest运行一个测试用例时，它会调用这个钩子函数。
def pytest_runtest_makereport(item):
    """
    用于向测试用例中添加用例的开始时间、内部注释，和失败截图等.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')  # 获取pytest-html插件的实例。这个插件用于在HTML报告中添加额外的内容，如截图。
    outcome = yield  # 生成器被yield暂停，等待测试用例执行。当测试用例执行完成后，生成器会恢复，并且outcome会包含测试用例的结果。
    report = outcome.get_result()  # 从outcome中获取测试报告
    report.description = description_html(item.function.__doc__)  # 设置报告的描述为测试用例的文档字符串的HTML版本（通过description_html函数转换）
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):  # 如果测试用例是skipped（跳过）并且预期会失败（xfail），或者测试用例失败并且预期不会失败
            case_path = report.nodeid.replace("::", "_") + ".png"
            if "[" in case_path:
                case_name = case_path.split("-")[0] + "].png"  # 生成截图的文件名
            else:
                case_name = case_path
            capture_screenshots(case_name)# 调用capture_screenshots函数来捕获截图
            img_path = "image/" + case_name.split("/")[-1]
            if img_path:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % img_path
                extra.append(pytest_html.extras.html(html))  # 构造HTML代码来在报告中显示截图，将HTML代码添加到报告的extra字段中
        report.extra = extra  # 更新报告的extra字段，这样它就可以包含截图的HTML代码。

def description_html(desc):
    """
    将用例中的描述转成HTML对象
    :param desc: 描述
    :return:
    """
    if desc is None:
        return "No case description"
    desc_ = ""  # 遍历输入的描述 desc，将每个字符添加到 desc_ 字符串中。如果遇到一个换行符 \n，则使用分号 ; 替换它
    for i in range(len(desc)):
        if desc[i] == '\n':
            desc_ = desc_ + ";"
        else:
            desc_ = desc_ + desc[i] #这里处理所有字符，包括第一个字符

    desc_lines = desc_.split(";")  # 使用分号 ; 将 desc_ 分割成多个行，存储在 desc_lines 中
    desc_html = html.html(  # 使用 html 模块（假设这个模块已经被导入）来创建HTML结构
        html.head(
            html.meta(name="Content-Type", value="text/html; charset=latin1")),
        html.body(
            [html.p(line) for line in desc_lines]))
    return desc_html

def capture_screenshots(case_name):
    """
    配置用例失败截图路径
    :param case_name: 用例名
    :return:
    """
    global driver
    file_name = case_name.split("/")[-1]
    if RunConfig.NEW_REPORT is None:
        raise NameError('没有初始化测试报告目录')
    else:
        image_dir = os.path.join(RunConfig.NEW_REPORT, "image", file_name)
        if RunConfig.driver is not None:
            RunConfig.driver.save_screenshot(image_dir)
        else:
            print("警告sjy: RunConfig.driver 驱动是is None, 跳过skipping screenshot capture.")

# 设置用例描述表头
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.pop()
# 设置用例描述表格
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.pop()

