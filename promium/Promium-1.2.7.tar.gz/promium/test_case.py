import os
import pytest
import logging
import threading
import requests
import traceback

from urllib.parse import urlsplit

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.opera.options import Options as OperaOptions
from selenium.webdriver.remote.remote_connection import RemoteConnection

from promium.assertions import (
    WebDriverSoftAssertion,
    RequestSoftAssertion
)
from promium.exceptions import PromiumException
from promium.device_config import CHROME_DESKTOP_1920_1080
from promium.logger import (
    request_logging,
    logger_for_loading_page
)
from promium.common import upload_screenshot


FREEZE_TEST_STATE = os.environ.get('FREEZE_TEST_STATE')

log = logging.getLogger(__name__)

DRIVERS = {
    'firefox': 'Firefox',
    'chrome': 'Chrome',
    'safari': 'Safari',
    'opera': 'Opera',
    'ie': 'Ie',
}

MAX_LOAD_TIME = 10

DOWNLOAD_PATH = "/tmp"


def is_freeze():
    return True if FREEZE_TEST_STATE in ("true", "t", "True", "1") else False


def get_chrome_opera_options(options, device, is_headless=False):
    if is_headless:
        options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--no-first-run")
    options.add_argument("--verbose")
    options.add_argument("--enable-logging --v=1")
    options.add_argument("--test-type")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-gpu")
    options.add_argument(f"--window-size={device.width},{device.height}")
    prefs = {
        "download.default_directory": DOWNLOAD_PATH,
        "download.directory_upgrade": True,
        'prompt_for_download': False
    }
    options.add_experimental_option("prefs", prefs)
    if device.user_agent:
        options.add_argument(f"--user-agent={device.user_agent}")
        if device.device_name:
            mobile_emulation = {"deviceName": device.device_name}
            options.add_experimental_option(
                "mobileEmulation", mobile_emulation
            )
    return options


def get_chrome_options(device, proxy_server=None, is_headless=False):
    options = ChromeOptions()
    chrome_options = get_chrome_opera_options(
        options, device, proxy_server, is_headless
    )
    return chrome_options


def get_opera_options(device, proxy_server=None):
    options = OperaOptions()
    opera_options = get_chrome_opera_options(options, device, proxy_server)
    opera_options.add_extension("/work/uaprom/res/WebSigner_v1.0.8.crx")
    opera_options.binary_location = '/usr/bin/opera'
    return opera_options


def get_firefox_profile(device):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.startup.homepage", "about:blank")
    profile.set_preference("startup.homepage_welcome_url", "about:blank")
    profile.set_preference(
        "startup.homepage_welcome_url.additional", "about:blank"
    )
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", DOWNLOAD_PATH)
    profile.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        "application/zip"
    )
    profile.set_preference("pdfjs.disabled", True)

    FIREBUG_PATH = os.environ.get("FIREBUG_PATH")
    if FIREBUG_PATH and os.path.exists(FIREBUG_PATH):
        profile.add_extension(FIREBUG_PATH)
        profile.set_preference("extensions.firebug.allPagesActivation", "on")
        profile.set_preference("extensions.firebug.console.enableSites", "on")
        profile.set_preference(
            "extensions.firebug.defaultPanelName", "console"
        )
        profile.set_preference(
            "extensions.firebug.console.defaultPersist", "true"
        )
        profile.set_preference(
            "extensions.firebug.consoleFilterTypes", "error"
        )
        profile.set_preference("extensions.firebug.showFirstRunPage", False)
        profile.set_preference("extensions.firebug.cookies.enableSites", True)
    if device.user_agent:
        profile.set_preference("general.useragent.override", device.user_agent)
    profile.update_preferences()
    return profile


def get_firefox_options(device):
    """Function available if selenium version > 2.53.0"""
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("-no-remote")
    firefox_options.add_argument(f"-width {device.width}")
    firefox_options.add_argument(f"-height {device.height}")
    return firefox_options


