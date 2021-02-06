import os
import uuid
from shutil import copyfile

# Enter property IDs here
property_ids = [1, 2]

if not os.path.exists('./images'):
    os.makedirs('./images')

for id in property_ids:
  for filename in os.listdir("./{}".format(id)):
    file_format = filename.split(".")[1]
    uuid_name = "{}.{}".format(uuid.uuid4(), file_format)
    file_name_path = "./{}/{}".format(id, filename)
    # os.rename(file_name_path, uuid_name)
    copyfile(file_name_path, "./images/{}".format(uuid_name))
    print("{},{}".format(id, uuid_name))
