from setuptools import setup


setup(
    name='mdn_mark',
    version='1.3.0',
    author='陈忠润',
    author_email='chenzhongrun@bonc.com.cn',
    description="""采集百度手机卫士 360手机卫士 搜狗号码通三个平台对手机号码的标注信息.
        1.1.0: 加入搜狗API采集方式，但与从网页采集结果是一致的。
        1.2.0：采用多线程，将不同源分开采集，避免互相影响。
        1.3.3：加入命令行工具，加入对IP的处理工具。""",
    packages=['get_mdn_mark'],
    # include_package_data=True,
    entry_points={
        'console_scripts': [
            'screen-ips=get_mdn_mark.proxies:screen_alive_proxies',
            'mdn-mark=get_mdn_mark.get_mdn_mark:threading_main'
        ]
    },
    install_requires=['zoran_tools>=0.2.1', 'requests_html']
)