def create_driver(device, proxy_server=None, env_var='SE_DRIVER', default=None):
    """
    Examples:

        - 'chrome://'
        - 'firefox://'
        - 'opera://'
        - 'http+chrome://host:port/wd/hub'

    """
    is_headless = True if os.environ.get("HEADLESS") == "Enabled" else False
    browser_profile = None
    certs = {
        'acceptSslCerts': True,
        'acceptInsecureCerts': True
    }

    driver_dsn = os.environ.get(env_var) or default
    if not driver_dsn:
        raise RuntimeError(f'Selenium WebDriver is not set in the {env_var} '
                           f'environment variable')

    try:
        scheme, netloc, url, _, _ = urlsplit(driver_dsn)
    except ValueError:
        raise ValueError(f'Invalid url: {driver_dsn}')

    if scheme in DRIVERS:
        if scheme == "chrome":
            chrome_options = get_chrome_options(
                device, proxy_server, is_headless
            )
            return webdriver.Chrome(
                chrome_options=chrome_options,
                desired_capabilities=certs if is_headless else None
            )
        elif scheme == "firefox":
            return webdriver.Firefox(
                firefox_profile=get_firefox_profile(device),
                firefox_options=get_firefox_options(device)
            )
        elif scheme == "opera":
            return webdriver.Opera(options=get_opera_options(device))
        return getattr(webdriver, DRIVERS[scheme])()
    elif scheme.startswith('http+'):
        proto, _, client = scheme.partition('+')
        if not netloc:
            raise ValueError(f'Network address is not specified: {driver_dsn}')

        capabilities = getattr(DesiredCapabilities, client.upper(), None)
        capabilities["loggingPrefs"] = {
            "performance": "ALL", "server": "ALL", "client": "ALL",
            "driver": "ALL", "browser": "ALL"
        }
        if capabilities is None:
            raise ValueError(f'Unknown client specified: {client}')

        remote_url = f'{proto}://{netloc}{url}'
        command_executor = RemoteConnection(
            remote_url, keep_alive=False, resolve_ip=False
        )
        if client == "chrome":
            chrome_options = get_chrome_options(
                device, proxy_server, is_headless
            )
            chrome_options.add_argument("--disable-dev-shm-usage")
            capabilities.update(chrome_options.to_capabilities())
            if is_headless:
                capabilities.update(certs)
        elif client == "firefox":
            capabilities.update(get_firefox_options(device).to_capabilities())
            browser_profile = get_firefox_profile(device)
        elif client == "opera":
            capabilities.update(get_opera_options(device).to_capabilities())
            capabilities["browserName"] = "opera"
        try:
            driver = webdriver.Remote(
                command_executor=command_executor,
                desired_capabilities=capabilities,
                browser_profile=browser_profile
            )
        except WebDriverException:
            log.warning("[SETUP] Second attempt for remote driver connection.")
            driver = webdriver.Remote(
                command_executor=command_executor,
                desired_capabilities=capabilities,
                browser_profile=browser_profile
            )
        return driver

    raise ValueError(f'Unknown driver specified: {driver_dsn}')


class TDPException(Exception):

    def __init__(self, *args):
        self.message = (
            "exception caught during execution test data preparing.\n"
            "Look at the original traceback:\n\n%s\n"
        ) % ("".join(traceback.format_exception(*args)))

    def __str__(self):
        return self.message


class TDPHandler:
    """
    TDP - Test Data Preparation
    context manager for handling any exception
    during execution test data preparing.
    We need to raise a specific custom exceptions.
    :example:
    with self.tdp_handler():
        some code
    """

    def __init__(self):
        pass

    def __enter__(self):
        log.info("[TDP] Start test data preparing...")
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        log.info("[TDP] Finish test data preparing")
        if exc_type:
            raise TDPException(exc_type, exc_value, exc_tb)
        return


class TestCase(object):
    test_case_url = None
    assertion_errors = None

    def tdp_handler(self):
        """
        Use this context manager for prepare of test data only,
        not for business logic!
        """
        return TDPHandler()


