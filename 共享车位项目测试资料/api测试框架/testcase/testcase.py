from  tools.util import FileUtil
from  tools.lib_util import APIUtil

class TestSalesAPI:
    def test_lessor(self):
        test_info = FileUtil.get_test_info('..\\conf\\test_info.ini', 'api_lessor', 'lessor_api')
        APIUtil.assert_api(test_info)

if __name__ == '__main__':

    TestSalesAPI().test_lessor()