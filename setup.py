from setuptools import setup, find_packages

filepath = 'README.md'

setup(
    name='EVCode',
    version='1.2.0',
    author='lidongxun967',
    author_email='debug967@outlook.com',
    description='一个通过SMTP进行邮箱验证码发送的项目',
    long_description=open(filepath, encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
