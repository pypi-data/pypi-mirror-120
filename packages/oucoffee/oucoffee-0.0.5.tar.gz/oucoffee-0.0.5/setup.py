from setuptools import setup, find_packages

requirements = [
    'jupyter',
    'numpy',
    'matplotlib',
    'requests',
    'pandas'
]

setup(
    name='oucoffee',
    version='0.0.5',
    python_requires='>=3.6',
    author='Oucoffee Developers',
    author_email='282832606@qq.com',
    url='https://github.com/YiguoWang/oucoffee',
    description='Dive into Deep Learning',
    license='MIT-0',
    packages=find_packages(),
    zip_safe=True,
    install_requires=requirements,
)