class WebDriverTestCase(TestCase, WebDriverSoftAssertion):
    driver = None
    device = CHROME_DESKTOP_1920_1080  # default data
    excluded_browser_console_errors = []
    lock = threading.Lock()

    ALLOWED_HOSTS = []
    SKIPPED_HOSTS = []

    @logger_for_loading_page
    def get_url(self, url, cleanup=True):
        self.driver.get(url)
        if cleanup:
            try:
                self.driver.execute_script(
                    'localStorage.clear()'
                )
            except WebDriverException:
                pass
        return url

    def check_console_errors(self):

        if hasattr(self.driver, "console_errors"):
            if self.driver.console_errors:
                browser_console_errors = self.driver.console_errors
                if self.excluded_browser_console_errors:
                    try:
                        return list(map(
                            lambda x: x, filter(
                                lambda x: x if not filter(
                                    lambda e: (
                                        True if e["msg"] in x and e["comment"]
                                        else False
                                    ),
                                    self.excluded_browser_console_errors
                                ) else None, browser_console_errors
                            )
                        ))
                    except Exception as e:
                        raise PromiumException(
                            "Please check your excluded errors list. "
                            "Original exception is: %s" % e
                        )
                return browser_console_errors
        return []

    def setup_method(self, method):
        self.assertion_errors = []
        pytest.config.get_fail_debug = self.get_fail_debug
        pytest.config.assertion_errors = self.assertion_errors
        pytest.config.check_console_errors = self.check_console_errors
        pytest.config.get_screenshot_png = self.get_screenshot_png

        if hasattr(method, 'device'):
            self.device = method.device.args[0]

        try:
            self.driver = create_driver(
                self.device, proxy_server=None
            )
            self.driver.console_errors = []
        except WebDriverException as e:
            msg_exited_abnormally = (
                "failed to start: exited abnormally"
            )
            if msg_exited_abnormally in e.msg:
                pytest.xfail(msg_exited_abnormally)
            else:
                raise e

    def teardown_method(self, method):
        self.driver.console_errors = []
        if self.driver:
            self.driver.xrequestid = None
            try:
                self.driver.quit()
            except WebDriverException as e:
                log.error(
                    "[PROMIUM] Original webdriver exception: %s" % e
                )

    def get_screenshot_png(self):
        return self.driver.get_screenshot_as_png()

    def get_fail_debug(self):
        """Failed test report generator"""

        alerts = 0
        try:
            while self.driver.switch_to.alert:
                alert = self.driver.switch_to.alert
                print('Unexpected ALERT: %s\n' % alert.text)
                alerts += 1
                alert.dismiss()
        except Exception:
            if alerts != 0:
                print('')
            pass
        url = self.driver.current_url
        screenshot = upload_screenshot(self.driver)
        # node_id = get_grid_node_id(
        #     self.driver.session_id,
        #     self.driver.command_executor._url
        # )
        return (
            'webdriver',
            url,
            screenshot,
            # node_id,
        )


class RequestTestCase(RequestSoftAssertion):
    session = None
    proxies = {}

    def setup_method(self, method):
        self.session = requests.session()
        self.session.url = (
            'Use self.get_response(url) for request tests or '
            'util methods for api tests!'
        )
        self.assertion_errors = []
        pytest.config.assertion_errors = self.assertion_errors
        pytest.config.get_fail_debug = self.get_fail_debug

    def teardown_method(self, method):

        if self.session:
            self.session.close()
    
    def get_fail_debug(self):
        if not hasattr(self.session, 'status_code'):
            self.session.status_code = None

        """Failed test report generator"""
        return (
            'request',
            self.session.status_code,
        )

    def get_response(self, url, method="GET", timeout=10, **kwargs):
        self.session.url = url
        self.session.status_code = None
        response = self.session.request(
            method=method,
            url=url,
            timeout=timeout,
            verify=False,
            hooks=dict(response=request_logging),
            **kwargs,
        )
        self.session.status_code = response.status_code
        return response
