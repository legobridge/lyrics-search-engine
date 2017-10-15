'''
This is a preprocessing script for the Lyrics Search Engine.
On execution, it will create triplets of Track ID, Artist Name, and Title
for each song in the lyrics dataset, and store these in "id_to_metadat.txt".
It also calculates the IDF (Inverse Document Frequency) values for each
of 5000 most occuring words in the lyrics dataset and writes them to
a file called "idf.txt".

This script makes use of the musiXmatch dataset, 
the official lyrics collection for the Million Song Dataset, 
available at: http://labrosa.ee.columbia.edu/millionsong/musixmatch

Author: Kushal Agrawal
Date of Completion: 30/09/2017
'''

import math
import time
import h5py


# Note the start time of the process
start_time = time.time()
print("Welcome. Please be patient as this process can take around 10 minutes")
print("Retrieving Track IDs and Term Frequencies...")

# Lyrics dataset (contains lyrics data of more than 210,000 songs)
lyrics = open('mxm_dataset_train.txt', 'r')

# Discard first line
lyrics.readline()

# Load the data into a list
tracks = [track.rstrip('\n') for track in lyrics]

# Close file post-use
lyrics.close()

# Set to store Track IDs for faster searching
track_ids = set()

# List to store Document Frequencies
document_frequency = [0] * 5001

# The total number of documents
N = len(tracks)

# Fetch Track IDs and presence of word indices from each line
for track in tracks:
	attrib = track.split(',')
	track_ids.add(attrib[0])
	for i in range(2, len(attrib)):
		word_index = int(attrib[i][:attrib[i].index(':')])
		document_frequency[word_index] += 1

print("Computing Inverse Document Frequencies...")

# String to store data to be written to "idf.txt"
idf_string = ''

# Compute and add the IDF values to "idf_string"
for i in range(0, len(document_frequency)):
	if (document_frequency[i] == 0):
		idf_string += '0\n'
	else:
		idf_string += str(math.log10(N / document_frequency[i])) + '\n'

print("Writing to disk, do not interrupt.")

# Write to file
idf_file = open('idf.txt', 'w')

idf_file.write(idf_string)

idf_file.close()


print("Mapping Track IDs to Metadata...")

# Million Songs dataset (in HDF5 format)
summary_file = h5py.File('./msd_summary_file.h5', 'r')
asongs = summary_file['analysis']['songs']
msongs = summary_file['metadata']['songs']

# String to store data to be written to "id_to_metadata.txt"
itm_string = ''

# For each of the million songs, fetch the Track ID, Artist Name,
# and the Title of the song. If Track ID exists in our lyrics dataset,
# add (in CSV form) the three values to the "itm_string" 
for i in range(1000000):
	track_id = asongs[i]['track_id'].decode('utf-8')
	if (track_id in track_ids):
		artist = msongs[i]['artist_name'].decode('utf-8')
		title = msongs[i]['title'].decode('utf-8')
		itm_string += track_id + ',' + artist + ',' + title + '\n'

print("Writing to disk, do not interrupt.")

# Write to file
itm_file = open('id_to_metadata.txt', 'w')

itm_file.write(itm_string)

itm_file.close()

# Finishing statements, print time taken
print("All done :)")
end_time = time.time()
print("Time Taken: " + str((end_time - start_time) / 60) + " minutes")