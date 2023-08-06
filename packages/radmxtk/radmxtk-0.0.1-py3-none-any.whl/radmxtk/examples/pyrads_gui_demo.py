#!/usr/bin/env python
import os
import shutil
import radiomics
from radmxtk.pyrads_gui.controller import Controller

if __name__ == '__main__':

	testCases = ['lung1','lung2']

	exampleData_folder = os.path.abspath(os.path.join(os.getcwd(),'exampleData'))

	dir_valid = True
	if os.path.isdir(exampleData_folder):
		for testCase in testCases:
			testCase_folder = os.path.join(exampleData_folder,testCase)
			if os.path.isdir(testCase_folder):
				imageName = os.path.join(testCase_folder,'CT.nrrd')
				if os.path.isfile(imageName) == True:
					roiName = os.path.join(testCase_folder,'tumour.nrrd')
					if os.path.isfile(roiName) == False:
						dir_valid = False
						shutil.rmtree(exampleData_folder)
						break
				else:
					dir_valid = False
					shutil.rmtree(exampleData_folder)
					break
			else:
				dir_valid = False
				shutil.rmtree(exampleData_folder)
				break
	else:
		dir_valid = False

	if dir_valid == False:
		os.mkdir(exampleData_folder)

		for testCase in testCases:
			testCase_folder = os.path.join(exampleData_folder,testCase)
			os.mkdir(testCase_folder)

			imageName, roiName = radiomics.getTestCase(testCase, testCase_folder)
			_, image_ext = os.path.splitext(imageName)
			_, roi_ext = os.path.splitext(roiName)
			new_imageName = os.path.join(testCase_folder,'CT'+image_ext)
			new_roiName = os.path.join(testCase_folder,'tumour'+roi_ext)

			os.rename(imageName,new_imageName)
			os.rename(roiName,new_roiName)
			
	c = Controller(exampleData_folder)