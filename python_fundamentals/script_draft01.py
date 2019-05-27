import operator

pets = [
	("IronMan", 100),
	("CaptainAmerica", 350),
	("BlackWidow", 250),
	("Hulk", 800),
	("AntMan", 300),
	("Spiderman", 190)
]

pets.sort(key=operator.itemgetter(1))
idx = 0
while idx < len(pets) and pets[idx][1] < 300:
  print(f"{pets[idx][0]} is eating too little!")
  idx += 1
