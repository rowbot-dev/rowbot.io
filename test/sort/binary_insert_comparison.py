
import math
import random
import time

d = 10000
array = [i for i in range(d)]

item = random.randint(0, d)

def binary_insert(array, item):
  previous = None
  search_length = math.floor(len(array) / 2)
  index = search_length

  while previous != index:
    # print(item, index, array[index])
    if index == len(array):
      break

    previous = index
    search_length = max(math.floor(search_length / 2), 1)
    down = item < array[index]

    if down:
      index = index - search_length
    elif item == array[index]:
      return index
    else:
      index = index + search_length

    # boundary conditions
    index = max(index, 0)
    index = min(index, len(array))

  return index

def linear_insert(array, item):
  for i in range(len(array)):
    if item < array[i]:
      return i-1

def bilinear_insert(array, item):
  l = len(array)
  for i in range(l):
    if item < array[i]:
      return i-1
    elif item > array[l - i - 1]:
      return l - i

binary_start = time.time()
binary_index = binary_insert(array, item)
binary_time = time.time() - binary_start

print(binary_index, binary_time)

linear_start = time.time()
linear_index = linear_insert(array, item)
linear_time = time.time() - linear_start

print(linear_index, linear_time)

bilinear_start = time.time()
bilinear_index = bilinear_insert(array, item)
bilinear_time = time.time() - bilinear_start

print(bilinear_index, bilinear_time)
