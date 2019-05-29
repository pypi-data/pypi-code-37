import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fanolabsaccobot",
    version="0.0.9",
    author="Henry Zheng",
    author_email="henry.zheng@fano.ai",
    description="FanoLabs Accobot module for Python3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.fanoai.cn/SDKs/accobot-python",
    packages=setuptools.find_packages('src'),
    package_dir = {'':'src'},
    license='LICENSE',
)