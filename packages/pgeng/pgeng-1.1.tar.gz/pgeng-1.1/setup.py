import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='pgeng',
	version='1.1',
	author='Qamynn',
	description='Useful functions and classes for PyGame',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/Qamynn/pgeng',
	license='MIT',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
	packages=['pgeng'],
	include_package_data=True,
	install_requires=['pygame>=2'],
	python_requires='>=3.6',
)
