from distutils.core import setup

long_description = """
 Let's to convert Google Like Query Language into ElasticSearch understandable Query DSL
 """

setup(name='django_gapps_oauth2_login',
      version='0.9.7.3',
      description='Django Google Apps Oauth2 Login',
      long_description=long_description,
      url='https://github.com/Aplopio/plasticparser',
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
      ],
      keywords=["elasticsearch ", "query language", "query parser"],
      packages=['plasticparser'],
      install_requires=['pyparsing==2.0.2', 'mock==1.0.1'],
)
