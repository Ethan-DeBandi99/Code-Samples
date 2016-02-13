# Naive Bayes Classifer
# Retrieve and label spam and ham documents from spam and ham directories.
# The features are the 2000 most common words in all the documents.
# Each feature gets a say in deciding which label should be assigned to a given input value.
# Starts by calculating prior probability of each label, determined by the frequency of
# each label in the training set, e.g. 60 spam and 40 ham out of 100 files, 
# spam has a 60% prior probability and ham has a 40% prior probability.
# Each feature contributes to the prior probability to get a likelihood estimate foe each label.
# The label with the highest likelihood estimate is assigned to the input value, 
# e.g. 39% estimate for spam, 61% estimate for ham, file is assigned "ham".
import nltk
import os
import random
from nltk.corpus import stopwords
stopwords = nltk.corpus.stopwords.words('english') #all non-descriptive English words  
class mySpamClassifier:
	def __init__(self, spamFolder, hamFolder):
		self.totalSpamWords = []
		self.totalHamWords = []
		self.totalSpamFile = []
		self.spamFiles = os.listdir(spamFolder)
		self.totalHamFile = []
		self.hamFiles = os.listdir(hamFolder)
		
		for docs in self.spamFiles:
			textFile = open(spamFolder + "/" + docs, "r")
			lines = textFile.readlines()
			textFile.close()
			wordList = [w.split() for w in lines]#splits the lines into words
			words = sum(wordList, [])#flattens inot a simple list of all words
			featureWords = [w.lower() for w in words if w not in stopwords and len(w) > 1 and w.isalpha()] #omits needless words
			featureWords = list(set(featureWords))  # remove duplicates
			self.totalSpamFile.append((featureWords, "spam")) # assigns label for file
			self.totalSpamWords += featureWords #adds words to total words
			
		for docs in self.hamFiles:
			textFile = open(hamFolder + "/" + docs, "r")
			lines = textFile.readlines()
			textFile.close()
			wordList = [w.split() for w in lines]#splits the lines into words
			words = sum(wordList, [])#flattens inot a simple list of all words
			featureWords = [w.lower() for w in words if w not in stopwords and len(w) > 1 and w.isalpha()] #omits needless words
			featureWords = list(set(featureWords))  # remove duplicates
			self.totalHamFile.append((featureWords, "ham")) # assigns label for file
			self.totalHamWords += featureWords #adds words to total words
	
		self.documents = self.totalSpamFile
		self.documents += self.totalHamFile
		random.shuffle(self.documents)#list with spam and ham documents randomly distributed

		certainIndex = int(len(self.documents)*0.9)#getting 90% and 10% of the total documents
		self.trainDocs = self.documents[:certainIndex] #90% of total documents
		self.testDocs = self.documents[certainIndex:] #10% of total documents
		self.totalWords = self.totalSpamWords + self.totalHamWords 
		random.shuffle(self.totalWords)
		self.all_words = nltk.FreqDist(w for w in self.totalWords if w.isalpha())#lists frequency of all words
		self.word_features = list(self.all_words)[:2000] #lists top 2000 most frequent words


	def train(self): #trains the classifier by calculating probabilities	
		self.numSpam = 0
        	for i in self.trainDocs:
            		if(i[1]=="spam"):
                		self.numSpam += 1
                self.probSpam = self.numSpam/(len(self.documents))
		self.numHam = len(self.documents)-self.numSpam
         	self.probHam = self.numHam/(len(self.documents))
        	self.spamProb = {}
        	self.hamProb = {}  
		self.hamEp = 1/(self.numHam+1)
		self.spamEp = 1/(self.numSpam+1) 
        	for doc in self.trainDocs:
            		for word in self.word_features:
                		self.spamProb[word] = 0
                		self.hamProb[word] = 0
                 		if doc[1] == "spam":
                    			if word in doc[0]:
                        			self.spamProb[word] += 1
                		else:
                  			if word in doc[0]:
                        			self.hamProb[word] += 1
        	for word in self.spamProb:
			if self.spamProb[word] == 0:
				self.spamProb[word] = self.spamEp
			else:
				self.spamProb[word] = self.spamProb[word]/self.numSpam;
		for word in self.hamProb:
			if self.hamProb[word] == 0:
				self.hamProb[word] = self.hamEp
			else:
				self.hamProb[word] = self.hamProb[word]/self.numHam;
		
		
		
	def classify (self): #labels test docs as spam or ham based on feature probs.
		self.classifiedList = [] #list where docs are labeled
		self.probS = 1
		self.probH = 1	
		for doc in self.testDocs:
			for word in doc:
				if word in self.word_features:
					self.probS = self.probS * self.spamProb[word]
					self.probH = self.probH * self.hamProb[word]
			self.probS = self.probS * self.probSpam
			self.probH = self.probH * self.probHam
			if self.probS > self.probH:
				self.classifiedList.append((doc,"Spam"))
			else:
				self.classifiedList.append((doc,"Ham"))
		return self.classifiedList

	def accuracy (self): #calculates percent of docs that were correctly classified
		result = 0
		countCorrect = 0
		for item in self.classifiedList:
			if item[1] == "Spam":
				if item[0][1] in self.spamFiles:
					countCorrect += 1
			else:
				if item[0][1] in self.hamFiles:
					countCorrect +=1
		result = float(countCorrect)/float(len(self.classifiedList))
		return result

