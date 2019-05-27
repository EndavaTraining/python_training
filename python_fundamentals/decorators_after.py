import time


def time_it(func):
  def wrapper(*args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    print(func.__name__ + " took " + str((end - start) * 1000) + " mil sec")
    return result
  return wrapper


@time_it
def classic_loop(pets):
  result = []
  for name, food in pets.items():
    if food < 300:
      result.append(f"{name} is eating too little")
  return result
	

@time_it
def annon_func(pets):
  result = list(f"{k} is eating too little!" for k, v in pets.items() if v < 300)
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
