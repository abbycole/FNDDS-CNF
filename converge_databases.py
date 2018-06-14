import sys
import csv
import difflib

data_path = 'Data/'																	

with open(data_path + 'CNF.FOOD.NAME.csv', encoding='utf-8', errors='ignore') as cnf_file:
	cnf_reader = csv.reader(cnf_file)
	with open(data_path + 'CNF-FNDDS.matches.csv', 'w+') as new_file:
		fieldnames = ['Canadian Food', 'US Matches']
		new_writer = csv.DictWriter(new_file, fieldnames)
		new_writer.writeheader()

		count = 0

		for cnf_row in cnf_reader:
			if (count == 0): count = 1; continue														# do not include header row
			# if (count == 10): break																	# limits how much gets processed

			with open(data_path + 'FNDDS.main.food.desc.csv') as fndds_file:
				fndds_reader = csv.reader(fndds_file)															
				new_row = {'Canadian Food': cnf_row[4]}																				
				top_three = [[0, "", 0], [0, "", 0], [0, "", 0]]																		

				for fndds_row in fndds_reader:																	
					sequence = difflib.SequenceMatcher(isjunk=None, a=cnf_row[4], b=fndds_row[3])		# compare each FNDDS row to the current CNF row		 	
					difference = sequence.ratio()*100													# express as floating point percentage

					if (difference > 60) :																# only list > 60% similarity
						for i in range(0,3):
							if (difference > top_three[i][0]):											# arrange top three > 60%
								top_three[i] = [difference, fndds_row[3], fndds_row[0]]					# TODO: inlclude ties?
								break	
			count += 1


			new_row_text = ""
			for item in top_three:
				if (item[2] != 0) :																		# do not list empty top_three values
					new_row_text += str(item[1]) + '(' + str(round(item[0], 2)) + '% match ' + '#' + str(item[2]) + '); '
				
			new_row['US Matches'] = new_row_text
			new_writer.writerow(new_row)
					




		
		




