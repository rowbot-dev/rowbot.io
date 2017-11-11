
import math

series = [4,5,6,7,1,2,3]
destination = []

# [4] 0
# [4,5] 1
# [4,5,6] 2
# [4,5,6,7] 3
# [1,4,5,6,7] 0
# [1,2,4,5,6,7] 1
# [1,2,3,4,5,6,7] 2

def binary_insert(array, item):
  search_length = math.floor(len(array) / 2) # the size of the next jump (halves each time)
  index = search_length # start index at centre
  previousDirection = None # whether movement is up or down last step
  direction = None # current movement

  while True:

    # if the array length is zero, or the index is equal, place at end, creating new slot
    if index == len(array):
      break

    previousDirection = direction
    direction = get_direction(item, array[index])

    # minimum search length is 1
    # update index and search length
    search_length = max(math.floor(search_length / 2), 1)
    index += direction * search_length

    # will keep flip-flopping between two elements if its value is between them, e.g. 4 going between 3 and 5
    # there is no index for it to land on, so the index it should choose is the higher one
    # [3,5] -> a value of 4 should displace 5 -> [3,4,5]
    # so, if the direction was previously down, but the current is up, stay there.
    # print(index, direction, previousDirection) # uncomment and remove statement below to see result
    if direction == 1 and previousDirection == -1:
      break

    # if the value is lower than the first element, the direction will be -1, but we want that to mean insert as first element.
    if index == -1:
      index = 0
      break

  return index

def get_direction(i1, i2):
  if i1 > i2:
    return 1
  elif i1 == i2:
    return 0
  else:
    return -1

for i in series:
  index = binary_insert(destination, i)
  destination[index:index] = [i]
  print(destination)
