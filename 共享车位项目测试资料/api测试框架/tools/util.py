import configparser
import os
import time

class TimeUtil:
    @classmethod
    def get_filename_time(cls):
        """
           返回用于文件名格式的时间字符串
       :param :

       :return:
           时间字符串格式为%Y%m%d_%H%M%S
       """
        return time.strftime('%Y%m%d_%H%M%S', time.localtime())

    @classmethod
    def get_standard_format_time(cls):
        """
        获取当前系统时间，返回标准格式时间
        :return: 返回的时间格式为%Y-%m-%d %H:%M:%S
        """

        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

class LogUtil:

    logger = None

    @classmethod
    def get_logger(cls, name):
        """
            返回规定格式的日志生成器对象
        :param name:
            调用logger的模块名
        :return:
            日志生成器对象
        """
        import logging
        if cls.logger is None:
            # 获取日志生成器对象
            cls.logger = logging.getLogger(name)
            # 定义获取信息的级别
            cls.logger.setLevel(level=logging.INFO)
            # 如果日志目录不存在则创建
            if not os.path.exists('..\\logs'):
                os.mkdir('..\\logs')
            # 创建logger的文件句柄与规定的文件关联
            handler = logging.FileHandler(
                '..\\logs\\' + TimeUtil.get_filename_time() + '.log', encoding='utf8')
            # 定义信息的格式
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            cls.logger.addHandler(handler)
            cls.logger.info(
                '*****************************************************\n')

        return cls.logger

class FileUtil:
    logger = LogUtil.get_logger(os.path.join(os.getcwd(), 'util'))
    @classmethod
    def get_ini_value(cls, path, section, option):
        """
        从ini配置文件中读取某个指定的键对应的值并返回
        :param path:配置文件路径
        :param section:节点名称
        :param option:键的名称
        :return:对应的单值
        """
        import configparser
        cp = configparser.RawConfigParser()
        value = None
        try:
            cp.read(path, encoding='utf-8')
            value = cp.get(section, option)
        except BaseException:
            cls.logger.error('读取配置文件错误')
        return value

    @classmethod
    def get_test_info(cls, path, section, option):
        """
        从test_info.ini读取excel配置信息，将excel内容全部读出
        :param path:测试信息配置文件路径及文件名
        :param section: 页面名称
        :param option: 每条测试信息的键
        :return: 测试信息的json格式
        """
        params = eval(cls.get_ini_value(path, section, option))
        import xlrd

        workbook = xlrd.open_workbook(params['test_info_path'])
        sheet_content = workbook.sheet_by_name(params['sheet_name'])
        case_sheet_content = workbook.sheet_by_name(params['case_sheet_name'])
        version = case_sheet_content.cell(1, 1).value
        test_data = []

        for i in range(params['start_row'], params['end_row']):
            data = sheet_content.cell(i, params['test_data_col']).value
            expect = sheet_content.cell(i, params['expect_col']).value
            temp = str(data).split('\n')
            di = {}
            request_params = {}  # 用于保存发送接口传递的参数
            for t in temp:
                request_params[t.split('=')[0]] = t.split('=')[1]
            di['params'] = request_params
            di['expect'] = expect
            di['caseid'] = sheet_content.cell(i, params['caseid_col']).value
            di['module'] = sheet_content.cell(i, params['module_col']).value
            di['type'] = sheet_content.cell(i, params['type_col']).value
            di['desc'] = sheet_content.cell(i, params['desc_col']).value
            di['version'] = version
            di['uri'] = sheet_content.cell(i, params['uri']).value
            di['request_method'] = sheet_content.cell(i, params['request_method']).value
            test_data.append(di)
        test_data1=tuple(test_data)
        return test_data1


if __name__ == '__main__':
    test_info = FileUtil.get_test_info('..\\conf\\test_info.ini', 'api_lessor', 'lessor_api')
    print(test_info)



