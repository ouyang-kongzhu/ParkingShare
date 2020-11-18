import requests

from tools.util import FileUtil


class APIUtil:
    @classmethod
    def get_session(self):

        session = requests.session()
        url = FileUtil.get_ini_value('../conf/base.ini', 'api', 'url')
        url1 = FileUtil.get_ini_value('../conf/base.ini', 'api', 'url1')
        # data = eval(FileUtil.get_ini_value('..\\conf\\base.ini', 'api', 'data'))
        session.get(url1)
        session.get(url)



        return session

    @classmethod
    def request(self, method, url, data=None):
        session = self.get_session()
        req = getattr(session, method)(url, data)
        return req

    @classmethod
    def assert_api(cls, test_info):

        for info in test_info:
            resp = APIUtil.request(info['request_method'], info['uri'], info['params'])
            cls.assert_equal(resp.text, info['expect'])

    @classmethod
    def assert_equal(cls, expect, actual):
        if expect == actual:
            test_result = 'test-pass'
        else:
            test_result = 'test-fail'
        print(test_result)

if __name__ == '__main__':
    test_info = FileUtil.get_test_info('..\\conf\\test_info.ini', 'api_lessor', 'lessor_api')
    APIUtil.assert_api(test_info)
    # url='http://172.16.13.142:8080/SharedParkingPlace/admin/auditsManagement/parkinginformation/'
    # resp = APIUtil.request('post',url,{'parkingnumber': '3', 'parkingstatus': '1', 'uid': '6ade98f4-a14c-4bf0-a993-8ca936030245', 'parkingsizeid': '1', 'locationid': '5006', 'detailslocation': '阿萨'} )
    # print(resp.text)
