Utility to create an environment.yml file from imports.

Example:

        $ environment_extractor --dir C:\Users\user\Documents\project --ignored_libs "twine lightgbm" --name new_env --channels "pytorch defaults" --extra_libs "fiona geopandas"

Installation:

	$ git clone https://github.com/Joshua-Brooke/Environment_extractor
	$ cd environment_extractor
	$ pip install .
	or
	$ pip install environment_extractor
