import pprint

pets = {}

#open file in read-only mode
fr_handle = open("pets_feeding.txt", "r")
for line in fr_handle:
  name, food = line.split(" ")
  pets.update({name: int(food)})
fr_handle.close()
print("Pets food intake read from file:")
pprint.pprint(pets, width=1)

sick_pets = {k:v for k, v in pets.items() if v < 300}

#open file in write-only mode
fw_handle = open("sick_pets.txt", "w")
for name, food in sick_pets.items():
  fw_handle.write(f"{name} {food}\n")
fw_handle.close()

print("\nSick pets logged in file are:")
with open("sick_pets.txt", "r") as file_content:
  print(file_content.read())
