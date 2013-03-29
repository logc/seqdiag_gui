from distutils.core import setup

setup(name='seqdiag_gui',
      version='0.1b1',
      description='A graphical user interface to the seqdiag package',
      author='Luis Osa',
      author_email='luis.osa.gdc@gmail.com',
      url='https://github.com/logc/seqdiag_gui',
      package_dir={'': 'src'},
      packages=['seqdiag_gui'],
      install_requires=[
          'seqdiag==0.8.2',
          ## 'wxPython==2.9.4.0',
      ],
      entry_points={
          'console_scripts': [
              'seqdiag_gui=seqdiag_gui.main:run',
          ]}
      )
