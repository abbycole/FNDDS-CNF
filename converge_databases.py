import sys
import csv
import difflib

path_to_data = 'FNDDS-CNF/Data/'


cnf = open(path_to_data + 'CNF.FOOD.NAME.csv', encoding='utf-8', errors='ignore') 
csv_cnf = csv.reader(cnf)															

cnf_food_row_num = 4
fndds_food_row_num = 3

converged_database = {}
new_file = open('new_csv.csv', 'w+')
fieldnames = ['Canadian Food', 'US Matches']
new_csv = csv.DictWriter(new_file, fieldnames)
new_csv.writeheader()

count = 0

for cnf_row in csv_cnf:
	if (count == 0): count = 1; continue
	if (count == 50): break

	fndds = open(path_to_data + 'FNDDS.main.food.desc.csv')  									
	csv_fndds = csv.reader(fndds)															
	newrow = {'Canadian Food': cnf_row[4]}																				
	top_three = [[0, "", 0], [0, "", 0], [0, "", 0]]																		

	for fndds_row in csv_fndds:																	
		sequence = difflib.SequenceMatcher(isjunk=None, a=cnf_row[4], b=fndds_row[3])			 	
		difference = sequence.ratio()*100

		for i in range(0,3):
			if (difference > top_three[i][0]):
				top_three[i] = [difference, fndds_row[3], fndds_row[0]]
				break	
	fndds.close()

	newrow_text = ""
	for item in top_three:
		newrow_text += item[1] + '(' + str(round(item[0], 2)) + '% match ' + '#' + item[2] + '); '
	newrow['US Matches'] = newrow_text
	new_csv.writerow(newrow)
	count += 1

	
	




