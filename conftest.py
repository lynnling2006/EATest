import sys
import os
import time

now = time.strftime('%Y%m%d_%H%M%S')
logfile_name=f'test_{now}.log'
report_name=f'test_report_{now}.html'

def pytest_configure(config):
    config.option.log_file = os.path.join(config.rootdir, 'log', logfile_name)
    config.option.htmlpath = os.path.join(config.rootdir, 'report', report_name)
    config.option.self_contained_html = True
