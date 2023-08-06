from setuptools import setup, find_packages

with open('requirements.txt',  'r') as f:
    requirements = f.read().splitlines()


with open('README.md', encoding='utf-8') as f:
    readme = f.read()

# speedups for aiohttp
extras_require = {
    'speedups': 'aiohttp[speedups]',
}

setup(
    name='discord-sdk',
    author='moanie',
    python_requires='>=3.7.0',
    url='https://github.com/moanie/discord-sdk',
    version="0.1.2a",
    packages=find_packages(),
    license='MIT',
    description='An asynchronous Discord library for python.',
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)