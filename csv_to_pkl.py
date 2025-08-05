# -*- coding: utf-8 -*-
import sys
import os
import csv
import json
import pickle
from copy import deepcopy

# 默认使用命令python train_csv_to_pkl.py ./annotations/train.csv ./annotations/train.pkl

csvPath = sys.argv[1]
#pbtxtPath = sys.argv[2]
targetPath = sys.argv[2]

per_target_annotations_dict = {'bounding_box': [], 'label': [], 'person_id': []}
labels_list = []
video_dict = {}
superio_videos_list = []

csv_list = []
with open(csvPath, 'rt') as f:
    cr = csv.reader(f)
    for row in cr:
        csv_list.append(row)  # 将csvPath的csv文件内容读入列表，每行为其一个元素，元素也为list

csv_list.sort(key=lambda list: (list[0].split('_')[0], int(list[0].split('_')[1].split('-')[0]), int(list[0].split('_')[1].split('-')[1]), int(list[0].split('_')[1].split('-')[-1]), int(list[1]), int(list[7])))
#csv_list.sort(key=lambda list: (list[0].split('_')[0], int(list[0].split('_')[1]), int(list[1]), int(list[7])))

csv_list_tmp = []
for i in csv_list:
    csv_list_item_tmp = i
    video_id_tmp = i[0]
    clip_mid_time_tmp = i[1]
    clip_person_id_tmp = i[7]
    csv_list_item_tmp.append(video_id_tmp+'_'+clip_mid_time_tmp+'_'+clip_person_id_tmp)
    csv_list_tmp.append(csv_list_item_tmp)

csv_list_tmp_index = csv_list_tmp[0][8]
person_id_list = []
person_label_list = []
person_bbox_list = []

for i in csv_list_tmp:
    if i[8] != csv_list_tmp_index:
        per_target_annotations_dict['bounding_box'] = person_bbox_list_tmp
        per_target_annotations_dict['label'] = person_label_list
        per_target_annotations_dict['person_id'] = person_id_list
        labels_list.append({'index': csv_list_tmp_index.rsplit('_', 1)[0],
                            'bounding_box': per_target_annotations_dict['bounding_box'],
                            'label': per_target_annotations_dict['label'],
                            'person_id': per_target_annotations_dict['person_id']})
        csv_list_tmp_index = i[8]
        person_id_list = []
        person_label_list = []
        person_bbox_list = []
        person_id_list.append(int(i[7]))
        person_label_list.append(int(i[6])-1)
        person_bbox_list = [float(i[2]), float(i[3]), float(i[4]), float(i[5])]
        person_bbox_list_tmp = [float('{:.3f}'.format(k)) for k in person_bbox_list]
    else:
        person_id_list.append(int(i[7]))
        person_label_list.append(int(i[6])-1)
        person_bbox_list = [float(i[2]), float(i[3]), float(i[4]), float(i[5])]
        person_bbox_list_tmp = [float('{:.3f}'.format(k)) for k in person_bbox_list]

per_target_annotations_dict['bounding_box'] = person_bbox_list_tmp
per_target_annotations_dict['label'] = person_label_list
per_target_annotations_dict['person_id'] = person_id_list
labels_list.append({'index':  csv_list_tmp_index.rsplit('_', 1)[0],
                    'bounding_box': per_target_annotations_dict['bounding_box'],
                    'label': per_target_annotations_dict['label'],
                    'person_id': per_target_annotations_dict['person_id']})


labels_list_tmp_index = labels_list[0].get('index')
per_clip_labels_list = []
for i in labels_list:
    if i.get('index') != labels_list_tmp_index:
        video_dict.update({'video': labels_list_tmp_index.rsplit('_', 1)[0],
                           'time': int(labels_list_tmp_index.rsplit('_', 1)[1]),
                           'start_frame': int(labels_list_tmp_index.rsplit('_', 1)[1])*30+1-45,
                           'n_frames': 91,
                           'mid_frame': int(labels_list_tmp_index.rsplit('_', 1)[1])*30+1,
                           'format_str': 'image_%06d.jpg',
                           'frame_rate': 30.0,
                           'labels': per_clip_labels_list})
        superio_videos_list.append(deepcopy(video_dict))
        labels_list_tmp_index = i.get('index')
        per_clip_labels_list = []
        per_clip_labels_list.append({'bounding_box': i['bounding_box'],
                                     'label': i['label'],
                                     'person_id': i['person_id']})
    else:
        per_clip_labels_list.append({'bounding_box': i['bounding_box'],
                                     'label': i['label'],
                                     'person_id': i['person_id']})

video_dict.update({'video': labels_list_tmp_index.rsplit('_', 1)[0],
                   'time': int(labels_list_tmp_index.rsplit('_', 1)[1]),
                   'start_frame': int(labels_list_tmp_index.rsplit('_', 1)[1])*30+1-45,
                   'n_frames': 91,
                   'mid_frame': int(labels_list_tmp_index.rsplit('_', 1)[1])*30+1,
                   'format_str': 'image_%06d.jpg',
                   'frame_rate': 30.0,
                   'labels': per_clip_labels_list})
superio_videos_list.append(deepcopy(video_dict))

my_action_list = [
    {'name': 'stand', 'id': 1},
    {'name': 'sit', 'id': 2},
    {'name': 'walk', 'id': 3},
    {'name': 'bend over', 'id': 4},
    {'name': 'crouch down', 'id': 5},  
    {'name': 'climbing the pole or tower', 'id': 6},
    {'name': 'descending the pole or tower', 'id': 7},
    {'name': 'climbing the ladder', 'id': 8},
    {'name': 'descending the ladder', 'id': 9},
    {'name': 'assist in ladder climbing', 'id': 10},
    {'name': 'fasten the safety belt', 'id': 11},
    {'name': 'unfasten the safety belt', 'id': 12},
    {'name': 'drop', 'id': 13},
    {'name': 'lifting an object', 'id': 14},
    {'name': 'lowering an object', 'id': 15},
    {'name': 'pull or drag (a rope, etc)', 'id': 16},
    {'name': 'strike', 'id': 17},
    {'name': 'twist(a nut, etc)', 'id': 18},
    {'name': 'handover (a wrench, etc)', 'id': 19},
    {'name': 'receive (a pair of pliers, etc)', 'id': 20},
    {'name': 'swing (a hoe, etc)', 'id': 21},
    {'name': 'carry (a shovel, etc)', 'id': 22},
    {'name': 'place', 'id': 23},
    {'name': 'leap over', 'id': 24},
    {'name': 'cross through', 'id': 25},
    {'name': 'open(a door,etc)', 'id': 26},
    {'name': 'push', 'id': 27},
    {'name': 'wrap', 'id': 28},
    {'name': 'take', 'id': 29},
    {'name': 'wave', 'id': 30}
                  ]

#生成pkl文件
with open(targetPath, "wb") as pklfile:
    pickle.dump((superio_videos_list, my_action_list), pklfile)




