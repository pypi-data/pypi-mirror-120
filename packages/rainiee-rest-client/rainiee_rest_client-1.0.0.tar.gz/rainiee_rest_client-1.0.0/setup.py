import setuptools
import os
path = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(path, 'README.md'),encoding='utf8') as f:
        long_description = f.read()
except Exception as e:
    long_description = "rainiee_rest_client"

setuptools.setup(
    name="rainiee_rest_client",
    version="1.0.0",
    author="rainiee",
    author_email="rainiee@163.com",
    description="rainiee rest api client",
    long_description = long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Rainiee-Technology",
    license='MIT',
    zip_safe=False,
    packages=setuptools.find_packages(),
    python_requires='>=3',
)