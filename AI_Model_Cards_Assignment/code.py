import json
import pandas as pd
from nsfw_detector import predict
import matplotlib.pyplot as plt

neutral_values = []
age_list = []
data_arr = []


""" Please note that, this below commented code is writing the output.txt file with the nsfw scores of each image
in fairface_1000_label_train.numbers file. My windows machine do not allow me to us the tensorflow_hub to parse that
data, so I ended up commenting the code. You can uncomment and it will work in different machine. Therefore, I will also
the output.txt file for the reference."""

# model = predict.load_model("./models/keras_nsfw_mobilenet2.224x224.h5")
# for i in range(1, 1000):  
#     data_arr.append(predict.classify(model, "./fairface_1000/train_1000/" + str(i) + ".jpg"))

# with open("output.txt", "w") as txt_file:
#     ctr = 0
#     for x in data_arr:
#         txt_file.write(json.dumps(data_arr[ctr].get(list(x.keys())[0])))
#         txt_file.write("\n")
#         ctr += 1

with open('output.txt') as f:
    while f:
        filename = f.readline().lstrip("./fairface_1000/train_1000").rstrip()
        try:
            data = json.loads(f.readline())
        except ValueError:
            break
        neutral_values.append(data["neutral"])

# reading the excel file and fetching the age column values from it
train = pd.read_excel('fairface_1000/fairface_1000_label_train.xlsx')
train = train.drop(0)
for i, row in train.iterrows():
    if i > 0:
        age = row['Unnamed: 1']
        age_list.append(age)
age_list.pop()

# constructing a dictionary of (age : neutral_values)
dict_age_neutral = {}
for i in range (len(age_list)):
    if age_list[i] in dict_age_neutral:
        dict_age_neutral[age_list[i]].append(neutral_values[i])
    else:
        dict_age_neutral[age_list[i]] = [neutral_values[i]]

# calculating the average of the neutral value and updating it in the dictionary
for age in dict_age_neutral:
    lst = dict_age_neutral[age]
    avg = sum(lst) / len(lst)
    dict_age_neutral[age] = avg

# plotting on a bar graph
keys = list(dict_age_neutral.keys())
values = list(dict_age_neutral.values())
plt.bar(keys, values)
plt.xlabel('Age')
plt.ylabel('Average of Neural Values')
plt.show()


