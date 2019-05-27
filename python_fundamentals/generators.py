def sick_pets_identifier(pets):
	"""
	Generator for identifying sick pets
	"""
	for name, food in pets.items():
		if food < 300:
			yield {name: food}
			
			
pets = {
	"IronMan": 100,
	"CaptainAmerica": 350,
	"BlackWidow": 250,
	"Hulk": 800,
	"AntMan": 300,
	"Spiderman": 190
}

sick_pets = sick_pets_identifier(pets)
print("Manually displaying each sickly pet:")
print(next(sick_pets))
print(next(sick_pets))
print(next(sick_pets))

print("Using a for loop to display the sick pets:")
sick_pets2 = sick_pets_identifier(pets)
for item in sick_pets2:
	print(item)
