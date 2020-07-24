#!/usr/bin/env python3
import fire 
import logging
from mwr.util.dict2attr import Arg
# from argparser import args
class MWR:
    """
    MWR: Train on tomograms and Predict to restore missing-wedge
    """
    def train(self, input_dir: str,
        gpuID: str = '0,1,2,3',
        mask: str= None,
        noise_folder: str = None,
        iterations: int = 50,
        datas_are_subtomos: bool = False,
        subtomo_dir: str='subtomo',
        data_folder: str = "data",        
        log_level: str = "debug",

        continue_training: bool = False,
        continue_iter: int = 0,

        noise_level:  float= 0.04,
        noise_start_iter: int = 20,
        noise_pause: int = 5,
        
        cube_sidelen: int = 64,
        cropsize: int = 96,
        ncube: int = 300,
        preprocessing_ncpus: int = 24,

        epochs: int = 10,
        batch_size: int = 8,
        steps_per_epoch: int = 200,
        
        predict_cropsize: int = 96,
        predict_batch_size: int = 16,

        drop_out: float = 0.5,
        convs_per_depth: int = 3,
        kernel: tuple = (3,3,3),
        unet_depth: int = 3,
        batch_normalization: bool = False,
        normalize_percentile: bool = True,
    ):
        """
        Preprocess tomogram and train u-net model on generated subtomos
        :param input_dir: path to tomogram from which subtomos are sampled; format: .mwr or .rec
        :param mask: (None) if sample subtomos with a mask to exclude background region.
        :param gpuID: (0,1,2,3) The gpuID to used during the training. e.g 0,1,2,3.
        :param datas_are_subtomos: (False) Is your trainin data subtomograms?
        :param subtomo_dir: (subtomo) The folder where the input subtomograms at.
        :param iterations: (50) Number of training iterations.
        :param continue_training: (False) Continus previous training? When continue, the architecture of network can not be changed.
        :param continue_iter: (0) Which iteration you want to start from?

        ************************noise settings************************

        :param log_level: (debug) logging level 

        ************************continue training settings************************

        :param preprocessing_ncpus: (16) Number of cpu for preprocessing. 

        ************************training settings************************

        :param data_folder: (data)Temperary folder to save the generated data used for training.
        :param mask: (None) the path to mask file or None
        :param cube_sidelen: Size of training cubes, this size should be divisible by 2^unet_depth.
        :param cropsize: Size of cubes to impose missing wedge. Should be same or larger than size of cubes.
        :param ncube: Number of cubes generated for each (sub)tomos. Because each (sub)tomo rotates 16 times, the actual number of cubes for trainings should be ncube*16.
        :param epochs: Number of epoch for each iteraction.
        :param batch_size:Size of the minibatch.
        :param steps_per_epoch:Step per epoch. A good estimation of this value is (sub)tomos * ncube * 16 / batch_size *0.9.")

        ************************predict settings************************

        :param noise_folder: Add noise during training, Set None to disable noise reduction. 
        :param noise_level: Level of noise STD(added noise)/STD(data).
        :param noise_start_iter: Iteration that start to add trainning noise.
        :param noise_pause: Iters trainning noise remain at one level.

        ************************preprocessing settings************************

        :param drop_out: Drop out rate to reduce overfitting.
        :param convs_per_depth: Number of convolution layer for each depth.
        :param kernel: Kernel for convolution 
        :param unet_depth: Number of convolution layer for each depth.
        :param batch_normalization: Sometimes batch normalization may induce artifacts for extreme pixels in the first several iterations. Those could be restored in further iterations.
        :param normalize_percentile:Normalize the 5 percent and 95 percent pixel intensity to 0 and 1 respectively. If this is set to False, normalize the input to 0 mean and 1 standard dievation.
        :param predict_batch_size： Predict batch size. 

        ************************network settings************************
        
        :param predict_cropsize: Predict cubesize.
        """
        #from mwr.argparser import args
        # import warnings  
        # with warnings.catch_warnings():  
        #     warnings.filterwarnings("ignore",category=FutureWarning)
        from mwr.bin.mwr3D import run

        d = locals()
        d_args = Arg(d)
        logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d:%H:%M:%S')
        #if d_args.log_level == "debug":
        logging.basicConfig(level=logging.DEBUG)
        run(d_args)

    def predict(self, mrc_file: str, output_file: str, weight:str, model: str, gpuID:str='0,1,2,3', cubesize:int=64,cropsize:int=96, batchsize:int=16,norm: bool=True,log_level: str="debug"):
        """
        Predict tomograms using trained model including model.json and weight(xxx.h5)
        :param mrc_file: path to tomogram format: .mwr or .rec
        
        :return ******options******
        :param model: path to trained model
        :param output_file: 
        """
        from mwr.bin.mwr3D_predict import predict
        d = locals()
        d_args = Arg(d)
        predict(d_args)

    def make_mask(self,tomo_path,mask_name,side: int=8,percentile: int=50,threshold: int=1):
        """
        generate a mask to constrain sampling area of the tomogram
        :param tomo_path: path to the tomogram
        :param mask_name: path and name of the mask to save as
        :param side:
        :param percentile:
        :param threshold:
        """
        from mwr.bin.maskGene import make_mask
        make_mask(tomo_path,mask_name,side=side,percentile=percentile,threshold=threshold)
        print('mask generated')

    def generate_noise(self,output_folder: str,number_volume: int, cubesize: int, minangle: int=-60,maxangle: int=60,
    anglestep: int=2, start: int=0,ncpus: int=20, mode: int=0):
        """
        generate training noise to accelerate the missing wedge information retrieval
        :param output_folder: path to folder for saving noises
        :param number_volume: number of noise cubes to generate
        :param cubesize: side length of the noise cubes, usually 64 or 96
        :param ncpus: number of cpus to use
        """
        from mwr.util.mwr3D_noise_generator import make_noise
        make_noise(output_folder=output_folder, number_volume=number_volume, cubesize=cubesize, minangle=minangle,maxangle=maxangle, anglestep=anglestep, start=start,ncpus=ncpus, mode=mode)
        
    
    
if __name__ == "__main__":
    fire.Fire(MWR)
