import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ruteni",
    version="0.4.0",
    author="Johnny Accot",
    description="Thin layer over Starlette",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    py_modules=["ruteni"],
    install_requires=[
        "aiodns",
        "aioredis",
        "aiosmtplib",
        "aiosmtpd",
        "anyio",
        "apscheduler",
        "authlib",
        "babel",
        "bcrypt",
        "databases",
        "httpx",
        "itsdangerous",
        "jinja2",
        "jwcrypto",
        "limits",
        "python-multipart",
        "paramiko",
        "python-socketio",
        "sqlalchemy",
        "sqlalchemy-utils",
        "starlette",
        "transitions",
        "websockets",
        "zxcvbn",
    ],
    test_suite="tests.my_module_suite",
)
