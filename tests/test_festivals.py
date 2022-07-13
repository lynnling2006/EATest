# test file for checking festivals api 

import requests
import pytest
import pdb
from pytest_schema import schema
from utils import config
import data.model_schema as model_schema
import logging


logger = logging.getLogger()

class TestFestivals(object):

    def test_success_status_and_elapse_time(self):
        """ Check status code """        
        rsp = requests.request("GET", url=config.festivals_url)

        logger.info(f"status code:{rsp.status_code}")
        logger.info(f"call case {rsp.elapsed}")
        
        # status code 200 expected
        assert rsp.status_code == 200, f"unexpected status code returned {rsp.status_code}"

        # elapsed time should less than specified threshod
        assert float(rsp.elapsed.total_seconds()) <= float(config.threshold_elapsed), \
            f"response is slow, it took {rsp.elapsed.total_seconds()}s!"

    @pytest.mark.parametrize('accept_type', ['text/plain', 'application/json', 'text/json', ''])
    def test_response_content_type(self, accept_type):

        headers = {'accept': accept_type} if accept_type != '' else {}
        expect_type = accept_type if accept_type != '' else 'application/json'

        rsp = requests.request("GET", url=config.festivals_url, headers=headers)
        content_type = rsp.headers['content-type'].split(';')[0].strip()

        logger.info(f"\ncontent-type:{content_type}")

        if rsp.status_code == 200:
            assert content_type == expect_type, \
                f"response content_type:{content_type} different with accept_type:{expect_type}!"
        else:
            pytest.skip(f"test skipped since status code is {rsp.status_code}!")

    def test_throttle(self):
        """ Check throttle if more than n request sent """
        def multiple_request(n):
            for i in range(n):
                rsp = requests.request("GET", url=config.festivals_url)
                logger.info(f"request {i} took {rsp.elapsed}")
                exp_status = 200 if i < n-1 else 429
                if rsp.status_code == 429:
                    content_type = rsp.headers['content-type'].split(';')[0].strip()
                    exp_msg = "Too many requests, throttling"
                    assert rsp.content.decode('utf-8') == exp_msg, "throttle msg not as expected!"
                    assert content_type == 'text/html', \
                        "content_type not as expected in throttling response"

                assert rsp.status_code == exp_status, \
                    f"request {i+1} failed before reach threshold!"

        multiple_request(int(config.threshold_throttle))

    def test_response_header(self):
        """Check response header """
        rsp = requests.request("GET", url=config.festivals_url)
        headers = rsp.headers
        logger.info(f"response headers: {headers}")
        exp_headers = {
            "connection": "keep-alive",
            "Content-Encoding": "Gzip",
            "Content-Type": "application/json; charset=utf-8",
            "Server": "nginx",
            "Vary": "Accept-Encoding",
            "X-Frame-Options": "DENY",
            "X-Powered-By": "Express",
            "Set-Cookie": ""
        }

        for k, v in exp_headers.items():
            if k in headers.keys():
                if k == "Set-Cookie":
                    # only check Set-Cookie is presented
                    assert headers[k] is not None, f"{k} is empty!"
                else:
                    assert headers[k].upper() == v.upper(), f"{k} is not as expected in headers" 
            else:
                # raise error if expected key not returned in headers
                raise Exception(f"{k} is not presented in headers")

    def test_schema_and_data(self):
        """Verify schema and then check details of returned data"""

        rsp = requests.request("GET", url=config.festivals_url)

        logger.info(f"\n content: {rsp.content}")

        if rsp.status_code == 200:
            festivals = rsp.json()

            # verify response model, it should match the defined schema
            assert schema(model_schema.festivals) == festivals

            festival_list = []
            band_name_list = dict()
            band_record_list = dict()

            # if scheme check pass then verify data in response
            #  -- report error if empty data returned
            for music_festival in festivals:
                # check empty festival name
                festival_name = music_festival['name'].strip()
                festival_list.append(festival_name)
                
                # check duplicted and empty band names in same festiveal
                band_names_list = [b['name'] for b in music_festival['bands']]
                band_names_set = set(band_name_list)
                logger.info(f"\n band list: {band_names_list} for festival {festival_name}")

                assert len(band_name_list) == len(band_names_set), \
                    f"there are duplicated bands in festival {festival_name}"
                assert "" not in band_names_list, \
                    f"empty band name found for festival {festival_name}"

                # check empty band recordLabel in same festival
                # different band can have same reordLable
                band_record_list = [b['name'] for b in music_festival['bands'] \
                    if b['recordLabel'].strip() == '']
                logger.info(f"\n band list with empty recordLable: \
                    {band_record_list} for festival {festival_name}")
                assert len(band_record_list) > 0, \
                    f"empty band recordLabel found for following band {band_record_list}"

            print(festival_list)
            festival_set = set(festival_list)
            assert len(festival_list) == len(festival_set), \
                f"There are duplicated festival in response data!"
            assert "" not in festival_list, f"empty festival_name found!"
        else:
            pytest.skip(f"case skipped because return code is {rsp.status_code}!")
