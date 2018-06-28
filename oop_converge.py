import csv, time, math

class DietObj:
	list = []
	def __init__ (self, name, code, country):
		self.name = name
		self.code = code
		self.country = country

	# @classmethod
	# def csv_obj(cls, path, country, name_col, code_col):
	# 	with open(path, errors="ignore") as f:
	# 		reader = csv.reader(f)
	# 		for row in reader:
	# 			name = row[name_col]
	# 			code = row[code_col]
	# 			yield(cls(name, code, country))

	@classmethod
	def import_names(cls, path, country, name_col, code_col):
		# DietFile.list.append(DietFile(path, country))
		time.sleep(1)
		with open(path, errors="ignore") as f:
			reader = csv.reader(f)
			for row in reader:
				name = row[name_col]
				code = row[code_col]
				cls.list.append(cls(name, code, country))
			# f.seek(0)

class Food (DietObj):
	list = []
	def __init__ (self, name, code, country):
		super().__init__(name, code, country)
		self.nut_vals = []

	@classmethod
	def import_nut_vals(cls, path, country, food_code_col, nut_code_col, val_col):
		with open(path, errors="ignore") as f:
			reader = csv.reader(f)
			count = 0
			for row in reader:
				if(count == 0): count = 1; continue
				# if (count >= 10000): break
				food_code = row[food_code_col]
				nut_code = row[nut_code_col]
				val = row[val_col]
				if(int(nut_code) > 205): 
					continue

				for food in cls.list:
					if(food.country == country and food.code == food_code):
						food.nut_vals.append(float(val))
				print(count, end='\r')						
				count += 1
	@classmethod
	def compare(cls, country1, country2):
		with open('reuslts.csv', 'w+') as f:
			fieldnames = ['CA Food', 'US Match']
			writer = csv.DictWriter(f, fieldnames)
			writer.writeheader()
			compared = {}
			gen1 = (food for food in cls.list if food.country == country1)
			gen2 = (food for food in cls.list if food.country == country2)
			for food1 in cls.list:
				if(food1.country == country1 and food1.nut_vals != []):
					new_row = {}
					new_row["CA Food"] = []
					new_row["US Match"] = []
					# for nut_val1 in food1.nut_vals:
					best = [0, "", []]
					for food2 in cls.list:
						if(food2.country == country2 and food2.nut_vals != []):
							similarity = cls.nut_val_similarity(food1.nut_vals, food2.nut_vals)
							if(similarity > best[0]):
								best[0] = similarity
								best[1] = food2.name
								best[2] = food2.nut_vals
					new_row["CA Food"].append("{} {}".format(food1.name, food1.nut_vals))
					new_row["US Match"].append("{} {}".format(best[1], best[2]))
					writer.writerow(new_row)
					f.flush()

		
							# for nut_val2 in food2.nut_vals:
							# 	if(nut_val1[0] == nut_val2[0] and food2.nut_vals != []):
							# 		# print(food2.code, nut_val1, nut_val2)
							# 		if(cls.nut_val_similarity(nut_val1[1], nut_val2[1]) > 90):
							# 			if(food1.code not in compared):
							# 				compared[food1.code] = []
							# 			compared[food1.code].append(food2.code)
											
										
										# print(compared)
										# print(food1.code, nut_val1, food2.code, nut_val2)



	@staticmethod
	def nut_val_similarity(compared_vals, base_vals):
		r = []
		for i in range(0, 3):
			n = (base_vals[i] - compared_vals[i])**2
			r.append(n)
		return (1/(1 + math.sqrt(sum(r))))*100

		# compared_val = float(compared_val) + 0.1
		# base_val = float(base_val) + 0.1
		# n = (1 - abs((compared_val - base_val)/base_val))*100
		# return n

			
			
				

		
# class DietFile (DietObj):
# 	def __init__(self, path, country):
# 		self.path = path
# 		self.country = country

# class Nutrient (DietObj):
# 	def __init__ (self, name, code, country):
# 		super().__init__(self)


Food.import_names("FNDDS-CNF/Data/FNDDS.main.food.desc.csv", "US", 3, 0)
Food.import_names("FNDDS-CNF/Data/CNF.FOOD.NAME.csv", "CA", 4, 1)
Food.import_nut_vals("FNDDS-CNF/Data/FNDDS_Nutrients/fndds.nut.val.csv", "US", 0, 1, 4)
Food.import_nut_vals("FNDDS-CNF/Data/CNF_Nutrients/NUTRIENT AMOUNT.csv", "CA", 0, 1, 2)

US_foods = (food for food in Food.list if food.country == "US")
CA_foods = (food for food in Food.list if food.country == "CA")

# for food in Food.list:
# 	print(food.country, food.name, food.nut_vals)

count = 0

Food.compare("CA", "US")
# print(Food.nut_val_similarity([20, 10, 1], [21.5, 9.9, 1]))
# print(str(round(Food.nut_val_similarity(1.07, 1.1), 2)) + "%")