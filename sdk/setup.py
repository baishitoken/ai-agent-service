from setuptools import setup, find_packages

setup(
    name='AI-Agent-SDK',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'flask',
        'pydantic',
        'flask_cors',
        'python-dotenv'
    ],
    author='Your Name',
    description='SDK for AI-Agent service',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
