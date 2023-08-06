import tkinter.filedialog
import tkinter as tk
import pandas as pd
import SimpleITK as sitk
import numpy as np

import radiomics
import threading
import logging
import shutil
import yaml
import csv
import six
import os

from radiomics import getFeatureClasses
from radiomics.featureextractor import RadiomicsFeatureExtractor
from multiprocessing import cpu_count, Pool
from collections import OrderedDict
from datetime import datetime

class Model():
	def __init__(self):
		self.data_path = ''
		self.image_path = ''
		self.roi_path = ''
		self.default_data_path = os.getcwd()
		self.default_image_path = ''
		self.default_roi_path = ''
		self.initial_dir = self.default_data_path
		self.directory_setup = ''
		self.subject_list = []
		self.all_files_list = []
		self.image_files_list = []
		self.roi_files_list = []
		self.file_list_valid = False
		self.data_files_valid = False
		self.yaml_dicts = {'imageType':{'Original': {}}}
		self.yaml_file = ''
		self.subject_files = {}
		self.logs_file = ''
		self.output_file = ''

	def read_meta_params(self):
		meta_params_found = False
		lines = []
		with open(self.yaml_file, 'r') as yaml_file:
			for line in yaml_file:  
				# checking string is present in line or not
				if meta_params_found == True:
					lines.append(line)
				elif '# meta-parameters (DO NOT EDIT)' in line:
					meta_params_found = True

			if meta_params_found:
				voxelBased_line = lines[0]
				downSampling_line = lines[1]

				voxelBased = voxelBased_line[voxelBased_line.index(':')+1:].strip() == 'true'
				downSampling = downSampling_line[downSampling_line.index(':')+1:].strip() == 'true'

				if voxelBased == True:
					if self.yaml_dicts['voxelSetting'] is None:
						self.yaml_dicts['voxelSetting'] = {}
					self.yaml_dicts['voxelSetting']['voxelBased'] = True
					self.yaml_dicts['voxelSetting']['downSampling'] = True
				
					if downSampling == False:
						self.yaml_dicts['voxelSetting']['downSampling'] = False

	def browse_dir(self, step_name):
		dir_path = ''
		if step_name == 'Step 2':
			data_path = tk.filedialog.askdirectory(initialdir = self.default_data_path)
			if len(data_path) > 0:
				self.data_path = data_path
				self.default_data_path = data_path
				self.initial_dir = os.path.split(data_path)[0]
				self.init_subject_list()
			dir_path = self.data_path

		elif step_name == 'Step 3':
			image_path = tk.filedialog.askdirectory(initialdir = self.default_image_path)
			if len(image_path) > 0:
				self.image_path = image_path
				self.init_image_files_list()
			dir_path = self.image_path

		elif step_name == 'Step 4':
			roi_path = tk.filedialog.askdirectory(initialdir = self.default_roi_path)
			if len(roi_path) > 0:
				self.roi_path = roi_path
				self.init_roi_files_list()
				self.init_all_files_list()
			dir_path = self.roi_path

		return dir_path

	def load(self):
		open_file = tk.filedialog.askopenfile(mode="r",initialdir = self.initial_dir,filetypes=[("YAML file", "*.yaml")])
		if open_file is not None:
			self.yaml_file = open_file.name
			self.yaml_dicts = {}
			with open(self.yaml_file, 'r') as stream:
				try:
					self.yaml_dicts = yaml.safe_load(stream)
					self.read_meta_params()
				except yaml.YAMLError as exc:
					print(exc)
		else:
			self.yaml_file = ''
			self.yaml_dicts = {}

	def save(self,setting_dict,voxelSetting_dict,featureClass_dict):
		self.setting_dict = setting_dict
		self.voxelSetting_dict = voxelSetting_dict
		self.featureClass_dict = featureClass_dict

		self.yaml_dicts['setting'] = setting_dict
		self.yaml_dicts['voxelSetting'] = voxelSetting_dict
		self.yaml_dicts['featureClass'] = featureClass_dict

		save_file = tk.filedialog.asksaveasfile(defaultextension='.yaml',initialdir = self.initial_dir,filetypes=[("YAML file", "*.yaml")])
		meta_params = ['\n\n# meta-parameters (DO NOT EDIT)\n']
		if save_file is not None:
			self.yaml_file = save_file.name
			with open(self.yaml_file, 'a') as the_file:
				
				the_file.write('imageType:\n  Original: {}\n\n')
				if len(self.setting_dict) > 0:
					# self.yaml_dicts['setting'] = self.setting_dict
					the_file.write('setting:\n')
					for key,val in self.setting_dict.items():
						if isinstance(val, bool):
							if val == True:
								the_file.write('  '+key+': '+'true'+'\n')
							else:
								the_file.write('  '+key+': '+'false'+'\n')
						else:
							the_file.write('  '+key+': '+str(val)+'\n')
					the_file.write('\n')

				
				if 'voxelBased' in list(self.voxelSetting_dict.keys()):
					self.yaml_dicts['voxelSetting'] = self.voxelSetting_dict
					if 'downSampling' not in list(self.voxelSetting_dict.keys()):
						self.voxelSetting_dict['downSampling'] = False

					for key,val in self.voxelSetting_dict.items():

						if key == 'voxelBased':
							if val == True:
								the_file.write('voxelSetting:\n')
								meta_params.append('# voxelBased: true\n')	
							else:
								meta_params.append('# voxelBased: false\n')
						elif key == 'downSampling':
							if val == False:
								meta_params.append('# downSampling: false\n')	
							else:
								meta_params.append('# downSampling: true\n')
						else:
							if isinstance(val, bool):
								
								if val == True:
									the_file.write('  '+key+': '+'true'+'\n')
								else:
									the_file.write('  '+key+': '+'false'+'\n')
							else:
								the_file.write('  '+key+': '+str(val)+'\n')
					the_file.write('\n')
				else:
					the_file.write('\n')

				if len(self.featureClass_dict) > 0:
					the_file.write('featureClass:\n')
					for key,val in self.featureClass_dict.items():
						the_file.write('  '+key+':\n')
					the_file.write('\n')
				
				the_file.write(''.join(meta_params))

	def init_subject_list(self):
		if len(self.data_path) > 0:
			self.subject_list = [dir_item for dir_item in os.listdir(self.data_path) if os.path.isdir(os.path.join(self.data_path,dir_item))]

	def init_roi_files_list(self):
		if len(self.roi_path) > 0:
			self.roi_files_list = [dir_item for dir_item in os.listdir(self.roi_path) if dir_item[0] != '.']# if (dir_item[-3:]=='nii' or dir_item[-6:]=='nii.gz')]

	def init_image_files_list(self):
		if len(self.image_path) > 0:
			self.image_files_list = [dir_item for dir_item in os.listdir(self.image_path) if dir_item[0] != '.']# if (dir_item[-3:]=='nii' or dir_item[-6:]=='nii.gz')]

	def init_all_files_list(self):
		self.all_files_list = list(set(self.image_files_list+self.roi_files_list))
		pass

	def check_file_list_valid(self):
		if len(set(self.image_files_list).intersection(self.roi_files_list)) > 0:
			self.file_list_valid = False
		elif len(self.image_files_list) == 0 or len(self.roi_files_list) == 0:
			self.file_list_valid = False
		else:
			self.file_list_valid = True

		return self.file_list_valid

	def validate_directory(self):
		if self.directory_setup == 'same':

			subject_files = {}
			for subject in self.subject_list:
				subject_files[subject] = {}
				for image_file in self.image_files_list:
					image_path = os.path.join(self.data_path,subject,image_file)

					if os.path.isfile(image_path):
						subject_files[subject][image_file] = image_path
					else:
						return False, file_path

				for roi_file in self.roi_files_list:
					roi_path = os.path.join(self.data_path,subject,roi_file)

					if os.path.isfile(roi_path):
						subject_files[subject][roi_file] = roi_path
					else:
						return False, file_path
			
			self.subject_files = subject_files
			return True, ''

		elif self.directory_setup == 'diff':

			subject_files = {}
			for subject in self.subject_list:
				subject_files[subject] = {}

				image_folder = os.path.join(self.data_path,subject,os.path.split(self.image_path)[1])
				for image_file in self.image_files_list:
					image_path = os.path.join(image_folder,image_file)

					if os.path.isfile(image_path):
						subject_files[subject][image_file] = image_path
					else:
						return False, image_path

				roi_folder = os.path.join(self.data_path,subject,os.path.split(self.roi_path)[1])
				for roi_file in self.roi_files_list:
					roi_path = os.path.join(roi_folder,roi_file)

					if os.path.isfile(roi_path):
						subject_files[subject][roi_file] = roi_path
					else:
						return False, roi_path

			self.subject_files = subject_files
			return True, ''

	def init_output_file(self):
		initial_dir = os.path.split(self.data_path)[0]
		initial_name = os.path.split(self.data_path)[1]+'_features.csv'
		output_file = tk.filedialog.asksaveasfile(defaultextension='.csv',initialdir=initial_dir,filetypes=[("CSV file", "*.csv")])
		
		if output_file is not None:
			self.output_file = output_file.name
			self.root_dir = os.path.split(self.output_file)[0]
			self.temp_dir = os.path.join(self.root_dir,'_TEMP')

	def run(self,subject):
		# Instantiate Radiomics Feature extractor
		extractor = RadiomicsFeatureExtractor(self.yaml_file)

		#self.parent.update_idletasks()
		ptLogger = logging.getLogger('radiomics.batch')
		feature_vector = OrderedDict({'subject_ID':subject})

		# set thread name to subject ID
		threading.current_thread().name = subject 

		subject_paths = self.subject_files[subject]

		for image in self.image_files_list:
			image_path = subject_paths[image]
			image_name = image[0:image.index('.')]
			
			for roi in self.roi_files_list:
				roi_path = subject_paths[roi]
				roi_name = roi[0:roi.index('.')]

				try:
					filename = r'features_'+subject+ '_' + image_name + '_' + roi_name + '.csv'
					output_filename = os.path.join(self.root_dir, self.temp_dir, filename)

					if os.path.isfile(output_filename):
						# Output already generated, load result (prevents re-extraction in case of interrupted process)
						with open(output_filename, 'w') as outputFile:
							reader = csv.reader(outputFile)
							headers = reader.rows[0]
							values = reader.rows[1]
							feature_vector = OrderedDict(zip(headers, values))

						ptLogger.info('Image: %s,  ROI: %s  already processed...', image_name, roi_name)

					else:
						t = datetime.now()

						pyrads_result = extractor.execute(image_path, roi_path)
						pyrads_list = []

						for key,val in pyrads_result.items():
							pyrads_key = image_name + '_' + roi_name + '_' + key
							pyrads_list.append((pyrads_key,val))

						pyrads_dict = OrderedDict(pyrads_list[22:])
						feature_vector.update(pyrads_dict)

						# Store results in temporary separate files to prevent write conflicts
						# This allows for the extraction to be interrupted. Upon restarting, already processed cases are found in the
						# TEMP_DIR directory and loaded instead of re-extracted
						with open(output_filename, 'w') as outputFile:
							writer = csv.DictWriter(outputFile, fieldnames=list(feature_vector.keys()), lineterminator='\n')
							writer.writeheader()
							writer.writerow(feature_vector)
							# Display message
						delta_t = datetime.now() - t

						ptLogger.info('Subject: %s, Image: %s,  ROI: %s  processed in %s', subject,image_name,roi_name,delta_t)

				except Exception:
					ptLogger.error('Feature extraction failed!', exc_info=True)

		return feature_vector

	def extract_segment_features(self,logger):
		# Ensure the entire extraction is handled on 1 thread
		#####################################################
		sitk.ProcessObject_SetGlobalDefaultNumberOfThreads(1)
		# Set up the pool processing
		############################
		logger.info('pyradiomics version: %s', radiomics.__version__)
		logger.info('Loaded %d jobs', len(self.subject_list))

		# Make output directory
		if os.path.isdir(os.path.join(self.root_dir, self.temp_dir)):
			shutil.rmtree(os.path.join(self.root_dir, self.temp_dir))			
		logger.info('Creating temporary output directory %s', os.path.join(self.root_dir, self.temp_dir))
		os.mkdir(os.path.join(self.root_dir, self.temp_dir))

		NUM_OF_WORKERS = cpu_count() - 1  # Number of processors to use, keep one processor free for other work
		if NUM_OF_WORKERS < 1:  # in case only one processor is available, ensure that it is used
			NUM_OF_WORKERS = 1

		logger.info('Starting parallel pool with %d workers out of %d CPUs', NUM_OF_WORKERS, cpu_count())

		# Running the Pool
		pool = Pool(NUM_OF_WORKERS)
		results = pool.map(self.run, self.subject_list)

		try:
			# Store all results into 1 file
			with open(self.output_file, mode='w') as outputFile:
				writer = csv.DictWriter(outputFile,
					fieldnames=list(results[0].keys()),
					restval='',
					extrasaction='raise',  # raise error when a case contains more headers than first case
					lineterminator='\n')
				writer.writeheader()
				writer.writerows(results)

			# if REMOVE_TEMP_DIR:
			logger.info('Removing temporary directory %s (contains individual case results files)',
									os.path.join(self.root_dir, self.temp_dir))
			shutil.rmtree(os.path.join(self.root_dir, self.temp_dir))


		except Exception:
			logger.error('Error storing results into single file!', exc_info=True)

	def extract_voxel_features(self,logger):
		NUM_OF_WORKERS = cpu_count() - 1  # Number of processors to use, keep one processor free for other work
		if NUM_OF_WORKERS < 1:  # in case only one processor is available, ensure that it is used
			NUM_OF_WORKERS = 1

		# Make output directory
		if os.path.isdir(os.path.join(self.root_dir, self.temp_dir)):
			shutil.rmtree(os.path.join(self.root_dir, self.temp_dir))			
		logger.info('Creating temporary output directory %s', os.path.join(self.root_dir, self.temp_dir))
		os.mkdir(os.path.join(self.root_dir, self.temp_dir))

		# Ensure the entire extraction is handled on 1 thread
		#####################################################
		sitk.ProcessObject_SetGlobalDefaultNumberOfThreads(1)
		# Set up the pool processing
		############################
		logger.info('pyradiomics version: %s', radiomics.__version__)

		# Initialize feature extractor using the settings file
		extractor = RadiomicsFeatureExtractor(self.yaml_file)
		featureClasses = getFeatureClasses()

		features_dict = {}

		for feature_class, features in six.iteritems(extractor.enabledFeatures):
			features_dict[feature_class] = []

			if features is None or len(features) == 0:
				features = [f for f, deprecated in six.iteritems(featureClasses[feature_class].getFeatureNames()) if not deprecated]

			for f in features:
				features_dict[feature_class].append(f)

		output_dict = {}
		first_subject = True
		for subject in self.subject_list:
			subject_paths = self.subject_files[subject]
			output_dict[subject] = {}

			output_filelist = {}
			for roi in self.roi_files_list:
				roi_path = subject_paths[roi]
				roi_name = roi[0:roi.index('.')]
				output_filelist[roi_name] = {}

				_, file_extension = os.path.splitext(roi_path)
				if file_extension == '.gz':
					file_extension = '.nii.gz'
				filename = subject + '_' + roi_name + '_firstorder_Mean' + file_extension # this is important
				roi_samples_path = os.path.join(self.root_dir, self.temp_dir, filename)

				extractor = RadiomicsFeatureExtractor(self.yaml_file)
				extractor.disableAllFeatures()
				extractor.enabledFeatures = {'firstorder':['Mean']}
				extractor.enableFeaturesByName()

				featureVector = extractor.execute(roi_path,roi_path, voxelBased=True)

				for featureName, featureValue in six.iteritems(featureVector):
					if isinstance(featureValue, sitk.Image):
						roi_samples = featureValue				
						if 'downSampling' in list(self.yaml_dicts['voxelSetting'].keys()):
							if self.yaml_dicts['voxelSetting']['downSampling'] == True:
								if 'kernelRadius' in list(self.yaml_dicts['voxelSetting'].keys()):
									r = self.yaml_dicts['voxelSetting']['kernelRadius']
								else:
									r = 2
								stride = 2*r + 1

								roi = sitk.GetArrayFromImage(roi_samples)

								if 'force2D' in list(self.yaml_dicts['setting'].keys()):
									force2D = self.yaml_dicts['setting']['force2D']
								else:
									force2D = False

								offsets_checked = []
								num_samples = []

								for offset_i in range(0,stride):
									for offset_j in range(0,stride):
										if force2D == False:
											for offset_k in range(0,stride):
												offset = (offset_i,offset_j,offset_k)
												downSampling = 0*roi
												downSampling[0:-1:stride,0:-1:stride,0:-1:stride] = 1
												np.roll(downSampling,offset,(0,1,2))
												samples = np.multiply(roi,downSampling)
												
												offsets_checked.append(offset)
												num_samples.append(np.sum(np.ravel(samples)))
										else:
											offset = (offset_i,offset_j,0)
											downSampling = 0*roi
											downSampling[0:-1:stride,0:-1:stride,:] = 1
											np.roll(downSampling,offset,(0,1,2))
											samples = np.multiply(roi,downSampling)
											
											offsets_checked.append(offset)
											num_samples.append(np.sum(np.ravel(samples)))

								ind = num_samples.index(max(num_samples))
								offset = offsets_checked[ind]
								
								downSampling = 0*roi
								if force2D == False:
									downSampling[0:-1:stride,0:-1:stride,0:-1:stride] = 1
									np.roll(downSampling,offset,(0,1,2))
								else:
									downSampling[0:-1:stride,0:-1:stride,:] = 1
									np.roll(downSampling,offset,(0,1,2))

								roi_samples_nda = np.multiply(roi,downSampling)
								roi_samples = sitk.GetImageFromArray(roi_samples_nda)

						sitk.WriteImage(roi_samples, roi_samples_path)

				for image in self.image_files_list:
					image_path = subject_paths[image]
					image_name = image[0:image.index('.')]

					output_filelist[roi_name][image_name] = {}

					for feature_class, feature_list in features_dict.items():

						output_filelist[roi_name][image_name][feature_class] = {}
						cases = []	
						for feature in feature_list:
							case = {'subject_ID':subject,'image_name':image_name,'image_path':image_path,'roi_name':roi_name,'roi_path':roi_path}
							case['roi_samples'] = roi_samples_path
							case['feature_class'] = feature_class
							case['feature'] = feature
							cases.append(case)

							filename = case['subject_ID']+'_'+case['image_name']+'_'+case['roi_name']+'_'+case['feature_class']+'_'+case['feature']+'.csv'
							output_filelist[roi_name][image_name][feature_class][feature] = filename# os.path.join(self.root_dir, self.temp_dir, filename))

						logger.info('Starting parallel pool with %d workers out of %d CPUs to compute %d %s feature maps', NUM_OF_WORKERS, cpu_count(), len(feature_list), feature_class)
						pool = Pool(NUM_OF_WORKERS)
						results = pool.map(self.run_voxel, cases)

			# subject_ID_added = False
			for image in self.image_files_list:
				image_name = image[0:image.index('.')]

				for roi in self.roi_files_list:
					roi_name = roi[0:roi.index('.')]

					for feature_class, feature_list in features_dict.items():

						for feature in feature_list:
							csv_file = output_filelist[roi_name][image_name][feature_class][feature]
							csv_path = os.path.join(self.root_dir,self.temp_dir,csv_file)
							df = pd.read_csv(csv_path)
							feature_name = df.columns[0]
							output_dict[subject][feature_name] = df.values[:,0].tolist()

			if first_subject == True:
				subject_df = pd.DataFrame.from_dict(output_dict[subject])
				subject_df = pd.concat([pd.Series([subject]*subject_df.shape[0],name='subject_ID'),subject_df],axis=1)
				first_subject = False
			else:
				subject_df_i = pd.DataFrame.from_dict(output_dict[subject])
				subject_df_i = pd.concat([pd.Series([subject]*subject_df_i.shape[0],name='subject_ID'),subject_df_i],axis=1)
				subject_df = pd.concat([subject_df,subject_df_i],axis=0)

		subject_df.to_csv(self.output_file,index=False)

		# if REMOVE_TEMP_DIR:
		logger.info('Removing temporary directory %s (contains individual case results files)',
								os.path.join(self.root_dir, self.temp_dir))
		shutil.rmtree(os.path.join(self.root_dir, self.temp_dir))

	def run_voxel(self,case):
		# Instantiate Radiomics Feature extractor
		extractor = RadiomicsFeatureExtractor(self.yaml_file)
		extractor.disableAllFeatures()
		extractor.enabledFeatures = {case['feature_class']:[case['feature']]}
		extractor.enableFeaturesByName()

		ptLogger = logging.getLogger('radiomics.batch')

		# set thread name to feature class
		threading.current_thread().name = case['feature_class']

		try:
			filename = case['subject_ID']+'_'+case['image_name']+'_'+case['roi_name']+'_'+case['feature_class']+'_'+case['feature']+'.csv'
			output_filename = os.path.join(self.root_dir, self.temp_dir, filename)

			if os.path.isfile(output_filename):
			# Output already generated, load result (prevents re-extraction in case of interrupted process)
				ptLogger.info('Subject: %s, Image: %s,  ROI: %s,  Feature: %s  already processed...',case['subject_ID'],case['image_name'],case['roi_name'],case['feature'])
			else:
				t = datetime.now()
				featureVector = extractor.execute(case['image_path'], case['roi_path'], voxelBased=True)

				image = None
				for featureName, featureValue in six.iteritems(featureVector):
					if isinstance(featureValue, sitk.Image):
						image = featureValue

						roi_samples = sitk.GetArrayFromImage(sitk.ReadImage(case['roi_samples']))
						image_vals = sitk.GetArrayFromImage(image)
						image_sampled = np.ravel(image_vals[roi_samples == 1]) # TODO: add label support

						feature_name = case['image_name']+'_'+case['roi_name']+'_'+case['feature_class']+'_'+case['feature']
						feature_values = pd.Series(data=image_sampled, name=feature_name)

						with open(output_filename, 'w') as outputFile:
							feature_values.to_csv(output_filename,index=False)
							delta_t = datetime.now() - t
							ptLogger.info('Subject: %s, Image: %s,  ROI: %s,  Feature: %s  processed in %s',case['subject_ID'],case['image_name'], case['roi_name'],case['feature'],delta_t)
		
		except Exception:
			ptLogger.error('Feature extraction failed!', exc_info=True)

	def extract_features(self):
		threading.current_thread().name = 'Main'
		self.logs_file = os.path.join(self.root_dir,'pyrad_log.txt')

		rLogger = radiomics.logger
		logHandler = logging.FileHandler(filename=self.logs_file, mode='w')
		logHandler.setLevel(logging.INFO)
		logHandler.setFormatter(logging.Formatter('%(levelname)-.1s: (%(threadName)s) %(name)s: %(message)s'))
		rLogger.addHandler(logHandler)

		outputhandler = rLogger.handlers[0]  # Handler printing to the output
		outputhandler.setFormatter(logging.Formatter('[%(asctime)-.19s] (%(threadName)s) %(name)s: %(message)s'))
		outputhandler.setLevel(logging.INFO)  # Ensures that INFO messages are being passed to the filter
		outputhandler.addFilter(info_filter('radiomics.batch'))

		logging.getLogger('radiomics.batch').debug('Logging init')
		logger = logging.getLogger('radiomics.batch')

		if 'voxelSetting' in list(self.yaml_dicts.keys()):
			self.extract_voxel_features(logger)
		else:
			self.extract_segment_features(logger)

class info_filter(logging.Filter):
	def __init__(self, name):
		super(info_filter, self).__init__(name)
		self.level = logging.WARNING

	def filter(self, record):
		if record.levelno >= self.level:
			return True
		if record.name == self.name and record.levelno >= logging.INFO:
			return True
		return False

