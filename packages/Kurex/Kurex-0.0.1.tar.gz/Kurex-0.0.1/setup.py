from setuptools import setup

def readme():
    with open('READMe.md') as f:
        return f.read()

setup(name='Kurex',
      version='0.0.1',
      description='test package bottom text.',
      long_description=readme(),
      long_descripttion_content_type='text/markdown',
      classifiers=[
          'Development Status :: 1 - Planning',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent'
      ],

      url='https://github.com/Sai-AungKhant/',
      author='SaiAungKhant',
      author_email='saiaungkhantthu60@gmail.com',
      keywords='core package',
      license='MIT',
      packages=['Kurex'],
      install_requires=[],
      include_package_data=True,
      zip_safe=False)