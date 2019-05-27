pets = [
	("IronMan", 100),
	("CaptainAmerica", 350),
	("BlackWidow", 250),
	("Hulk", 800),
	("AntMan", 300),
	("Spiderman", 190)
]

print([f"{itm[0]} is eating too little" for itm in pets if itm[1] < 300])
