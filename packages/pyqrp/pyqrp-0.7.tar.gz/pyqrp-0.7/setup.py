from setuptools import setup

with open("README.md", "r") as fh:
    long_desc = fh.read()

setup(
    name='pyqrp',
    version="0.7",
    packages=["pyqrp"],
    package_dir={'': "src"},
    scripts=['scripts/pyqrp'],
    author="George",
    author_email="drpresq@gmail.com",
    description="PYQRP: A Simple QRP File interpreter in Python",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/drpresq/pyqrp",
    install_requires=[
        "openpyxl",
        "xlrd",
        "pyautogui"
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.4'
        ]
    },
    keywords="",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities'
    ],
)
