import os
import uuid
from shutil import copyfile

property_ids = []

ids = input("Enter property IDs in comma separated (ex. 1, 2, 3):")

for id in ids.split(","):
    property_ids.append(int(id))

if not os.path.exists('./images'):
    os.makedirs('./images')

if os.path.exists("output.csv"):
    os.remove("output.csv")

out_file = open("output.csv", "w")
out_file.write("property_id,uuid_filename\n")

for id in property_ids:
  for filename in os.listdir("./{}".format(id)):
    if filename.startswith("."):
        continue
    try:
        file_format = filename.split(".")[1]
    except IndexError:
        continue
    uuid_name = "{}.{}".format(uuid.uuid4(), file_format)
    file_name_path = "./{}/{}".format(id, filename)
    # os.rename(file_name_path, uuid_name)
    copyfile(file_name_path, "./images/{}".format(uuid_name))
    out_file.write("{},{}\n".format(id, uuid_name))
