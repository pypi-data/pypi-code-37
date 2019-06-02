from setuptools import setup, find_packages

setup(
    name="webviewhooks",
    version="0.0.3",
    description="get webView html DOM tree",
    author="looper",
    author_email="looperchu2018@gmail.com",
    zip_safe=False,
    license='MIT',
    install_requires=['frida==12.5.5', 'frida-tools==2.0.0', ],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)