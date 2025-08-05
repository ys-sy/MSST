import os
import shutil
import sys


#传入raw_frames文件夹路径
raw_frames_dir = str(sys.argv[1])

#传入videos_key_frames文件夹路径
videos_key_frames_dir = str(sys.argv[2])

#传入videos_middle_key_frames文件夹路径
videos_middle_key_frames_dir = str(sys.argv[3])

#传入all_key_frames文件夹路径
all_key_frames_dir = str(sys.argv[4])


#获取子文件夹的路径
subfile = os.listdir(raw_frames_dir)
for i in subfile:
    imagelist = os.listdir(raw_frames_dir + "/" + i)
    num_imagelist = len(imagelist)
    nun_keyframes = num_imagelist//30
    # 获取关键帧编号
    keyframesnum = range(0, nun_keyframes)
    middlekeyframesnum = range(2, nun_keyframes-2)
    if not os.path.exists(videos_key_frames_dir + "/" + i):
        os.mkdir(videos_key_frames_dir + "/" + i)
    if not os.path.exists(videos_middle_key_frames_dir + "/" + i):
        os.mkdir(videos_middle_key_frames_dir + "/" + i)

    
    #将所有视频关键帧复制到all_key_frames文件夹下
    #将每个视频关键帧复制到videos_key_frames文件夹下，每个视频对应一个子文件夹用于存放该视频的关键帧
    #文件名会包含对应视频的关键帧数量
    for j in keyframesnum:
        temp_num = str(j*30+1).zfill(6)
        srcfile = raw_frames_dir + "/" + i + '/' + 'image_' + temp_num + '.jpg'
        dstpath1 = all_key_frames_dir + "/" + i + '_'+str(nun_keyframes)+'_image_' + temp_num + '.jpg'
        dstpath2 = videos_key_frames_dir + "/"  + i + '/' + i + '_'+str(nun_keyframes)+'_image_' + temp_num + '.jpg'
        # 复制文件
        shutil.copy(srcfile, dstpath1)
        shutil.copy(srcfile, dstpath2)
        
    for j in middlekeyframesnum:
        temp_num = str(j*30+1).zfill(6)
        
        srcfile = raw_frames_dir + "/" + i + '/' + 'image_' + temp_num + '.jpg'
        dstpath3 = videos_middle_key_frames_dir + "/"  + i + '/' + i + '_'+str(nun_keyframes)+'_image_' + temp_num + '.jpg'
        # 复制文件
        shutil.copy(srcfile, dstpath3)
        
    
