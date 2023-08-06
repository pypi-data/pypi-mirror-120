import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name="knarrow",
    version="0.0.1",
    author="Marijan Smetko",
    author_email="msmetko@msmetko.xyz",
    description="TODO",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/InCogNiTo124/knarrow',
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires='>=3.0',
)
