import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

DEV_REQUIREMENTS = [
    'coveralls == 3.*',
    'flake8',
    'pytest == 6.*',
    'pytest-cov == 2.*',
]

setuptools.setup(
    name='dad-tool',
    version='0.1.7',
    description='Dummy Address Data (DAD) - Real addresses from all around the world.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/Justintime50/dad-python',
    author='Justintime50',
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    extras_require={
        'dev': DEV_REQUIREMENTS,
    },
    # TODO: Is there a way we can specify the single `src` dir instead of each individually?
    package_data={
        'dad_tool': [
            'dad/src/addresses/australia/*.json',
            'dad/src/addresses/canada/*.json',
            'dad/src/addresses/china/*.json',
            'dad/src/addresses/europe/*.json',
            'dad/src/addresses/mexico/*.json',
            'dad/src/addresses/united-states/*.json',
            'dad/src/other/*.json',
        ],
    },
    python_requires='>=3.7',
)
