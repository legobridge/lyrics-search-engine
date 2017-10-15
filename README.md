## Lyrics Search Engine

#### Author - Kushal Agrawal

The following two methods can be employed to run the program:

1. Standalone Executables - The author has provided standalone executable files ("preprocess" and "search", with no file extensions) that can be executed without installing any software (not even the Python interpreter is required) on Linux based operating systems.

2. Compile and Run - The compilation and execution of this program requires that the user have Python 3 installed on their system. Additional modules required for proper functioning are:
	a) [h5py](http://docs.h5py.org/en/latest/build.html)
	b) [Porter Stemmer](https://pypi.python.org/pypi/stemming/1.0)
After installing Python 3 and the aforementioned modules, one only needs to run the two python scripts "preprocess.py" and "search.py" by typing "python3 <filename>.py" in whatever terminal/console one prefers.

The lyrics from "Example Queries.txt" can be used to test the Search Engine.

Note - The "preprocess.py" script needs to be run only once (and in fact, not even once since the author has provided the two files that the script generates along with the code). The existence of the preprocessed files is necessary for the functioning of "search.py".

GitHub Note - The 100.0 MB file size limit of GitHub prohibits the inclusion of the 300 MB msd_summary_file.h5, and so it can be obtained and put in the correct directory by downloading it from [here](http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/msd_summary_file.h5).