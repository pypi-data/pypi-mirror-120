from setuptools import setup, find_packages
 
classifiers = []
 
setup(
	name='pypiapijson',
	version='2.2',
	description='A client for connect to pypi.org api to retrieve the python packages!',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	url='https://github.com/dumb-stuff/pypiapijson',  
	author='Rukchad Wongprayoon',
	author_email='mooping3roblox@gmail.com',
	license='MIT', 
	classifiers=classifiers,
	keywords='Tools', 
	packages=find_packages(),
	install_requires=["aiohttp"],
	project_urls={
		"Documentation":"https://pypiapijson.biomooping.tk"
	}
)
