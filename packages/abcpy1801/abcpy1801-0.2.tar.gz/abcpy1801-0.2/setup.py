from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()



setup(name='abcpy1801',
      version='0.2',
      description='A sudo Package',
      long_description=readme(),
      long_description_content_type='text/x-rst;',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='automl',
      url='http://github.com/jonh-doe',
      author='Rute Souza',
      author_email='rute.s.abreu@gmail.com',
      license=['MIT'],
      packages=['abcpy1801'],
      install_requires=[
          'numpy',
      ],
      include_package_data=True,
      zip_safe=False)