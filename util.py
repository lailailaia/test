import numpy as np
import nibabel as nib
import os


# 切块
def cut_block(nii_filepath):
    # nii = nib.load('F:/swmADNI_941_S_1203_MR_MPR__GradWarp__B1_Correction_Br_20070801201750736_S25671_I63880.nii')
    nii = nib.load(nii_filepath)
    image = nii.get_fdata()
    image_pad = np.pad(image, pad_width=((2, 2), (2, 3), (2, 2)), mode='constant', constant_values=(0, 0))
    block_list = []
    for l in range(0, image_pad.shape[0], 25):
        for w in range(0, image_pad.shape[1], 25):
            if w == 10:
                print(50)
            for h in range(0, image_pad.shape[2], 25):
                temporary_block = image_pad[l:l + 25, w:w + 25, h:h + 25]
                block_list.append(temporary_block)
    return block_list


# 保存每个样本切好的块，save_path文件夹路径，filename_文件名，block_list块名
def save_block_list(save_path, filename, block_list):
    for i in range(len(block_list)):
        folder_path = os.path.join(save_path, 'block' + str(i))
        if not os.path.exists(folder_path):  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(folder_path)
        # filepath = save_path + str(i)
        filepath = os.path.join(folder_path, filename + "_" + str(i))
        np.save(filepath, block_list[i])


# 保存所有的文件,fileDir所要读取的nii文件夹，saveDir保存的文件夹
def save_all_nii_block(fileDir, saveDir):
    for file in os.listdir(fileDir):
        file_name = fileDir + "/" + file
        block_list = cut_block(file_name)
        save_block_list(save_path=saveDir, filename=file, block_list=block_list)


if __name__ == "__main__":
    root_filepath = '/userdata/All_Data_Set/ADNI/MRI_509data/postprocessing/MClc'
    save_Dir = '/userdata/sharedata/x_cut_block/MClc'
    save_all_nii_block(root_filepath, save_Dir)
