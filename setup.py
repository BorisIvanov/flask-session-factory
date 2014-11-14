from setuptools import setup


setup(
    name='flask-session-factory',
    version='0.1',
    url='https://github.com/BorisIvanov/flask-session-factory',
    license='MIT',
    author='Boris Ivanov',
    author_email='',
    maintainer='Boris Ivanov',
    maintainer_email='',
    description='Server-side sessions for Flask with SqlAlchemy',
    long_description=__doc__,
    py_modules=['flasksessionfactory'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.10.1',
        'SQLAlchemy>=0.9.8',
		'Flask-SQLAlchemy==2.0',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords="flask session sqlalchemy cookie cookieless"
)