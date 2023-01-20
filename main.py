from grid import *
from classification import *
from synonyms import *
from opposite import *
def get_possible_words(category):
	file = "data/" +str(category) + ".txt"
	f = open(file, "r")
	words = f.read().splitlines()
	f.close()
	return words

def main():
	grid = make_grid("data/sample.txt");
	print("initial grid:")
	print(grid);
	#train model 
	LM , count_vector = train_model("data/classification_data .csv") 
	horizental_info,vertical_info = get_info("data/sample.txt")
	#get posiible words of every key 
	for i in horizental_info:
		for key in i:
			words_list =key["KEY"].split()
			if len(words_list) == 1 :
				key["VALUE"] = get_syn(key["KEY"])
			elif words_list[0]=='مترادف' or words_list[0]=='معنی':
				key["VALUE"] = get_syn(words_list[1])
			elif words_list[0] == 'مخالف':
				key["VALUE"] = get_op(words_list[1])
			else:
				key["VALUE"] = get_possible_words(classify([key["KEY"]],LM, count_vector))
				print(key["VALUE"])
	for i in vertical_info:
		for key in i:
			words_list =key["KEY"].split()
			if len(words_list) == 1 :
				key["VALUE"] = get_syn(key["KEY"])
			elif words_list[0]=='مترادف' or words_list[0]=='معنی':
				key["VALUE"] = get_syn(words_list[1])
			elif words_list[0] == 'مخالف':
				key["VALUE"] = get_op(words_list[1])
			else:
				key["VALUE"] = get_possible_words(classify([key["KEY"]],LM, count_vector))

if __name__ == '__main__':
	main()
