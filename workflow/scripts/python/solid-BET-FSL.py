# %% IMPORTS

import nibabel as nib
import dcm2niix
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os

# %% FOLDER PATHS

# Path to data
folder_path = '/Users/caryngeady/Documents/GitHub/Brain-Project/SOLID-DICOM'
# folder_path = '/Users/caryngeady/Documents/GitHub/Brain-Project/Glioma meDIP Dicoms'

# Get list of subfolders and corresponding patient IDs
patientIDs = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
imageFolders = [os.path.join(folder_path, patientID, f) for patientID in patientIDs for f in os.listdir(os.path.join(folder_path, patientID)) if os.path.isdir(os.path.join(folder_path, patientID, f)) or f.endswith('.zip')]
# %% UN-ZIP WHERE APPROPRIATE

# check if the folder in imageFolders is a path to a .zip file -- if it is, unzip it and remove the .zip file
# for i in range(len(imageFolders)):
#     if imageFolders[i].endswith('.zip'):
#         # create a subdirectory with the same name as the zip file (without the .zip extension)
#         subdir = os.path.join(os.path.dirname(imageFolders[i]), os.path.basename(imageFolders[i])[:-4])
#         os.makedirs(subdir, exist_ok=True)
#         # unzip the file into the subdirectory
#         subprocess.run(['unzip', imageFolders[i], '-d', subdir])
#         # remove the .zip file
#         os.remove(imageFolders[i])
#         # update the imageFolders list
#         imageFolders[i] = imageFolders[i][:-4]

# %% CONVERT TO NIFTI

folder_path = '/Users/caryngeady/Documents/GitHub/Brain-Project/out/images'

for i in range(len(imageFolders)):
    
    try:
        dcm_name  = os.path.basename(os.path.dirname(imageFolders[i])) + ' - ' + os.path.basename(imageFolders[i])
        # Run dcm2niix
        subprocess.run([
            'dcm2niix',
            '-z', 'y',  # Compress output file with gzip
            '-f', dcm_name,  # Output filename format
            '-o', folder_path,  # Output directory
            imageFolders[i]  # Input directory
        ])
    except:
        print(f"Error converting {imageFolders[i]}")

# %% GENERATE BRAIN MASK

# Steps:
# 1. Create a list of the nifti files
# 2. Perform skull-stripping on each nifti file
# 3. Using the skull-stripped nifti file, generate a brain mask (binary mask, where 1 = brain, 0 = background)

# Get list of nifti files
folder_path = '/Users/caryngeady/Documents/GitHub/Brain-Project/out/images'
mask_path = '/Users/caryngeady/Documents/GitHub/Brain-Project/out/masks'
nifti_files = [f for f in os.listdir(folder_path) if f.endswith('.nii.gz')]

# Brain extraction via FSL
fsl_dir = "/Users/caryngeady/fsl"
os.environ["FSLDIR"] = fsl_dir
os.environ["PATH"] += os.pathsep + os.path.join(fsl_dir, "bin")
subprocess.run(["bash", "-c", f". {os.path.join(fsl_dir, 'etc/fslconf/fsl.sh')}"])
os.environ["FSLOUTPUTTYPE"] = "NIFTI_GZ"

for nifti_file in nifti_files:
    try:
        image_file = os.path.join(folder_path,nifti_file) 
        mask_name = os.path.join(mask_path, os.path.basename(nifti_file)[:-7] + '_mask.nii.gz')
        subprocess.run(["bet", image_file, mask_name, "-f", "0.5", "-g", "0", "-m"])

    except:
        print(f"Error extracting brain from {nifti_file}")

# %% BIAS CORRECTION with FSL FAST

folder_path = '/Users/caryngeady/Documents/GitHub/Brain-Project/out/images'
nifti_files = [f for f in os.listdir(folder_path) if f.endswith('.nii.gz')]
bias_corrected_path = '/Users/caryngeady/Documents/GitHub/Brain-Project/out/bias_corrected'

for nifti_file in nifti_files:
    try:
        image_file = os.path.join(folder_path,nifti_file) 
        bias_corr_name = os.path.join(bias_corrected_path, os.path.basename(nifti_file)[:-7] + '_biascorr.nii.gz')
        subprocess.run(['fast', '-B', '-o', bias_corr_name, image_file])

    except:
        print(f"Error correcting bias in {nifti_file}")

# %% PREP FOR PYRADIOMICS FEATURE EXTRACTION

import pandas as pd

# Specify the directory paths for tumor masks and brain masks
path_to_project = '/Users/caryngeady/Documents/GitHub/Brain-Project'
path_to_label = 'SOLID-nii/masks'
path_to_image = 'SOLID-nii/bias_corrected'

# preallocate lists
study_list = [] # description of the study (all SOLID)
patient_list = [] # patient ID
label_list = [] # label of the ROI examined (all 1s)
date_list = [] # date the imaging was acquired
desc_list = [] # description of the imaging protocol
image_list = [] # path to the image
mask_list = [] # path to the mask

# get the list of nifti files
images = [f for f in os.listdir(os.path.join(path_to_project,path_to_image)) if f.endswith('biascorr_restore.nii.gz')]
masks = [f for f in os.listdir(os.path.join(path_to_project,path_to_label)) if f.endswith('_mask_mask.nii.gz')]

images[61] = 'SOLID-004_-_2019_APR_13_-_AXIAL_FLAIR+C_biascorr_restore.nii.gz'

# sort the lists in ascending order
images.sort()
masks.sort()

for i in range(len(images)):

    study_list.append('SOLID')
    patient_list.append(images[i].split('_-_')[0])
    label_list.append('1')
    date_list.append(images[i].split('_-_')[1])
    desc_list.append(images[i].split('_-_')[2][:-24])
    image_list.append(os.path.join(path_to_project,path_to_image,images[i]))
    mask_list.append(os.path.join(path_to_project,path_to_label,masks[i]))
    
pyrad_df = pd.DataFrame({'Study':study_list,'Patient':patient_list,'Label':label_list,'Date':date_list,'Description':desc_list,'Image':image_list,'Mask':mask_list})
pyrad_df.to_csv('pyrad-solid.csv',index=False)

# %%
