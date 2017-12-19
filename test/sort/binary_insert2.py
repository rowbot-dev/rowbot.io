
import math

# series = [4,5,6,7,1,2,3,8,9,10,11,33,32,31,30,29,28,27,12,13,14,15,16,17,18,19,26,25,24,23,22,21,20]
destination = list(range(100))
destination.pop(0)
destination.pop(98)

def binary_insert(array, value):
  # Stage one: get search_length down to one
  # Stage two: once the search_length is one, catalogue potential positions

  search_length = math.floor(len(array) / 2) # the size of the next jump (halves each time)
  index = search_length # start index at centre

  candidates = {}
  while index < len(array) and index >= 0:
    direction = get_direction(value, array[index])
    if search_length == 1:
      if index in candidates.values():
        break
      candidates[direction] = index

    search_length = max(math.floor(search_length / 2), 1)
    index += direction * search_length
    
  index = max(sum(list(candidates.items())[0]), 0)

  return index

def get_direction(i1, i2):
  if i1 > i2:
    # print('greater', i1, i2)
    return 1
  elif i1 == i2:
    # print('equal', i1, i2)
    return 0
  else:
    # print('less', i1, i2)
    return -1

for i in range(100):
  index = binary_insert(destination, i)
  destination[index:index] = [i]
  print(destination)

# print(destination)
# print(index)
