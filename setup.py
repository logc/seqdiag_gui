from distutils.core import setup

setup(name='seqdiag_gui',
      version='0.1a1',
      description='',
      author='Luis Osa',
      author_email='luis.osa.gdc@gmail.com',
      url='https://github.com/logc/seqdiag_gui',
      package_dir = {'': 'src'},
      packages=['seqdiag_gui'],
      install_requires=[
          'seqdiag',
          ],
      entry_points={
          'console_scripts':[
              'run=seqdiag_gui.main:run',
              ]
          }
          
      )
