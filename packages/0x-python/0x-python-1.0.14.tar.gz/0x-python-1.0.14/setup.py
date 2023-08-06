import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="0x-python",
    version="1.0.14",
    author="Skeetzo",
    author_email="WebmasterSkeetzo@gmail.com",
    url = 'https://github.com/skeetzo/0x-python',
    keywords = ['0x','api','python'],
    description="0x python wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=['tests']), # Include all the python modules except `tests`.
    include_package_data=True,
    install_requires=[
            "requests"
        ],
    entry_points={
        'console_scripts' : [
            'ZeroEx = ZeroEx.ZeroEx:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Operating System :: POSIX :: Linux",
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)