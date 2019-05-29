from setuptools import setup


setup(
    name='mdn_mark',
    version='1.0.1',
    author='陈忠润',
    author_email='chenzhongrun@bonc.com.cn',
    description='采集百度手机卫士 360手机卫士 搜狗号码通三个平台对手机号码的标注信息',
    packages=['get_mdn_mark'],
    # include_package_data=True,
    entry_points={
        'console_scripts': ['mdn-mark=get_mdn_mark.get_mdn_mark:main', ]
    },
    install_requires=['zoran_tools>=0.2.1', 'requests_html']
)