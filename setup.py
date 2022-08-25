from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='chemlib',
    version='2.2.4',
    description='An easy-to-use library that quickly performs chemistry calculations.',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    include_package_data=True,
    packages=find_packages(),
    author='Hari Ambethkar',
    author_email='harirakul.a@gmail.com',
    keywords=['Chemistry', 'Chemlib'],
    url='https://github.com/harirakul/chemlib',
    download_url='https://pypi.org/project/chemlib/'
)

required = [
    'numpy',
    'sympy',
    'pandas',
    'Pillow'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=required)