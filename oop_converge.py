import csv, time

class DietObj:
	list = []
	def __init__ (self, name, code, country):
		self.name = name
		self.code = code
		self.country = country

	@classmethod
	def csv_obj(cls, path, country, name_col, code_col):
		with open(path, errors="ignore") as f:
			reader = csv.reader(f)
			for row in reader:
				name = row[name_col]
				code = row[code_col]
				yield(cls(name, code, country))

	@classmethod
	def import_from_csv(cls, path, country, name_col, code_col):
		for obj in cls.csv_obj(path, country, name_col, code_col):
			cls.list.append(obj)

class Food (DietObj):

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
				if (count >= 5000): break
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
		

class Nutrient (DietObj):
	def __init__ (self, name, code, country):
		super().__init__(self)


Food.import_from_csv("FNDDS-CNF/Data/FNDDS.main.food.desc.csv", "US", 3, 0)
Food.import_from_csv("FNDDS-CNF/Data/CNF.FOOD.NAME.csv", "CA", 4, 1)
Food.import_nut_vals("FNDDS-CNF/Data/FNDDS_Nutrients/fndds.nut.val.csv", "US", 0, 1, 4)
Food.import_nut_vals("FNDDS-CNF/Data/CNF_Nutrients/NUTRIENT AMOUNT.csv", "CA", 0, 1, 2)

US_foods = (food for food in Food.list if food.country == "US")
CA_foods = (food for food in Food.list if food.country == "CA")

count = 0
for food in Food.list:
	if(count == 1000): continue
	print("{}  {}".format(food.country, food.nut_vals))
	count += 1