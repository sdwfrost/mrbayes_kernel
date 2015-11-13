from distutils.command.install import install
from distutils.core import setup
from distutils import log
import sys
import os
import json

kernel_json = {
    "argv": [sys.executable,
             "-m", "mrbayes_kernel",
             "-f", "{connection_file}"],
    "display_name": "MrBayes",
    "language": "mrbayes",
    "name": "mrbayes_kernel",
}


class install_with_kernelspec(install):

    def run(self):
        install.run(self)
        user = '--user' in sys.argv
        try:
            from ipykernel.kerspec import install_kernel_spec
        except ImportError:
            from IPython.kernel.kernelspec import install_kernel_spec
        from IPython.utils.tempdir import TemporaryDirectory
        with TemporaryDirectory() as td:
            os.chmod(td, 0o755)  # Starts off as 700, not user readable
            with open(os.path.join(td, 'kernel.json'), 'w') as f:
                json.dump(kernel_json, f, sort_keys=True)
            log.info('Installing kernel spec')
            kernel_name = kernel_json['name']
            try:
                install_kernel_spec(td, kernel_name, user=user,
                                    replace=True)
            except:
                install_kernel_spec(td, kernel_name, user=not user,
                                    replace=True)


svem_flag = '--single-version-externally-managed'
if svem_flag in sys.argv:
    # Die, setuptools, die.
    sys.argv.remove(svem_flag)

with open('mrbayes_kernel.py', 'rb') as fid:
    for line in fid:
        line = line.decode('utf-8')
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break

setup(name='mrbayes_kernel',
      version=version,
      description='An MrBayes kernel for Jupyter/IPython',
      long_description=open('README.rst', 'r').read(),
      url="https://github.com/sdwfrost/mrbayes_kernel",
      author='Simon Frost',
      author_email='sdwfrost@gmail.com',
      license='MIT',
      py_modules=['mrbayes_kernel'],
      cmdclass={'install': install_with_kernelspec},
      install_requires=["metakernel >= 0.10.5", "IPython >= 3.0"],
      classifiers=[
          'Framework :: IPython',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 2',
          'Topic :: System :: Shells',
      ]
      )
