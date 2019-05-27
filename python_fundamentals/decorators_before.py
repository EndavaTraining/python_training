import time

def classic_loop(pets):
  start = time.time()
  result = []
  for name, food in pets.items():
    if food < 300:
      result.append(f"{name} is eating too little")
  end = time.time()
  print("classic_loop took " + str((end - start) * 1000) + " mil sec")
  return result
	

def annon_func(pets):
	start = time.time()
	result = list(f"{k} is eating too little!" for k, v in pets.items() if v < 300)
	end = time.time()
	print("annon_func took " + str((end - start) * 1000) + " mil sec")
	return result
	
pets = {
	"IronMan": 100,
	"CaptainAmerica": 350,
	"BlackWidow": 250,
	"Hulk": 800,
	"AntMan": 300,
	"Spiderman": 190
}	
print(classic_loop(pets))
print(annon_func(pets))
