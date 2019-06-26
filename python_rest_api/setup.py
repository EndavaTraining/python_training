from setuptools import setup

test_requirements = [
    'pytest',
    'coverage',
    'pytest-cov'
]

setup(name='python_rest_api',
      version='1.0.0',
      description='Python Rest API',
      author='Darius Darida',
      author_email='darius.darida@endava.com',
      url='https://github.com/EndavaTraining/python_training.git',
      packages=['order_api', 'product_api', 'user_api'],
      extras_require={'test': test_requirements},
      install_requires=['Flask']
      )
