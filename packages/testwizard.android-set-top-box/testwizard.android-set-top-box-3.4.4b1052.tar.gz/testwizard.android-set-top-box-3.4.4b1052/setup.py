import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testwizard.android-set-top-box",
    version="3.4.4b1052",
    author="Eurofins Digital Testing - Belgium",
    author_email="testwizard-support@eurofins-digitaltesting.com",
    description="Testwizard for Android set-top box testobjects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.eurofins-digitaltesting.com/testwizard/",
    packages=['testwizard.android_set_top_box'],
    install_requires=[
        'testwizard.test==3.4.4b1052',
        'testwizard.testobjects-core==3.4.4b1052',
        'testwizard.commands-audio==3.4.4b1052',
        'testwizard.commands-mobile==3.4.4b1052',
        'testwizard.commands-powerswitch==3.4.4b1052',
        'testwizard.commands-remotecontrol==3.4.4b1052',
        'testwizard.commands-video==3.4.4b1052'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
    ],
)













