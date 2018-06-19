import sys
import csv
import difflib

data_path = 'Data/'		

def prepare_string(str):
	str = str.replace(',', '')
	str = str.lower()
	return str

def get_similarity_percentage(a, b):
	prepare_string(a)
	prepare_string(b)
	sequence = difflib.SequenceMatcher(isjunk=None, a=a, b=b)
	return sequence.ratio()*100			

def check_top_three(top_three_matches, similarity, name, id):
	for i in range(0,3):
		top_similarity = top_three_matches[i][0]
		if (similarity > top_similarity):											
			top_three_matches[i] = [similarity, name, id]									# TODO: inlclude ties?
			break	

def find_match(current_item, match_item, match_id, top_three_matches):
	similarity = get_similarity_percentage(current_item, match_item)	

	if (similarity > 60) :																
		check_top_three(top_three_matches, similarity, match_item, match_id)	

def write_new_row(top_three_matches, new_row, new_writer):
	new_row_text = ""
	for match in top_three_matches:
		match_id = str(match[2])
		match_name = str(match[1])
		match_similarity = str(round(match[0], 2))

		if (match_id != '0') :																		# do not list empty top_three values
			new_row_text += match_name + '(' + match_similarity + '% match ' + '#' + match_id + '); '

	new_row['US Matches'] = new_row_text
	new_writer.writerow(new_row)

with open(data_path + 'UKfoodlist.csv', encoding='utf-8', errors='ignore') as compared_file:
	compared_reader = csv.reader(compared_file)

	with open(data_path + 'UK-FNDDS.matches.csv', 'w+') as new_file:
		fieldnames = ['UK Food', 'US Matches']
		new_writer = csv.DictWriter(new_file, fieldnames)
		new_writer.writeheader()

		count = 0
		
		# end = 0.0
		for compared_row in compared_reader:
			if (count == 0): count = 1; continue														# do not include header row
			if (count == 50): break																	# limits how much gets processed


			with open(data_path + 'FNDDS.main.food.desc.csv') as fndds_file:
				fndds_reader = csv.reader(fndds_file)															
				new_row = {'UK Food': compared_row[1]}																				
				top_three = [[0, "", 0], [0, "", 0], [0, "", 0]]	

				match_count = 0
				for fndds_row in fndds_reader:
					find_match(compared_row[1], fndds_row[3], fndds_row[0], top_three)
					print("Finding matches for row: " + str(count) + " (in row " + str(match_count) + ")", end='\r', flush=True)
					match_count += 1

			write_new_row(top_three, new_row, new_writer)
			count += 1
					




		
		




