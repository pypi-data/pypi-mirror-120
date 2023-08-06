import setuptools, os

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

requires = ["pandas>=1.0.1", "numpy>=1.19.0", "scipy>=1.5.4", "scikit-learn>=0.23.0", "imbalanced-learn>=0.8.0"]

setuptools.setup(
    name='gitlabds',
    version=version,
    description='Gitlab Data Science and Modeling Tools',
    author='Kevin Dietz',
    author_email='kdietz@gitlab.com',
    packages=setuptools.find_packages(),
    url='https://gitlab.com/gitlab-data/gitlabds',
    python_requires= '>=3.6',
    install_requires=requires,
)  
