
import os
import glob

import csv
import cv2


def crop_img(img, h, w):
    center = img.shape
    x = center[1] / 2 - w / 2
    y = center[0] / 2 - h / 2
    crop_img = img[int(y):int(y + h), int(x):int(x + w)]
    return crop_img


# Both annotations and training examples can be found on http://transattr.cs.brown.edu/ 
with open("../annotations/annotations.tsv") as file:
    tsv_file = csv.reader(file, delimiter="\t")

    with open("../annotations/attributes.txt") as file:
        attribute_list = [line.rstrip() for line in file]

    items = []

  prev_source_fname = '00000064/1.jpg'
    count = 0

    for i, line in enumerate(tsv_file):
        fname = line[0]
        scores = line[1:]
        indices = list(filter(lambda x: float(scores[x].split(',')[0]) > 0.8, range(len(scores))))
        prompt = "".join([attribute_list[i] + ", " for i in indices])[:-2]
        # print(i, line)

        item = {}
        item["prompt"] = prompt
        item["source"] = "source/{}.png".format(i)
        item["target"] = "target/{}.png".format(i)
        items.append(item)

        if fname.split('/')[0] != prev_source_fname.split('/')[0]:
            prev_source_fname = fname

      # imageAlignedLD is the raw dataset (http://transattr.cs.brown.edu/).
        source_img = cv2.imread(os.path.join('../imageAlignedLD', prev_source_fname))
        target_img = cv2.imread(os.path.join('../imageAlignedLD', fname))

        source_img = crop_img(source_img, 480, 480)
        target_img = crop_img(target_img, 480, 480)

        source_img = cv2.resize(source_img, (512, 512), interpolation = cv2.INTER_CUBIC)
        target_img = cv2.resize(target_img, (512, 512), interpolation = cv2.INTER_CUBIC)


        if not os.path.exists('../source'):
            os.makedirs('../source')

        if not os.path.exists('../target'):
            os.makedirs('../target')
        cv2.imwrite("../source/{}.png".format(i), source_img)
        cv2.imwrite("../target/{}.png".format(i), target_img)

import json
with open('../prompt.json', 'w') as f:
    json.dump(items, f)
