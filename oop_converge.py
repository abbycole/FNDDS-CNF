import csv, time

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
				if (count >= 10000): break
				food_code = row[food_code_col]
				nut_code = row[nut_code_col]
				val = row[val_col]
				if(int(nut_code) > 205): 
					continue

				for food in cls.list:
					if(food.country == country and food.code == food_code):
						food.nut_vals.append([nut_code, val])
				print(count, end='\r')						
				count += 1
	@classmethod
	def compare(cls, country1, country2):
		gen1 = (food for food in cls.list if food.country == country1)
		gen2 = (food for food in cls.list if food.country == country2)
		for food1 in gen1:
			nut_vals1 = food1.nut_vals
			for nut_val1 in nut_vals1:
				nut_id1 = nut_val1[0]
				for food2 in gen2:
					nut_vals2 = food2.nut_vals
					nut_gen = (nut_val2 for nut_val2 in nut_vals2 if nut_id1 == nut_val2[0]) 
					for nut_val2 in nut_gen:

						print(food2.code, nut_val1, nut_val2)
			
			
				

		
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

count = 0

Food.compare("US", "CA")