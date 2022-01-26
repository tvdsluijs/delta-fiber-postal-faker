
# from tqdm.auto import trange
# from tqdm import tqdm
# from time import sleep
# import csv

# with open('postcodes.csv') as csv_file:
#      lines = len(csv_file.readlines())

# with open('postcodes.csv') as csv_file:
#     reader = csv.reader(csv_file)
#     # with tqdm(total=lines) as pbar:
#     for row in tqdm(reader, total=lines, desc="CSV File Process"):
#         for i in tqdm(range(1, 100)):
#             print(i)
from tqdm import tqdm
from time import sleep
from random import randint

# for sec in tqdm(range(2, 30), desc="Waiting for next check!", leave=False, bar_format='{l_bar}{bar:20}{r_bar}{bar:-20b}'):
for sec in tqdm(range(2, 30), desc="Waiting for next check!", leave=False, bar_format='Waiting .... {remaining}'):
    sleep(1)
