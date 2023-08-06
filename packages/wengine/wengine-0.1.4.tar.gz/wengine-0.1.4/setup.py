from setuptools import setup, find_packages


setup(
    name='wengine',
    version='0.1.4',
    install_requires=['whikoperator',
                      'weighting_platform',
                      'qodex_skud_bus',
                      'gravityRecorder',
                      'ghik_frame',
                      'weightsplitter',
                      'wsqluse'],
    packages=find_packages(),
    url='',
    license='',
    author='Arthur',
    author_email='ksmdrmvstchny@gmail.com',
    description='WEngine - оператор работы с weighing_platform'

)
