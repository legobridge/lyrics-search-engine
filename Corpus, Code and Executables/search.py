'''
This is the module which performs the core functionality of the
Lyrics Search Engine. It runs in the form of a Tkinter based GUI
and takes as input a text query consisting of fragmented, 
incomplete lyrics, and gives as output a list of at most 10
Artist-Song Title pairs, ranked in order of most similar to least
similar. There is an initial loading time of approximately 10 seconds,
but all successive searches are performed almost instaneously.

Author: Kushal Agrawal
Date of Completion: 30/09/2017
'''

import math
from stemming.porter2 import stem
import tkinter as tk

class SearchEngine(tk.Frame):
	'''
	This is the master application defining class and encapsulates
	everything from the GUI widgets to the core search implementation.
	'''

	def __init__(self, master = None):
		''' Constructor for the SearchEngine class. '''
		tk.Frame.__init__(self, master)
		self.entry = tk.StringVar()
		self.msg = tk.StringVar()
		self.grid()
		self.configureGrid()
		self.createWidgets()
		self.setMessage('Loading more than 210,000 song lyrics into memory, please be patient...')

	def configureGrid(self):
		''' Configure the Tkinter grid layout. '''
		self.rowconfigure(0, minsize = 50)
		self.columnconfigure(0, minsize = 80)
		self.rowconfigure(1, minsize = 50)
		self.columnconfigure(1, minsize = 80)
		self.rowconfigure(2, minsize = 50)
		self.columnconfigure(2, minsize = 80)
		self.rowconfigure(3, minsize = 50)
		self.columnconfigure(3, minsize = 80)
		self.rowconfigure(4, minsize = 50)
		self.columnconfigure(4, minsize = 80)
		self.rowconfigure(5, minsize = 50)
		self.columnconfigure(5, minsize = 80)
		self.rowconfigure(6, minsize = 50)
		self.columnconfigure(6, minsize = 80)
		self.rowconfigure(7, minsize = 50)
		self.columnconfigure(7, minsize = 80)
		self.rowconfigure(8, minsize = 50)

	def createWidgets(self):
		''' Define the attributes of the GUI elements. '''

		# The Quit Button
		self.quitButton = tk.Button(self, text = 'Quit', command = self.quit)
		self.quitButton.grid(row = 8, column = 7, rowspan = 1, columnspan = 1, padx = 15, pady = 25, sticky = tk.N + tk.E + tk.S + tk.W)

		# The Label above the Entry Text Box
		self.label = tk.Label(self, justify = tk.LEFT, text = 'Please enter your lyrical query here (the more words, the better)')
		self.label.grid(row = 0, column = 0, rowspan = 1, columnspan = 7, padx = 25, pady = 5, sticky = tk.W)

		# The Entry Text Box
		self.entryBox = tk.Entry(self, width = 60, bd = 3, relief = tk.RIDGE, textvariable = self.entry)
		self.entryBox.grid(row = 1, column = 0, rowspan = 1, columnspan = 7, padx = 20, pady = 5, sticky = tk.N + tk.E + tk.S + tk.W)

		# The Search Button
		self.enterButton = tk.Button(self, text = 'Search', command = self.search)
		self.enterButton.grid(row = 1, column = 7, rowspan = 1, columnspan = 1, padx = 15, pady = 15, sticky = tk.N + tk.E + tk.S + tk.W)

		# The Message Box to display the output
		self.messageBox = tk.Message(self, anchor = tk.NW, padx = 25, pady = 25, width = 500, justify = tk.LEFT, relief = tk.RIDGE, bd = 3, textvariable = self.msg)
		self.messageBox.grid(row = 2, column = 0, rowspan = 7, columnspan = 7, padx = 20, pady = 25, sticky = tk.N + tk.E + tk.S + tk.W)


	def setMessage(self, message):
		''' Set messageBox to display "message". '''
		self.msg.set(message)


	#############################################
	########### Data Loading Function ###########
	#############################################

	def loadPreprocessedData(self):
		''' Load the data prepared by "preprocess.py". '''

		# Preprocessed file with tuples consisting of comma
		# separated Track IDs, Artist Names, and Titles of songs
		self.itm_file = open('id_to_metadata.txt', 'r')

		# Dictionary to map Track IDs to Artist Names and Titles
		self.id_to_metadata = {}

		for itm in self.itm_file:
			track = itm.strip().split(',')
			self.id_to_metadata[track[0]] = (track[1], track[2])

		self.itm_file.close()


		# Preprocessed file with idf values
		# on the corresponding line number
		self.idf_file = open('idf.txt', 'r')

		# Load the idf values into a list
		self.idfs = [float(idf.rstrip('\n')) for idf in self.idf_file]

		self.idf_file.close()


		# Lyrics dataset
		self.lyrics = open('mxm_dataset_train.txt', 'r')

		# Load the words into a list
		self.words = self.lyrics.readline().strip().split(',')

		# Load the data into a list
		self.tracks = [track.rstrip('\n') for track in self.lyrics]

		self.lyrics.close()

		# Dictionary to map words to their indices
		self.word_to_index = {}

		for i in range(1, len(self.words)):
			self.word_to_index[self.words[i]] = i

		# Dictionaries to map word indices and Track IDs to Term Frequencies
		self.tf_wi_ti = 5001 * [0]
		self.tf_ti_wi = {}

		for i in range(0, 5001):
			self.tf_wi_ti[i] = {}

		for track in self.tracks:
			attrib = track.split(',')
			track_id = attrib[0]
			self.tf_ti_wi[track_id] = {}
			for i in range(2, len(attrib)):
				word_index = int(attrib[i][:attrib[i].index(':')])
				freq = int(attrib[i][(attrib[i].index(':') + 1):])
				self.tf_wi_ti[word_index][track_id] = freq
				self.tf_ti_wi[track_id][word_index] = freq
		self.setMessage('Loading Complete.')

	#############################################


	#############################################
	########## Query Stemming Function ##########
	#############################################

	def stemQuery(self, query):
		'''
		Stem the words in the query from the argument
		and return a list of tokenized words.
		'''

		# Remove newline characters
		query = query.replace('\n', ' ')
		query = query.replace('\r', ' ')

		# Convert to lowercase
		query = query.lower()

		# Special cases (English)
		query = query.replace("'m ", " am ")
		query = query.replace("'re ", " are ")
		query = query.replace("'ve ", " have ")
		query = query.replace("'d ", " would ")
		query = query.replace("'ll ", " will ")
		query = query.replace(" he's ", " he is ")
		query = query.replace(" she's ", " she is ")
		query = query.replace(" it's ", " it is ")
		query = query.replace(" ain't ", " is not ")
		query = query.replace("n't ", " not ")
		query = query.replace("'s ", " ")

		# Remove punctuation and symbols
		punctuation = (',', "'", '"', ",", ';', ':', '.', '?', '!', '(', ')',
		               '{', '}', '/', '\\', '_', '|', '-', '@', '#', '*')
		for p in punctuation:
		    query = query.replace(p, '')

		words = filter(lambda x: x.strip() != '', query.split(' '))

		# Stem words using Porter Stemmer
		words = map(lambda x: stem(x), words)

		return list(words)

	#############################################


	#############################################
	###### Query TFIDF Calculation Function #####
	#############################################

	def queryTfidfs(self):
		''' Calculate the TFIDF vector components for the query. '''
		self.query_tfidfs = {}
		self.query_vector_length = 0.0
		for query_tf_key in self.query_tfs:
			self.query_tfidfs[query_tf_key] =  (1 + math.log10(self.query_tfs[query_tf_key])) * self.idfs[query_tf_key]
			self.query_vector_length += self.query_tfidfs[query_tf_key] ** 2
		self.query_vector_length = math.sqrt(self.query_vector_length)

	#############################################


	#############################################
	######### TFIDF Calculation Function ########
	#############################################

	def tfidfScore(self, track_id):
		'''
		Calculate the TFIDF vector components for the document
		taken from the argument and return its TFIDF Score.
		'''

		# Compute TFIDF for the track denoted by "track_id"
		document_tfidfs = {}
		document_vector_length = 0.0
		for track_word_key in self.tf_ti_wi[track_id]:
			document_tfidfs[track_word_key] = (1 + math.log10(self.tf_ti_wi[track_id][track_word_key])) * self.idfs[track_word_key]
			document_vector_length += document_tfidfs[track_word_key] ** 2
		document_vector_length = math.sqrt(document_vector_length)

		# Compute the query-document TFIDF Score
		tfidf_score = 0.0
		for query_tf_key in self.query_tfs:
			if query_tf_key in self.tf_ti_wi[track_id]:
				tfidf_score += self.query_tfidfs[query_tf_key] * document_tfidfs[query_tf_key]
		tfidf_score /= (document_vector_length * self.query_vector_length)

		return tfidf_score

	#############################################


	#############################################
	######## Top Ten Selection Function #########
	#############################################

	def getTopTen(self):
		''' Select the top tracks and return them as a list. '''
		topTracks = []
		curMax = 0.0
		for i in range(0, 10):
			for tfidfs_key in self.tfidfs:
				if tfidfs_key > curMax and self.tfidfs[tfidfs_key] not in topTracks:
					curMax = tfidfs_key
			if (curMax == 0.0):
				break
			topTracks.append(self.tfidfs[curMax])
			curMax = 0.0
		return topTracks

	#############################################


	#############################################
	######### Query Processing Function #########
	#############################################

	def answerQuery(self, query):
		''' Process the query by calling the relevant methods and return a list of songs. '''

		# Query Term Frequencies
		self.query_tfs = {}

		# List of (stemmed) query words
		query_words = self.stemQuery(query)

		for qword in query_words:
			if qword in self.word_to_index:
				qword_index = self.word_to_index[qword]
				if self.idfs[qword_index] >= 0.2:
					if qword_index in self.query_tfs:
						self.query_tfs[qword_index] = self.query_tfs[qword_index] + 1
					else:
						self.query_tfs[qword_index] = 1

		# Compute TFIDFs for the query
		self.queryTfidfs()

		matches = {}
		for query_tfs_key in self.query_tfs:
			for track_id in self.tf_wi_ti[query_tfs_key]:
				if track_id in matches:
					matches[track_id] += 1
				else:
					matches[track_id] = 1

		# Set of tracks to check
		tracks_to_check = set()
		for track_id in self.id_to_metadata:
			if track_id in matches and matches[track_id] >= len(self.query_tfs) / 2:
				tracks_to_check.add(track_id)

		# TFIDFs for all documents
		self.tfidfs = {}
		for track_id in tracks_to_check:
			self.tfidfs[self.tfidfScore(track_id)] = track_id

		return self.getTopTen()

	#############################################


	#############################################
	########  Function Called on Clicking #######
	######## the Search Button in the GUI #######
	#############################################

	def search(self):
		'''
		Initiate the search by calling answerQuery() and set
		the messageBox contents to the result of the search.
		'''

		# Get the text from the entry box
		query = self.entry.get()

		# Get list of top matches
		top_tracks = self.answerQuery(query)

		msg_string = ''

		if len(top_tracks) < 1:
			msg_string += '\nSorry, there were no close matches, try adding more words'
		else:
			msg_string += '\nThe top tracks matching your query are:\n\n'
			counter = 1
			for top_track_id in top_tracks:
				metadata = self.id_to_metadata[top_track_id]
				msg_string += str(counter) + ". " + metadata[0] + " - " + metadata[1] + '\n'
				counter += 1

		# Set the message 
		self.setMessage(msg_string)

	#############################################


###############################################################################

root = tk.Tk()
app = SearchEngine(root)
app.master.title('Lyrics Search Engine')
app.after(500, app.loadPreprocessedData)
app.mainloop()