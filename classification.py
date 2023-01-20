import csv
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
# Import CountVectorizer class. 
# CountVectorizer converts text data to matrix of token counts.
from sklearn.feature_extraction.text import CountVectorizer 
# Create model(naive bayes) and training. 
from sklearn.naive_bayes import MultinomialNB
# Model Accuracy, how often is the classifier correct?
from sklearn import metrics 
def organize_classes(filename):
	#LOAD RAW DATA FEOM CSV FILE
	filename = filename
	raw_data = open(filename, 'rt')
	reader = csv.reader(raw_data, delimiter=',', quoting=csv.QUOTE_NONE)
	x = list(reader)
	data = np.array(x)
	organized_data= [[] for x in range(32)]
	for x in data:
		index = x[1]
		organized_data[int(index)].append(x[0])
	return organized_data
def train_model(filename) :
	#LOAD RAW DATA FEOM CSV FILE
	filename = filename
	raw_data = open(filename, 'rt')
	reader = csv.reader(raw_data, delimiter=',', quoting=csv.QUOTE_NONE)
	x = list(reader)
	data = np.array(x)
	#shuffle dataset
	np.random.shuffle(data)

	#split train and sample from eachother
	train , test = train_test_split(data, test_size = 0.0005)

	# Organize data
	values = []
	target = []
	for i in train:
		values.append(i[0])
		target.append(i[1])

	test_values = []
	tets_target = []
	for i in test:
		test_values.append(i[0])
		tets_target.append(i[1])
	count_vector = CountVectorizer()
	X_train_counts = count_vector.fit_transform(values)
	LM = MultinomialNB().fit(X_train_counts, target)
	docs_new = test_values
	# Transfroming.
	X_new_counts = count_vector.transform(docs_new)

	# Execute prediction(classification).
	predicted = LM.predict(X_new_counts)
	'''
	# Show predicted data.
	for doc, category in zip(docs_new, predicted):
		print("{0} => {1}".format(doc, category))
	print("Accuracy:",metrics.accuracy_score(tets_target,predicted))
	'''
	return LM , count_vector
def classify(docs_new, LM, count_vector):
	X_new_counts = count_vector.transform(docs_new)
	predicted = LM.predict(X_new_counts)
	# Show predicted data.
	for doc, category in zip(docs_new, predicted):
		print("{0} => {1}".format(doc, category))
	return predicted[0]

def main():
	my_list =['کشوری در خاور میانه']
	LM , count_vector = train_model("data/classification_data .csv")
	predicted_class =classify(my_list,LM, count_vector)
	organize_classes("data/classification_data .csv")
if __name__ == '__main__':
	main()
	