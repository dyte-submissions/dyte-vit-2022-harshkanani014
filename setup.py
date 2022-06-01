from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()

long_description = 'Command Line Interface (CLI) Tool to check version of dependency present in repositories file uploaded by user. \
    Dyte CLI tool provides features to check satisfied version and return output.csv with all satisfied version and also creates \
        Pull request to update particular version of dependency. Easy to use CLI tool with clean and clear output. \
            And support package.json of nodeJS and requirements.txt of python.'

setup(
		name ='Dyte Dependency version checker',
		version ='1.0.4',
		author ='Harsh Kanani',
		author_email ='harshkanani@gmail.com',
		url ='https://github.com/dyte-submissions/dyte-vit-2022-harshkanani014',
		description ='Demo Package for Dependency version checker for nodeJS and Python.',
		long_description = long_description,
		long_description_content_type ="text/markdown",
		license ='MIT',
		packages = find_packages(),
		entry_points ={
			'console_scripts': [
				'dyte = dyte_cli_package.dyte:messages'
			]
		},
		classifiers =(
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
		),
		keywords ='python package by Harsh Kanani',
		install_requires = requirements,
		zip_safe = False
)
