#!/usr/bin/env python3
import fire
import logging
import os, sys, traceback
from spIsoNet.util.dict2attr import Arg,check_parse,idx2list
from fire import core
from spIsoNet.util.metadata import MetaData,Label,Item

class ISONET:
    """
    ISONET: Train on tomograms and restore missing-wedge\n
    for detail discription, run one of the following commands:


    spisonet.py fsc3d -h
    spisonet.py map_refine -h
    """
    # spisonet.py prepare_star -h
    # spisonet.py prepare_subtomo_star -h
    # spisonet.py deconv -h
    # spisonet.py make_mask -h
    # spisonet.py extract -h
    # spisonet.py refine -h
    # spisonet.py predict -h
    # spisonet.py resize -h
    #log_file = "log.txt"

    # def prepare_star(self,folder_name, output_star='tomograms.star',pixel_size = 10.0, defocus = 0.0, number_subtomos = 100):
    #     """
    #     \nThis command generates a tomograms.star file from a folder containing only tomogram files (.mrc or .rec).\n
    #     spisonet.py prepare_star folder_name [--output_star] [--pixel_size] [--defocus] [--number_subtomos]
    #     :param folder_name: (None) directory containing tomogram(s). Usually 1-5 tomograms are sufficient.
    #     :param output_star: (tomograms.star) star file similar to that from "relion". You can modify this file manually or with gui.
    #     :param pixel_size: (10) pixel size in anstroms. Usually you want to bin your tomograms to about 10A pixel size.
    #     Too large or too small pixel sizes are not recommanded, since the target resolution on Z-axis of corrected tomograms should be about 30A.
    #     :param defocus: (0.0) defocus in Angstrom. Only need for ctf deconvolution. For phase plate data, you can leave defocus 0.
    #     If you have multiple tomograms with different defocus, please modify them in star file or with gui.
    #     :param number_subtomos: (100) Number of subtomograms to be extracted in later processes.
    #     If you want to extract different number of subtomograms in different tomograms, you can modify them in the star file generated with this command or with gui.

    #     """
    #     md = MetaData()
    #     md.addLabels('rlnIndex','rlnMicrographName','rlnPixelSize','rlnDefocus','rlnNumberSubtomo','rlnMaskBoundary')
    #     tomo_list = sorted(os.listdir(folder_name))
    #     i = 0
    #     for tomo in tomo_list:
    #         if tomo[-4:] == '.rec' or tomo[-4:] == '.mrc':
    #             i+=1
    #             it = Item()
    #             md.addItem(it)
    #             md._setItemValue(it,Label('rlnIndex'),str(i))
    #             md._setItemValue(it,Label('rlnMicrographName'),os.path.join(folder_name,tomo))
    #             md._setItemValue(it,Label('rlnPixelSize'),pixel_size)
    #             md._setItemValue(it,Label('rlnDefocus'),defocus)
    #             md._setItemValue(it,Label('rlnNumberSubtomo'),number_subtomos)
    #             md._setItemValue(it,Label('rlnMaskBoundary'),None)
    #     md.write(output_star)

    # def prepare_subtomo_star(self, folder_name, output_star='subtomo.star', pixel_size: float=10.0, cube_size = None):
    #     """
    #     \nThis command generates a subtomo star file from a folder containing only subtomogram files (.mrc).
    #     This command is usually not necessary in the traditional workflow, because "spisonet.py extract" will generate this subtomo.star for you.\n
    #     spisonet.py prepare_subtomo_star folder_name [--output_star] [--cube_size]
    #     :param folder_name: (None) directory containing subtomogram(s).
    #     :param output_star: (subtomo.star) output star file for subtomograms, will be used as input in refinement.
    #     :param pixel_size: (10) The pixel size in angstrom of your subtomograms.
    #     :param cube_size: (None) This is the size of the cubic volumes used for training. This values should be smaller than the size of subtomogram.
    #     And the cube_size should be divisible by 8. If this value isn't set, cube_size is automatically determined as int(subtomo_size / 1.5 + 1)//16 * 16
    #     """
    #     #TODO check folder valid, logging
    #     if not os.path.isdir(folder_name):
    #         print("the folder does not exist")
    #     import mrcfile
    #     md = MetaData()
    #     md.addLabels('rlnSubtomoIndex','rlnImageName','rlnCubeSize','rlnCropSize','rlnPixelSize')
    #     subtomo_list = sorted(os.listdir(folder_name))
    #     for i,subtomo in enumerate(subtomo_list):
    #         subtomo_name = os.path.join(folder_name,subtomo)
    #         try:
    #             with mrcfile.open(subtomo_name, mode='r') as s:
    #                 crop_size = s.header.nx
    #         except:
    #             print("Warning: Can not process the subtomogram: {}!".format(subtomo_name))
    #             continue
    #         if cube_size is not None:
    #             cube_size = int(cube_size)
    #             if cube_size >= crop_size:
    #                 cube_size = int(crop_size / 1.5 + 1)//16 * 16
    #                 print("Warning: Cube size should be smaller than the size of subtomogram volume! Using cube size {}!".format(cube_size))
    #         else:
    #             cube_size = int(crop_size / 1.5 + 1)//16 * 16
    #         it = Item()
    #         md.addItem(it)
    #         md._setItemValue(it,Label('rlnSubtomoIndex'),str(i+1))
    #         md._setItemValue(it,Label('rlnImageName'),subtomo_name)
    #         md._setItemValue(it,Label('rlnCubeSize'),cube_size)
    #         md._setItemValue(it,Label('rlnCropSize'),crop_size)
    #         md._setItemValue(it,Label('rlnPixelSize'),pixel_size)

    #         # f.write(str(i+1)+' ' + os.path.join(folder_name,tomo) + '\n')
    #     md.write(output_star)

    # def deconv(self, star_file: str,
    #     deconv_folder:str="./deconv",
    #     snrfalloff: float=None,
    #     deconvstrength: float=None,
    #     highpassnyquist: float=0.02,
    #     chunk_size: int=None,
    #     overlap_rate: float= 0.25,
    #     ncpu:int=4,
    #     tomo_idx: str=None):
    #     """
    #     \nCTF deconvolution for the tomograms.\n
    #     spisonet.py deconv star_file [--deconv_folder] [--snrfalloff] [--deconvstrength] [--highpassnyquist] [--overlap_rate] [--ncpu] [--tomo_idx]
    #     This step is recommanded because it enhances low resolution information for a better contrast. No need to do deconvolution for phase plate data.
    #     :param deconv_folder: (./deconv) Folder created to save deconvoluted tomograms.
    #     :param star_file: (None) Star file for tomograms.
    #     :param snrfalloff: (1.0) SNR fall rate with the frequency. High values means losing more high frequency.
    #     If this value is not set, the program will look for the parameter in the star file.
    #     If this value is not set and not found in star file, the default value 1.0 will be used.
    #     :param deconvstrength: (1.0) Strength of the deconvolution.
    #     If this value is not set, the program will look for the parameter in the star file.
    #     If this value is not set and not found in star file, the default value 1.0 will be used.
    #     :param highpassnyquist: (0.02) Highpass filter for at very low frequency. We suggest to keep this default value.
    #     :param chunk_size: (None) When your computer has enough memory, please keep the chunk_size as the default value: None . Otherwise, you can let the program crop the tomogram into multiple chunks for multiprocessing and assembly them into one. The chunk_size defines the size of individual chunk. This option may induce artifacts along edges of chunks. When that happen, you may use larger overlap_rate.
    #     :param overlap_rate: (None) The overlapping rate for adjecent chunks.
    #     :param ncpu: (4) Number of cpus to use.
    #     :param tomo_idx: (None) If this value is set, process only the tomograms listed in this index. e.g. 1,2,4 or 5-10,15,16
    #     """
    #     from spIsoNet.util.deconvolution import deconv_one

    #     logging.basicConfig(format='%(asctime)s, %(levelname)-8s %(message)s',
    #     datefmt="%m-%d %H:%M:%S",level=logging.INFO,handlers=[logging.StreamHandler(sys.stdout)])
    #     logging.info('\n######Isonet starts ctf deconvolve######\n')

    #     try:
    #         md = MetaData()
    #         md.read(star_file)
    #         if not 'rlnSnrFalloff' in md.getLabels():
    #             md.addLabels('rlnSnrFalloff','rlnDeconvStrength','rlnDeconvTomoName')
    #             for it in md:
    #                 md._setItemValue(it,Label('rlnSnrFalloff'),1.0)
    #                 md._setItemValue(it,Label('rlnDeconvStrength'),1.0)
    #                 md._setItemValue(it,Label('rlnDeconvTomoName'),None)

    #         if not os.path.isdir(deconv_folder):
    #             os.mkdir(deconv_folder)

    #         tomo_idx = idx2list(tomo_idx)
    #         for it in md:
    #             if tomo_idx is None or str(it.rlnIndex) in tomo_idx:
    #                 if snrfalloff is not None:
    #                     md._setItemValue(it,Label('rlnSnrFalloff'), snrfalloff)
    #                 if deconvstrength is not None:
    #                     md._setItemValue(it,Label('rlnDeconvStrength'),deconvstrength)

    #                 tomo_file = it.rlnMicrographName
    #                 base_name = os.path.basename(tomo_file)
    #                 deconv_tomo_name = '{}/{}'.format(deconv_folder,base_name)

    #                 deconv_one(it.rlnMicrographName,deconv_tomo_name,defocus=it.rlnDefocus/10000.0, pixel_size=it.rlnPixelSize,snrfalloff=it.rlnSnrFalloff, deconvstrength=it.rlnDeconvStrength,highpassnyquist=highpassnyquist,chunk_size=chunk_size,overlap_rate=overlap_rate,ncpu=ncpu)
    #                 md._setItemValue(it,Label('rlnDeconvTomoName'),deconv_tomo_name)
    #             md.write(star_file)
    #         logging.info('\n######Isonet done ctf deconvolve######\n')

    #     except Exception:
    #         error_text = traceback.format_exc()
    #         f =open('log.txt','a+')
    #         f.write(error_text)
    #         f.close()
    #         logging.error(error_text)

    # def make_mask(self,star_file,
    #             mask_folder: str = 'mask',
    #             patch_size: int=4,
    #             mask_boundary: str=None,
    #             density_percentage: int=None,
    #             std_percentage: int=None,
    #             use_deconv_tomo:bool=True,
    #             z_crop:float=None,
    #             tomo_idx=None):
    #     """
    #     \ngenerate a mask that include sample area and exclude "empty" area of the tomogram. The masks do not need to be precise. In general, the number of subtomograms (a value in star file) should be lesser if you masked out larger area. \n
    #     spisonet.py make_mask star_file [--mask_folder] [--patch_size] [--density_percentage] [--std_percentage] [--use_deconv_tomo] [--tomo_idx]
    #     :param star_file: path to the tomogram or tomogram folder
    #     :param mask_folder: path and name of the mask to save as
    #     :param patch_size: (4) The size of the box from which the max-filter and std-filter are calculated.
    #     :param density_percentage: (50) The approximate percentage of pixels to keep based on their local pixel density.
    #     If this value is not set, the program will look for the parameter in the star file.
    #     If this value is not set and not found in star file, the default value 50 will be used.
    #     :param std_percentage: (50) The approximate percentage of pixels to keep based on their local standard deviation.
    #     If this value is not set, the program will look for the parameter in the star file.
    #     If this value is not set and not found in star file, the default value 50 will be used.
    #     :param use_deconv_tomo: (True) If CTF deconvolved tomogram is found in tomogram.star, use that tomogram instead.
    #     :param z_crop: If exclude the top and bottom regions of tomograms along z axis. For example, "--z_crop 0.2" will mask out the top 20% and bottom 20% region along z axis.
    #     :param tomo_idx: (None) If this value is set, process only the tomograms listed in this index. e.g. 1,2,4 or 5-10,15,16
    #     """
    #     from spIsoNet.bin.make_mask import make_mask
    #     logging.basicConfig(format='%(asctime)s, %(levelname)-8s %(message)s',
    #     datefmt="%m-%d %H:%M:%S",level=logging.INFO,handlers=[logging.StreamHandler(sys.stdout)])
    #     logging.info('\n######Isonet starts making mask######\n')
    #     try:
    #         if not os.path.isdir(mask_folder):
    #             os.mkdir(mask_folder)
    #         # write star percentile threshold
    #         md = MetaData()
    #         md.read(star_file)
    #         if not 'rlnMaskDensityPercentage' in md.getLabels():
    #             md.addLabels('rlnMaskDensityPercentage','rlnMaskStdPercentage','rlnMaskName')
    #             for it in md:
    #                 md._setItemValue(it,Label('rlnMaskDensityPercentage'),50)
    #                 md._setItemValue(it,Label('rlnMaskStdPercentage'),50)
    #                 md._setItemValue(it,Label('rlnMaskName'),None)

    #         tomo_idx = idx2list(tomo_idx)
    #         for it in md:
    #             if tomo_idx is None or str(it.rlnIndex) in tomo_idx:
    #                 if density_percentage is not None:
    #                     md._setItemValue(it,Label('rlnMaskDensityPercentage'),density_percentage)
    #                 if std_percentage is not None:
    #                     md._setItemValue(it,Label('rlnMaskStdPercentage'),std_percentage)
    #                 if use_deconv_tomo and "rlnDeconvTomoName" in md.getLabels() and it.rlnDeconvTomoName not in [None,'None']:
    #                     tomo_file = it.rlnDeconvTomoName
    #                 else:
    #                     tomo_file = it.rlnMicrographName
    #                 tomo_root_name = os.path.splitext(os.path.basename(tomo_file))[0]

    #                 if os.path.isfile(tomo_file):
    #                     logging.info('make_mask: {}| dir_to_save: {}| percentage: {}| window_scale: {}'.format(tomo_file,
    #                     mask_folder, it.rlnMaskDensityPercentage, patch_size))
                        
    #                     #if mask_boundary is None:
    #                     if "rlnMaskBoundary" in md.getLabels() and it.rlnMaskBoundary not in [None, "None"]:
    #                         mask_boundary = it.rlnMaskBoundary 
    #                     else:
    #                         mask_boundary = None
                              
    #                     mask_out_name = '{}/{}_mask.mrc'.format(mask_folder,tomo_root_name)
    #                     make_mask(tomo_file,
    #                             mask_out_name,
    #                             mask_boundary=mask_boundary,
    #                             side=patch_size,
    #                             density_percentage=it.rlnMaskDensityPercentage,
    #                             std_percentage=it.rlnMaskStdPercentage,
    #                             surface = z_crop)

    #                 md._setItemValue(it,Label('rlnMaskName'),mask_out_name)
    #             md.write(star_file)
    #         logging.info('\n######Isonet done making mask######\n')
    #     except Exception:
    #         error_text = traceback.format_exc()
    #         f =open('log.txt','a+')
    #         f.write(error_text)
    #         f.close()
    #         logging.error(error_text)

    # def extract(self,
    #     star_file: str,
    #     use_deconv_tomo: bool = True,
    #     subtomo_folder: str = "subtomo",
    #     subtomo_star: str = "subtomo.star",
    #     cube_size: int = 80,
    #     crop_size: int = None,
    #     log_level: str="info",
    #     tomo_idx = None
    #     ):

    #     """
    #     \nExtract subtomograms\n
    #     spisonet.py extract star_file [--subtomo_folder] [--subtomo_star] [--cube_size] [--use_deconv_tomo] [--tomo_idx]
    #     :param star_file: tomogram star file
    #     :param subtomo_folder: (subtomo) folder for output subtomograms.
    #     :param subtomo_star: (subtomo.star) star file for output subtomograms.
    #     :param cube_size: (80) Size of cubes for training, should be divisible by 8, eg. 32, 64. The actual sizes of extracted subtomograms are this value adds 16.
    #     :param crop_size: (None) The size of subtomogram, should be larger then the cube_size The default value is 16+cube_size.
    #     :param log_level: ("info") level of the output, either "info" or "debug"
    #     :param use_deconv_tomo: (True) If CTF deconvolved tomogram is found in tomogram.star, use that tomogram instead.
    #     """
    #     d = locals()
    #     d_args = Arg(d)

    #     if d_args.log_level == "debug":
    #         logging.basicConfig(format='%(asctime)s, %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
    #         ,datefmt="%H:%M:%S",level=logging.DEBUG,handlers=[logging.StreamHandler(sys.stdout)])
    #     else:
    #         logging.basicConfig(format='%(asctime)s, %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
    #         ,datefmt="%m-%d %H:%M:%S",level=logging.INFO,handlers=[logging.StreamHandler(sys.stdout)])

    #     logging.info("\n######Isonet starts extracting subtomograms######\n")

    #     try:
    #         if os.path.isdir(subtomo_folder):
    #             logging.warning("subtomo directory exists, the current directory will be overwriten")
    #             import shutil
    #             shutil.rmtree(subtomo_folder)
    #         os.mkdir(subtomo_folder)

    #         from spIsoNet.preprocessing.prepare import extract_subtomos
    #         if crop_size is None:
    #             d_args.crop_size = cube_size + 16
    #         else:
    #             d_args.crop_size = crop_size
    #         d_args.subtomo_dir = subtomo_folder
    #         d_args.tomo_idx = idx2list(tomo_idx)
    #         extract_subtomos(d_args)
    #         logging.info("\n######Isonet done extracting subtomograms######\n")
    #     except Exception:
    #         error_text = traceback.format_exc()
    #         f =open('log.txt','a+')
    #         f.write(error_text)
    #         f.close()
    #         logging.error(error_text)


    # def refine(self,
    #     subtomo_star: str,
    #     gpuID: str = None,
    #     iterations: int = None,
    #     data_dir: str = None,
    #     pretrained_model: str = None,
    #     log_level: str = None,
    #     result_dir: str='results',
    #     remove_intermediate: bool =True,
    #     select_subtomo_number: int = None,
    #     ncpus: int = 16,
    #     continue_from: str=None,
    #     epochs: int = 10,
    #     batch_size: int = None,
    #     steps_per_epoch: int = None,

    #     noise_level:  tuple=(0.05,0.10,0.15,0.20),
    #     noise_start_iter: tuple=(11,16,21,26),
    #     noise_mode: str = None,
    #     noise_dir: str = None,
    #     learning_rate: float = 0.0003,

    #     mixed_precision: bool = True,
    #     normalize_percentile: bool = True,

    #     acc_batches: int = 1

    # ):
    #     """
    #     \ntrain neural network to correct missing wedge\n
    #     spisonet.py refine subtomo_star [--iterations] [--gpuID] [--preprocessing_ncpus] [--batch_size] [--steps_per_epoch] [--noise_start_iter] [--noise_level]...
    #     :param subtomo_star: (None) star file containing subtomogram(s).
    #     :param gpuID: (0,1,2,3) The ID of gpu to be used during the training. e.g 0,1,2,3.
    #     :param pretrained_model: (None) A trained neural network model in ".h5" format to start with.
    #     :param iterations: (30) Number of training iterations.
    #     :param data_dir: (data) Temperary folder to save the generated data used for training.
    #     :param log_level: (info) debug level, could be 'info' or 'debug'
    #     :param continue_from: (None) A Json file to continue from. That json file is generated at each iteration of refine.
    #     :param result_dir: ('results') The name of directory to save refined neural network models and subtomograms
    #     :param ncpus: (16) Number of cpu for preprocessing.

    #     ************************Training settings************************

    #     :param epochs: (10) Number of epoch for each iteraction.
    #     :param batch_size: (None) Size of the minibatch.If None, batch_size will be the max(2 * number_of_gpu,4). batch_size should be divisible by the number of gpu.
    #     :param steps_per_epoch: (None) Step per epoch. If not defined, the default value will be min(num_of_subtomograms * 8 / batch_size , 200)

    #     ************************Denoise settings************************

    #     :param noise_level: (0.05,0.1,0.15,0.2) Level of noise STD(added noise)/STD(data) after the iteration defined in noise_start_iter.
    #     :param noise_start_iter: (11,16,21,26) Iteration that start to add noise of corresponding noise level.
    #     :param noise_mode: (None) Filter names when generating noise volumes, can be 'ramp', 'hamming' and 'noFilter'
    #     :param noise_dir: (None) Directory for generated noise volumes. If set to None, the Noise volumes should appear in results/training_noise

    #     ************************Network settings************************

    #     :param learning_rate: (0.0003) learning rate for network training.
    #     :param normalize_percentile: (True) Normalize the 5 percent and 95 percent pixel intensity to 0 and 1 respectively. If this is set to False, normalize the input to 0 mean and 1 standard dievation.
    #     :param acc_batches: If this value is set to 2 (or more), accumulate gradiant will be used to save memory consumption.  Please make sure batches size is equal to or divisible by acc_batches * number_of_GPU 
    #     """
    #     from spIsoNet.bin.refine import run
    #     d = locals()
    #     d_args = Arg(d)
    #     with open('log.txt','a+') as f:
    #         f.write(' '.join(sys.argv[0:]) + '\n')
    #     run(d_args)

    def map_refine(self, 
                   input: str,
                   aniso_file: str, 
                   mask: str=None, 

                   gpuID: str=None, 
                   alpha: float=1,
                   ncpus: int=16, 
                   output_dir: str="isonet_maps",
                   pretrained_model: str=None,

                   epochs: int=50,
                   n_subvolume: int=1000, 
                   cube_size: int=64,
                   predict_crop_size: int=80,
                   batch_size: int=None, 
                   acc_batches: int=1,
                   learning_rate: float=3e-4
                   ):

        """
        \ntrain neural network to correct preffered orientation\n
        spisonet.py map_refine half1.mrc half2.mrc mask.mrc [--gpuID] [--ncpus] [--output_dir] [--fsc_file]...
        :param input: Input name of half1
        :param mask: Filename of a user-provided mask
        :param gpuID: The ID of gpu to be used during the training.
        :param ncpus: Number of cpu.
        :param output_dir: The name of directory to save output maps
        :param fsc_file: 3DFSC file if not set, isonet will generate one.
        :param epochs: Number of epochs for each iteration. This value can be increase (maybe to 10) to get (maybe) better result.
        :param n_subvolume: Number of subvolumes 
        :param predict_crop_size: The size of subvolumes, should be larger then the cube_size
        :param cube_size: Size of cubes for training, should be divisible by 16, e.g. 32, 64, 80.
        :param batch_size: Size of the minibatch. If None, batch_size will be the max(2 * number_of_gpu,4). batch_size should be divisible by the number of gpu.
        :param acc_batches: If this value is set to 2 (or more), accumulate gradiant will be used to save memory consumption.  
        :param learning_rate: learning rate. Default learning rate is 3e-4 while previous spIsoNet tomography used 3e-4 as learning rate
        """
        #TODO
        #mixed precision does not work for torch.FFT
        mixed_precision = False

        from spIsoNet.util.utils import mkfolder
        from spIsoNet.preprocessing.img_processing import normalize
        from spIsoNet.bin.map_refine import map_refine
        from spIsoNet.util.utils import process_gpuID
        from multiprocessing import cpu_count
        import mrcfile
        import numpy as np

        logging.basicConfig(format='%(asctime)s, %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
            ,datefmt="%H:%M:%S",level=logging.DEBUG,handlers=[logging.StreamHandler(sys.stdout)])   
        ngpus, gpuID, gpuID_list = process_gpuID(gpuID)


        os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"]=gpuID

        if batch_size is None:
            if ngpus == 1:
                batch_size = 4
            else:
                batch_size = 2 * len(gpuID_list)

        cpu_system = cpu_count()
        if cpu_system < ncpus:
            logging.info("requested number of cpus is more than the number of the cpu cores in the system")
            logging.info(f"setting ncpus to {cpu_system}")
            ncpus = cpu_system

        mkfolder(output_dir,remove=False)

        output_base = input.split('/')[-1]
        output_base = output_base.split('.')[:-1]
        output_base = "".join(output_base)

        with mrcfile.open(input, 'r') as mrc:
            half_map = normalize(mrc.data,percentile=False)
            voxel_size = mrc.voxel_size.x
            if voxel_size == 0:
                voxel_size = 1
        logging.info("voxel_size {}".format(voxel_size))

        if mask is None:
            mask_vol = np.ones(half_map.shape, dtype = np.float32)
            logging.warning("No mask is provided, please consider providing a soft mask")
        else:
            with mrcfile.open(mask, 'r') as mrc:
                mask_vol = mrc.data

        with mrcfile.open(aniso_file, 'r') as mrc:
            fsc3d = mrc.data

        map_refine(half_map, mask_vol, fsc3d, alpha = alpha,  voxel_size=voxel_size, output_dir=output_dir, 
                   output_base=output_base, mixed_precision=mixed_precision, epochs = epochs,
                   n_subvolume=n_subvolume, cube_size=cube_size, pretrained_model=pretrained_model,
                   batch_size = batch_size, acc_batches = acc_batches,predict_crop_size=predict_crop_size,gpuID=gpuID, learning_rate=learning_rate)
        
        logging.info("removing intermediate files")
        files = os.listdir(output_dir)
        import shutil
        for item in files:
            if item == "data" or item == "data~":
                path = f'{output_dir}/{item}'
                shutil.rmtree(path)
            if item.startswith('subvolume') or item == "tmp.npy":
                path = f'{output_dir}/{item}'
                os.remove(path)
        logging.info("Finished")

    def fsc3d(self, 
                   i: str,
                   i2: str, 
                   mask: str=None, 
                   o: str="FSC3D.mrc",
                   ncpus: int=16, 
                   limit_res: float=None, 
                   cone_sampling_angle: float=10,
                   ):

        """
        \ntrain neural network to correct preffered orientation\n
        spisonet.py map_refine half1.mrc half2.mrc mask.mrc [--gpuID] [--ncpus] [--output_dir] [--fsc_file]...
        :param i: Input name of half1
        :param i2: Input name of half2
        :param mask: Filename of a user-provided mask
        :param ncpus: Number of cpu.
        :param limit_res: The resolution limit for recovery, default is the resolution of the map.
        :param fsc_file: 3DFSC file if not set, isonet will generate one.
        :param cone_sampling_angle: Angle for 3D fsc sampling for spIsoNet generated 3DFSC. spIsoNet default is 10 degrees, the default for official 3DFSC is 20 degrees.
        """
        logging.basicConfig(format='%(asctime)s, %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
            ,datefmt="%H:%M:%S",level=logging.DEBUG,handlers=[logging.StreamHandler(sys.stdout)])   

        from spIsoNet.preprocessing.img_processing import normalize
        import numpy as np
        from multiprocessing import cpu_count
        import mrcfile

        from spIsoNet.util.FSC import get_FSC_map, ThreeD_FSC, recommended_resolution

        cpu_system = cpu_count()
        if cpu_system < ncpus:
            logging.info("requested number of cpus is more than the number of the cpu cores in the system")
            logging.info(f"setting ncpus to {cpu_system}")
            ncpus = cpu_system

        with mrcfile.open(i, 'r') as mrc:
            half1 = normalize(mrc.data,percentile=False)
            voxel_size = mrc.voxel_size.x
            if voxel_size == 0:
                voxel_size = 1

        with mrcfile.open(i2, 'r') as mrc:
            half2 = normalize(mrc.data,percentile=False)


        if mask is None:
            mask_vol = np.ones(half1.shape, dtype = np.float32)
            logging.warning("No mask is provided, please consider providing a soft mask")
        else:
            with mrcfile.open(mask, 'r') as mrc:
                mask_vol = mrc.data

        FSC_map = get_FSC_map([half1, half2], mask_vol)
        if limit_res is None:
            limit_res = recommended_resolution(FSC_map, voxel_size, threshold=0.143)
            logging.info("Global resolution at FSC={} is {}".format(0.143, limit_res))

        limit_r = int( (2.*voxel_size) / limit_res * (half1.shape[0]/2.) + 1)
        logging.info("Limit resolution to {} for spIsoNet 3D calculation. You can also tune this paramerter with --limit_res .".format(limit_res))

        logging.info("calculating fast 3DFSC, this will take few minutes")
        fsc3d = ThreeD_FSC(FSC_map, limit_r,angle=float(cone_sampling_angle), n_processes=ncpus)

        with mrcfile.new(o, overwrite=True) as mrc:
            mrc.set_data(fsc3d.astype(np.float32))
        logging.info("voxel_size {}".format(voxel_size))


         





    '''
    def map_refine_multi(self, half1_file, half2_file, mask_file, fsc_file, limit_res, output_dir="isonet_maps", gpuID=0, n_subvolume=50, crop_size=96, cube_size=64, weighting=False):
        logging.basicConfig(format='%(asctime)s, %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
            ,datefmt="%H:%M:%S",level=logging.DEBUG,handlers=[logging.StreamHandler(sys.stdout)])
        half1_list = half1_file.split(',')
        print(half1_list)
        half2_list = half2_file.split(',')
        mask_list = mask_file.split(',')
        import mrcfile
        half1 = []
        half2 = []
        mask = []
        for half1_file in half1_list:
            with mrcfile.open(half1_file, 'r') as mrc:
                half1.append(mrc.data)
                voxel_size = mrc.voxel_size.x
        for half2_file in half2_list:
            with mrcfile.open(half2_file, 'r') as mrc:
                half2.append(mrc.data)
        for mask_file in mask_list:
            with mrcfile.open(mask_file, 'r') as mrc:
                mask.append(mrc.data)
        with mrcfile.open(fsc_file, 'r') as mrc:
            fsc3d = mrc.data
        logging.info("voxel_size {}".format(voxel_size))
        from spIsoNet.bin.map_refine import map_refine_multi
        from spIsoNet.util.utils import mkfolder
        mkfolder(output_dir)
        logging.info("processing half map1")
        map_refine_multi(half1, mask, fsc3d, voxel_size=voxel_size, limit_res = limit_res, output_dir = output_dir, output_base="half1", weighting = weighting, n_subvolume = n_subvolume, cube_size = cube_size, crop_size = crop_size)
        logging.info("processing half map2")
        map_refine_multi(half2, mask, fsc3d, voxel_size=voxel_size, limit_res = limit_res, output_dir = output_dir, output_base="half2", weighting = weighting, n_subvolume = n_subvolume, cube_size = cube_size, crop_size = crop_size)
        logging.info("Two independent half maps are saved in {}. Please use other software for postprocessing and try difference B factors".format(output_dir))
    '''

    # def predict(self, star_file: str, model: str, output_dir: str='./corrected_tomos', gpuID: str = None, cube_size:int=64,
    # crop_size:int=96,use_deconv_tomo=True, batch_size:int=None,normalize_percentile: bool=True,log_level: str="info", tomo_idx=None):
    #     """
    #     \nPredict tomograms using trained model\n
    #     spisonet.py predict star_file model [--gpuID] [--output_dir] [--cube_size] [--crop_size] [--batch_size] [--tomo_idx]
    #     :param star_file: star for tomograms.
    #     :param output_dir: file_name of output predicted tomograms
    #     :param model: path to trained network model .h5
    #     :param gpuID: (0,1,2,3) The gpuID to used during the training. e.g 0,1,2,3.
    #     :param cube_size: (64) The tomogram is divided into cubes to predict due to the memory limitation of GPUs.
    #     :param crop_size: (96) The side-length of cubes cropping from tomogram in an overlapping patch strategy, make this value larger if you see the patchy artifacts
    #     :param batch_size: The batch size of the cubes grouped into for network predicting, the default parameter is four times number of gpu
    #     :param normalize_percentile: (True) if normalize the tomograms by percentile. Should be the same with that in refine parameter.
    #     :param log_level: ("debug") level of message to be displayed, could be 'info' or 'debug'
    #     :param tomo_idx: (None) If this value is set, process only the tomograms listed in this index. e.g. 1,2,4 or 5-10,15,16
    #     :param use_deconv_tomo: (True) If CTF deconvolved tomogram is found in tomogram.star, use that tomogram instead.
    #     :raises: AttributeError, KeyError
    #     """
    #     d = locals()
    #     d_args = Arg(d)
    #     from spIsoNet.bin.predict import predict

    #     if d_args.log_level == "debug":
    #         logging.basicConfig(format='%(asctime)s, %(levelname)-8s %(message)s',
    #         datefmt="%m-%d %H:%M:%S",level=logging.DEBUG,handlers=[logging.StreamHandler(sys.stdout)])
    #     else:
    #         logging.basicConfig(format='%(asctime)s, %(levelname)-8s %(message)s',
    #         datefmt="%m-%d %H:%M:%S",level=logging.INFO,handlers=[logging.StreamHandler(sys.stdout)])
    #     try:
    #         predict(d_args)
    #     except:
    #         error_text = traceback.format_exc()
    #         f =open('log.txt','a+')
    #         f.write(error_text)
    #         f.close()
    #         logging.error(error_text)
    
    # def resize(self, star_file:str, apix: float=15, out_folder="tomograms_resized"):
    #     '''
    #     This function rescale the tomograms to a given pixelsize
    #     '''
    #     md = MetaData()
    #     md.read(star_file)
        
    #     from scipy.ndimage import zoom
    #     import mrcfile
    #     if not os.path.isdir(out_folder):
    #         os.makedirs(out_folder)
    #     for item in md._data:
    #         ori_apix = item.rlnPixelSize
    #         tomo_name = item.rlnMicrographName
    #         zoom_factor = float(ori_apix)/apix
    #         new_tomo_name = "{}/{}".format(out_folder,os.path.basename(tomo_name))
    #         with mrcfile.open(tomo_name) as mrc:
    #             data = mrc.data
    #         print("scaling: {}".format(tomo_name))
    #         new_data = zoom(data, zoom_factor,order=3, prefilter=False)
    #         #new_data = rescale(data, zoom_factor,order=3, anti_aliasing = True)
    #         #new_data = new_data.astype(np.float32)

    #         with mrcfile.new(new_tomo_name,overwrite=True) as mrc:
    #             mrc.set_data(new_data)
    #             mrc.voxel_size = apix

    #         item.rlnPixelSize = apix
    #         print(new_tomo_name)
    #         item.rlnMicrographName = new_tomo_name
    #         print(item.rlnMicrographName)
    #     md.write(os.path.splitext(star_file)[0] + "_resized.star")
    #     print("scale_finished")

    def check(self):
        logging.basicConfig(format='%(asctime)s, %(levelname)-8s %(message)s',
        datefmt="%m-%d %H:%M:%S",level=logging.DEBUG,handlers=[logging.StreamHandler(sys.stdout)])

        from spIsoNet.bin.predict import predict
        from spIsoNet.bin.refine import run
        import skimage
        import PyQt5
        import tqdm
        logging.info('spIsoNet --version 1.0 alpha installed')
        logging.info(f"checking gpu speed")
        from spIsoNet.bin.verify import verify
        fp16, fp32 = verify()
        logging.info(f"time for mixed/half precsion and single precision are {fp16} and {fp32}. ")
        logging.info(f"The first number should be much smaller than the second one, if not please check whether cudnn, cuda, and pytorch versions match.")

    def gui(self):
        """
        \nGraphic User Interface\n
        """
        import spIsoNet.gui.Isonet_star_app as app
        app.main()

def Display(lines, out):
    text = "\n".join(lines) + "\n"
    out.write(text)

def pool_process(p_func,chunks_list,ncpu):
    from multiprocessing import Pool
    with Pool(ncpu,maxtasksperchild=1000) as p:
        # results = p.map(partial_func,chunks_gpu_num_list,chunksize=1)
        results = list(p.map(p_func,chunks_list))
    # return results

def main():
    core.Display = Display
    # logging.basicConfig(format='%(asctime)s, %(levelname)-8s %(message)s',datefmt="%m-%d %H:%M:%S",level=logging.INFO)
    if len(sys.argv) > 1:
        check_parse(sys.argv[1:])
    fire.Fire(ISONET)


if __name__ == "__main__":
    exit(main())