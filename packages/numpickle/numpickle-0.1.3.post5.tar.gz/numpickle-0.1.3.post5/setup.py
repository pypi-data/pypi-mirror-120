# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numpickle']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.5,<2.0.0', 'pandas>=0.24.2,<0.25.0']

setup_kwargs = {
    'name': 'numpickle',
    'version': '0.1.3.post5',
    'description': 'Faster loading of pandas data frames by saving them as numpy arrays and pickling their meta info (row+column names, column dtype info).',
    'long_description': '\n# numpickle\n\nFaster loading of pandas data frames by saving them as numpy arrays and pickling their meta info (row+column names, column dtype info).\n\nThe bigger the data frame, the bigger the gain of speed when reading compared to loading a text file.\n(E.g., a several GB RAM-consuming matrix took minutes to read-in using normal `pd.read_csv()`, but took only seconds to load when using `numpickle.load_numpickle()`).\n`all_numeric=True` accelerates loading by ~ 7 times.\n\nAlso mentioned in my [medium article](https://gwang-jin-kim.medium.com/faster-loading-and-saving-of-pandas-data-frames-using-numpickle-numpy-and-pickle-d15870519529).\n\n## Install\n\n```pip install numpickle```\n\n## Usage\n\n```\nimport pandas as pd\nimport numpickle as npl\n\n\n# create example data frame with non-numeric and numeric columns\ndf = pd.DataFrame([[1, 2,\'a\'], [3, 4, \'b\']])\ndf.columns = ["A", "B", "C"]\ndf.index = ["row1", "row2"]\n\ndf\n#       A  B  C\n# row1  1  2  a\n# row2  3  4  b\n\ndf.dtypes\n# A     int64\n# B     int64\n# C    object\n# dtype: object\n\n\n\n\n# save data frame as numpy array and pickle row and column names\n# into helper pickle file "/home/user/test.npy.pckl"\nnpl.save_numpickle(df, "/home/user/test.npy")\n\n# load the saved data\ndf_ = npl.load_numpickle("/home/user/test.npy")\n\ndf_\n#       A  B  C\n# row1  1  2  a\n# row2  3  4  b\n\n\ndf_.dtypes\n# A     int64\n# B     int64\n# C    object\n# dtype: object\n\nall(df == df_)\n# True\n\n\n\n\n\n\n####################################\n# data frames with numeric-only values\n###################################\n\n# If you have a data frame with only numeric values, put all_numeric=True .\n# Then dtypes is set to None and the loading will be slightly faster.\ndf = pd.DataFrame([[1, 2], [3, 4]])\ndf.columns = ["A", "B"]\ndf.index = ["row1", "row2"]\n\ndf\n#       A  B\n# row1  1  2\n# row2  3  4\n\ndf.dtypes\n# A     int64\n# B     int64\n# dtype: object\n\n# save numeric-only data frame\nnpl.save_numpickle(df, "/home/user/test.npy", all_numeric=True)\n# load numeric-only data frame (it recognizes automatically that it is numeric only\n# because dtypes=None or not existent in pickle file\ndf_ = npl.load_numpickle("/home/user/test.npy")\n\n\n###################################\n# save a csv or tab file as numpickle file(s) and delete original files\n###################################\nnpl.save_file_as_numpickle(fpath, sep="\\t", ending=".tab", all_numeric=True, deletep=True)\n# the data are read by pd.read_csv(), additional arguments for the reading process can be given\n# into the argument list, they will be forwarded to pd.read_csv() by *args, **kwargs\n# for the output file name, the `ending` is replaced by ".npy" and ".npy.pckl".\n# So choose the separator and ending accordingly when file is a csv file (sep=",", ending=".csv").\n```\n\n\n',
    'author': 'Gwang-Jin Kim',
    'author_email': 'gwang.jin.kim.phd@gmail.com',
    'maintainer': 'Gwang-Jin Kim',
    'maintainer_email': 'gwang.jin.kim.phd@gmail.com',
    'url': 'https://github.com/gwangjinkim/numpickle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
