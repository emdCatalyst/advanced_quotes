import setuptools

with open('README.md', 'r') as readme:
  long_description = readme.read()

with open('requirements.txt', 'r') as requirements_file:
  requirements_text = requirements_file.read()

requirements = requirements_text.split()

setuptools.setup(
      name='advanced_quotes',
      version='1.0',
      description='Your all-access pass to the world\'s largest quotations database. Random , daily quotes , over 40 thousand authors, various topics. Inside your comfy python development environment!',
      url='https://github.com/Mahdios/advanced_quotes',
      author='Mahdi Djaber',
      author_email='mahdios.dj@gmail.com',
      license='GPL-3.0',
      packages=setuptools.find_packages(),
      zip_safe=False,
      long_description_content_type="text/markdown",
      long_description=long_description,
      install_requires=['bs4','requests']
)
