import tkinter as tk
from tkinter import messagebox

from . import models
from . import views

class Controller():
	def __init__(self, initial_data_dir):
		self.step_name = 'Step 1'
		self.directory_radio_flag = False
		self.directory_browse_flag = False
		self.file_list_modified = False

		self.root = tk.Tk()
		self.model = models.Model()
		if initial_data_dir is not None:
			self.model.default_data_path = initial_data_dir
		self.view = views.View(self.root, self)

		self.root.title("PyRadiomics Utility")
		self.root['bg'] = '#F0F0F0'

		width=812; height=557
		screenwidth = self.root.winfo_screenwidth(); screenheight = self.root.winfo_screenheight()

		alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
		self.root.geometry(alignstr)
		self.root.resizable(width=False, height=False)
		self.root.deiconify()
		
		self.root.mainloop()

	def next(self):
		next_step = {'Step 1':'Step 2','Step 2':'Step 3','Step 3':'Step 4','Step 4':'Step 5','Step 5':'ready','ready':'extraction','extraction':'close'}[self.step_name]

		if next_step == 'Step 2':
			self.step_name = 'Step 2'
			self.view.show_step2(self.root,self)

			self.view.path_entry.contents.set(self.model.data_path)
			self.view.wiz_steps.deactivate('Step 1')
			self.view.wiz_steps.activate('Step 2')

			if len(self.model.data_path) == 0:
				self.view.next_button['state'] = 'disabled'
			else:
				self.view.next_button['state'] = 'normal'

		elif next_step == 'Step 3':	

			if self.model.directory_setup == 'same': # skip to file verification
				self.step_name = 'Step 5'
				self.model.image_path = self.model.data_path + '/' + self.model.subject_list[0] 
				self.model.roi_path = self.model.data_path + '/' + self.model.subject_list[0]

				if self.file_list_modified == False:
					self.model.init_image_files_list()
					self.model.init_roi_files_list()
					self.model.init_all_files_list()
					self.update_file_lists()

				self.view.show_step5(self.root,self)
				
				self.view.wiz_steps.deactivate('Step 2')
				self.view.wiz_steps.deactivate('Step 3')
				self.view.wiz_steps.deactivate('Step 4')
				self.view.wiz_steps.activate('Step 5')

				if self.model.check_file_list_valid():
					self.view.next_button['state'] = 'normal'
				else:
					self.view.next_button['state'] = 'disabled'

			elif self.model.directory_setup == 'diff': 
				self.step_name = 'Step 3'
				self.view.show_step3(self.root,self)

				self.view.path_entry.contents.set(self.model.image_path)
				self.view.wiz_steps.deactivate('Step 2')
				self.view.wiz_steps.activate('Step 3')

				if self.file_list_modified == False:
					self.model.init_image_files_list()
					self.model.init_roi_files_list()
					self.model.init_all_files_list()
					self.update_file_lists()

				if len(self.model.image_path) == 0:
					self.view.next_button['state'] = 'disabled'
				else:
					self.view.next_button['state'] = 'normal'

		elif next_step == 'Step 4':
			self.step_name = 'Step 4'
			self.view.show_step4(self.root,self)

			self.view.path_entry.contents.set(self.model.roi_path)
			self.view.wiz_steps.deactivate('Step 3')
			self.view.wiz_steps.activate('Step 4')

			self.view.next_button['state'] = 'disabled'

			if len(self.model.roi_path) == 0:
				self.view.next_button['state'] = 'disabled'
			else:
				self.view.next_button['state'] = 'normal'

			if self.file_list_modified == False:
				self.model.init_image_files_list()
				self.model.init_roi_files_list()
				self.model.init_all_files_list()
				self.update_file_lists()

		elif next_step == 'Step 5':			
			self.step_name = 'Step 5'
			self.view.show_step5(self.root,self)

			self.view.wiz_steps.activate('Step 5')
			self.view.wiz_steps.deactivate('Step 4')

			if self.model.check_file_list_valid():
				self.view.next_button['state'] = 'normal'
			else:
				self.view.next_button['state'] = 'disabled'

		elif next_step == 'ready':
			self.step_name = 'ready'
			self.view.show_extraction(self.root,self)
			self.view.wiz_steps.deactivate('Step 5')

			ready_flag, missing_file = self.model.validate_directory()
			if ready_flag:
				self.model.init_output_file()
			else:
				messagebox.showerror('Missing File(s)', 'Could not locate\n '+missing_file)
				self.view.next_button['state'] = 'disabled'

		elif next_step == 'extraction':
			self.step_name = 'extraction'
			self.view.instruction['text'] = 'Running PyRadiomics...'
			self.view.next_button['state'] = 'disabled'
			self.view.back_button['state'] = 'disabled'
			self.root.update()
			self.model.extract_features()
			self.view.instruction['text'] = 'Complete!'
			self.view.next_button['text'] = 'Close'
			self.view.show_save_load_label()
			self.view.save_load_label['text'] = 'Features saved in:\n    '+self.model.output_file
			self.view.next_button['state'] = 'normal'
			self.view.back_button['state'] = 'normal'
		elif next_step == 'close':
			answer = messagebox.askokcancel("Ready to Close","Are you sure you want to quit?")
			if answer:
				self.root.destroy()

	def back(self):
		back_step = {'Step 1':None,'Step 2':'Step 1','Step 3':'Step 2','Step 4':'Step 3','Step 5':'Step 4','ready':'Step 5','extraction':'ready'}[self.step_name]

		if back_step == 'Step 1':
			self.view.show_step1(self.root,self)
			self.load_options()
			self.view.next_button['state'] = 'normal'
			self.view.wiz_steps.deactivate('Step 2')
			self.view.wiz_steps.activate('Step 1')
			self.step_name = 'Step 1'
			self.view.next_button['state'] = 'normal'

		elif back_step == 'Step 2':
			self.view.show_step2(self.root,self)
			self.view.path_entry.contents.set(self.model.data_path)
			self.view.next_button['state'] = 'normal'
			self.view.wiz_steps.deactivate('Step 3')
			self.view.wiz_steps.activate('Step 2')
			self.step_name = 'Step 2'
		
		elif back_step == 'Step 3':
			self.view.show_step3(self.root,self)
			self.view.path_entry.contents.set(self.model.image_path)
			self.view.next_button['state'] = 'normal'
			self.view.wiz_steps.deactivate('Step 4')
			self.view.wiz_steps.activate('Step 3')
			self.step_name = 'Step 3'

		elif back_step == 'Step 4':
			if self.model.directory_setup == 'same':
				self.view.show_step2(self.root,self)
				self.view.path_entry.contents.set(self.model.data_path)
				self.view.next_button['state'] = 'normal'
				self.view.wiz_steps.deactivate('Step 5')
				self.view.wiz_steps.activate('Step 2')
				self.step_name = 'Step 2'
			else:
				self.view.show_step4(self.root,self)
				self.view.path_entry.contents.set(self.model.roi_path)
				self.view.next_button['state'] = 'normal'
				self.view.wiz_steps.deactivate('Step 5')
				self.view.wiz_steps.activate('Step 4')
				self.step_name = 'Step 4'

		elif back_step == 'Step 5':
			self.view.show_step5(self.root,self)

			self.view.next_button['state'] = 'normal'
			self.view.next_button['text'] = 'Next'

			self.view.wiz_steps.activate('Step 5')
			self.step_name = 'Step 5'

		elif back_step == 'ready':
			self.view.hide_save_load_label()
			self.root.update()
			self.view.show_extraction(self.root,self)
			self.view.instruction['text'] = 'Proceed to Extraction:'
			self.step_name = 'ready'

	def load(self):
		self.model.load()
		if len(self.model.yaml_file) > 0:
			self.view.save_load_label_text = 'Parameters loaded from:\n  '+self.model.yaml_file 
			self.view.show_save_load_label()
			self.view.next_button['state'] = 'normal'
			self.view.next_button_state = 'normal'
			self.load_options()

	def load_options(self):
		options_objects = [self.view.setting,self.view.voxelSetting,self.view.featureClass]
		for options_object in options_objects:
			for key,val in options_object.options_vars.items():
				options_object.options_vars[key].set(0)
				options_object.hide_entries(key)
		
		if 'voxelSetting' not in list(self.model.yaml_dicts.keys()):
			self.model.yaml_dicts['voxelSetting'] = {}
			self.model.yaml_dicts['voxelSetting']['voxelBased'] = False
		else:
			if len(self.model.yaml_dicts['voxelSetting']) == 0:
				self.model.yaml_dicts['voxelSetting'] = {}
			self.model.yaml_dicts['voxelSetting']['voxelBased'] = True

		for yaml_key,yaml_val in self.model.yaml_dicts.items():
			if yaml_key == 'imageType':
				pass
			else:
				yaml_dict = yaml_val
				if yaml_key == 'setting':
					for key,val in yaml_dict.items():

						if key in self.view.setting.options_vars.keys():
							if isinstance(val, bool):
								self.view.setting.options_vars[key].set(val)

							elif type(val) == type(float()) or type(val) == type(int()): 
								self.view.setting.options_vars[key].set(1)
								self.view.setting.options_strings[key].set(val) 
								self.view.setting.show_entries(key)

							elif type(val) == type(list()):
								self.view.setting.options_vars[key].set(1)
								for i in range(3):
									self.view.setting.options_strings[key][i].set(val[i]) 
									self.view.setting.show_entries(key)
								
				elif yaml_key == 'voxelSetting':
					if yaml_dict['voxelBased'] == True:
						self.view.featureClass.options_buttons['shape']['state'] = 'disabled'
						for option in self.view.voxelSetting.options_list:
							self.view.voxelSetting.options_buttons[option]['state'] = 'normal'
						for key,val in yaml_dict.items():
							if isinstance(val, bool):
								self.view.voxelSetting.options_vars[key].set(val)

							elif type(val) == type(float()) or type(val) == type(int()) or val == 'nan': 
								self.view.voxelSetting.options_vars[key].set(1)
								self.view.voxelSetting.options_strings[key].set(val) 
								self.view.voxelSetting.show_entries(key)

							elif type(val) == type(list()):
								self.view.voxelSetting.options_vars[key].set(1)
								for i in range(3):
									self.view.voxelSetting.options_strings[key][i].set(val[i]) 
									self.view.voxelSetting.show_entries(key)

					elif yaml_dict['voxelBased'] == False:
						self.view.voxelSetting.deactivate_all()
						self.view.voxelSetting.options_vars['voxelBased'].set(0)
						self.view.voxelSetting.options_buttons['voxelBased']['state'] = 'normal'

				elif yaml_key == 'featureClass':
					for key,val in yaml_dict.items():
						self.view.featureClass.options_vars[key].set(1)
						if key == 'shape' and val == True:
							self.view.voxelSetting.deactivate_all()
							self.view.voxelSetting.options_vars['voxelBased'].set(0)

	def save(self):
		setting_dict = {}
		for i, option in enumerate(self.view.setting.options_list):
			if self.view.setting.options_vars[option].get() == 1:
				if self.view.setting.options_dicts[i]['has_entry']:
					setting_dict[option] = float(self.view.setting.options_strings[option].get())
				elif self.view.setting.options_dicts[i]['has_entries']:
					x = float(self.view.setting.options_strings[option][0].get())
					y = float(self.view.setting.options_strings[option][1].get())
					z = float(self.view.setting.options_strings[option][2].get())
					setting_dict[option] = [x,y,z]
				else:
					setting_dict[option] = True

		voxelSetting_dict = {}
		for i, option in enumerate(self.view.voxelSetting.options_list):
			if self.view.voxelSetting.options_vars[option].get() == 1:
				if self.view.voxelSetting.options_dicts[i]['has_entry']:
					entry_string = self.view.voxelSetting.options_strings[option].get()

					if type(self.view.voxelSetting.params['option_list'][i][1]['entry_type']) == type(int(0)):
						voxelSetting_dict[option] = int(entry_string)
					else:
						voxelSetting_dict[option] = float(entry_string)

				elif self.view.voxelSetting.options_dicts[i]['has_entries']:
					x = float(self.view.voxelSetting.options_strings[option][0].get())
					y = float(self.view.voxelSetting.options_strings[option][1].get())
					z = float(self.view.voxelSetting.options_strings[option][2].get())
					voxelSetting_dict[option] = [x,y,z]
				else:
					voxelSetting_dict[option] = True

		featureClass_dict = {}
		for i, option in enumerate(self.view.featureClass.options_list):
			if self.view.featureClass.options_vars[option].get() == 1:
				featureClass_dict[option] = True

		self.model.setting_dict = setting_dict
		self.model.voxelSetting_dict = voxelSetting_dict
		self.model.featureClass_dict = featureClass_dict

		self.model.save(setting_dict,voxelSetting_dict,featureClass_dict)

		if len(self.model.yaml_file)>0:
			self.view.save_load_label_text = 'Parameters saved to:\n  '+self.model.yaml_file 
			self.view.show_save_load_label() 
			self.view.next_button['state'] = 'normal'
			self.view.next_button_state = 'normal'
			self.load_options()

	def browse_dir(self):
		dir_path = self.model.browse_dir(self.step_name)
		self.view.path_entry.contents.set(dir_path)
		self.view.path_entry.focus_set()

		if self.step_name == 'Step 2' and len(self.model.subject_list) > 0:
			self.directory_browse_flag = True
			self.file_list_modified = False
			if self.directory_radio_flag == True:
				self.view.next_button['state'] = 'normal'
			self.model.default_image_path = self.model.data_path + '/' + self.model.subject_list[0]
			self.model.default_roi_path = self.model.data_path + '/' + self.model.subject_list[0]

		elif self.step_name == 'Step 3' and len(self.model.image_path) > 0:
			self.model.init_image_files_list()
			if len(self.model.roi_files_list) > 0:
				self.model.init_all_files_list()
			self.update_file_lists()
			self.view.next_button['state'] = 'normal'

		elif self.step_name == 'Step 4' and len(self.model.roi_path) > 0:
			self.view.next_button['state'] = 'normal'
			self.model.init_image_files_list()
			self.model.init_roi_files_list()
			self.model.init_all_files_list()
			self.update_file_lists()

	def image_add_button(self):
		self.file_list_modified = True
		indices = self.view.all_files_list.listbox.curselection()
		if len(indices) > 0:
			index_to_add = indices[0]
			file_to_add = self.model.all_files_list[index_to_add]

			lines = self.view.image_files_list.listbox.size()
			if self.model.image_files_list.count(file_to_add) == 0:
				self.view.image_files_list.listbox.insert(lines, file_to_add)
				self.model.image_files_list.append(file_to_add)

			if self.model.check_file_list_valid():
				self.view.next_button['state'] = 'normal'
			else:
				self.view.next_button['state'] = 'disabled'

	def roi_add_button(self):
		self.file_list_modified = True
		indices = self.view.all_files_list.listbox.curselection()
		if len(indices) > 0:
			index_to_add = indices[0]
			file_to_add = self.model.all_files_list[index_to_add]

			lines = self.view.roi_files_list.listbox.size()
			if self.model.roi_files_list.count(file_to_add) == 0:
				self.view.roi_files_list.listbox.insert(lines, file_to_add)
				self.model.roi_files_list.append(file_to_add)

			if self.model.check_file_list_valid():
				self.view.next_button['state'] = 'normal'
			else:
				self.view.next_button['state'] = 'disabled'

	def update_file_lists(self):
		self.view.params['all_files_list']['height'] = len(self.model.all_files_list) * (12+10)
		self.view.params['image_files_list']['height'] = self.view.params['all_files_list']['height']
		self.view.params['image_files_list']['button_y'] = \
			self.view.params['image_files_list']['height'] + self.view.params['image_files_list']['y'] + 4
		self.view.params['roi_files_list']['height'] = self.view.params['all_files_list']['height']
		self.view.params['roi_files_list']['button_y'] = \
			self.view.params['roi_files_list']['height'] + self.view.params['roi_files_list']['y'] + 4

		self.view.all_files_list.update_file_list(self.model.all_files_list)
		self.view.image_files_list.update_file_list(self.model.image_files_list)
		self.view.roi_files_list.update_file_list(self.model.roi_files_list)

	def all_files_list_event(self, event):
		all_files_cursor = self.view.all_files_list.listbox.curselection()
		image_files_cursor = self.view.image_files_list.listbox.curselection()
		roi_files_cursor = self.view.roi_files_list.listbox.curselection()

		if len(all_files_cursor) > 0 or len(image_files_cursor) == 0 or len(roi_files_cursor) == 0:
			self.view.image_files_list.add_button["state"] = "normal"
			self.view.image_files_list.del_button["state"] = "disabled"
			self.view.roi_files_list.add_button["state"] = "normal"
			self.view.roi_files_list.del_button["state"] = "disabled"

		if len(roi_files_cursor) > 0:
			self.view.image_files_list.add_button["state"] = "disabled"
			self.view.roi_files_list.add_button["state"] = "disabled"
			self.view.image_files_list.del_button["state"] = "disabled"
			self.view.roi_files_list.del_button["state"] = "normal"

		elif len(image_files_cursor) > 0:
			self.view.image_files_list.add_button["state"] = "disabled"
			self.view.roi_files_list.add_button["state"] = "disabled"
			self.view.image_files_list.del_button["state"] = "normal"
			self.view.roi_files_list.del_button["state"] = "disabled"

	def image_files_list_event(self, event):
		image_files_cursor = self.view.image_files_list.listbox.curselection()
		roi_files_cursor = self.view.roi_files_list.listbox.curselection()
		all_files_cursor = self.view.all_files_list.listbox.curselection()
		if len(all_files_cursor) > 0:
			self.view.image_files_list.add_button["state"] = "normal"
			self.view.roi_files_list.add_button["state"] = "normal"
			self.view.image_files_list.del_button["state"] = "disabled"
			self.view.roi_files_list.del_button["state"] = "disabled"

		elif len(roi_files_cursor) > 0:
			self.view.image_files_list.add_button["state"] = "disabled"
			self.view.roi_files_list.add_button["state"] = "disabled"
			self.view.image_files_list.del_button["state"] = "disabled"
			self.view.roi_files_list.del_button["state"] = "normal"

		elif len(image_files_cursor) > 0:
			self.view.image_files_list.add_button["state"] = "disabled"
			self.view.roi_files_list.add_button["state"] = "disabled"
			self.view.image_files_list.del_button["state"] = "normal"
			self.view.roi_files_list.del_button["state"] = "disabled"

	def image_del_button(self):
		self.file_list_modified = True

		image_files_cursor = self.view.image_files_list.listbox.curselection()
		if len(image_files_cursor) == 0:
			return True
		index_to_del = image_files_cursor[0]
		self.view.image_files_list.listbox.delete(index_to_del)
		self.model.image_files_list.pop(index_to_del)

		if len(self.model.image_files_list) == 0:
			self.view.next_button["state"] = "disabled"
			return True

		if self.model.check_file_list_valid():
			self.view.next_button['state'] = 'normal'
		else:
			self.view.next_button['state'] = 'disabled'

		if index_to_del >= len(self.model.image_files_list):
			index = len(self.model.image_files_list)-1
		else:
			index = index_to_del

		self.view.image_files_list.listbox.selection_set(index)
		self.view.image_files_list.listbox.see(index)
		self.view.image_files_list.listbox.activate(index)
		self.view.image_files_list.listbox.selection_anchor(index)

	def roi_files_list_event(self, event):
		all_files_cursor = self.view.all_files_list.listbox.curselection()
		image_files_cursor = self.view.image_files_list.listbox.curselection()
		roi_files_cursor = self.view.roi_files_list.listbox.curselection()

		if len(all_files_cursor) > 0:
			self.view.image_files_list.add_button["state"] = "normal"
			self.view.roi_files_list.add_button["state"] = "normal"
			self.view.image_files_list.del_button["state"] = "disabled"
			self.view.roi_files_list.del_button["state"] = "disabled"

		elif len(image_files_cursor) > 0:
			self.view.image_files_list.add_button["state"] = "disabled"
			self.view.roi_files_list.add_button["state"] = "disabled"
			self.view.image_files_list.del_button["state"] = "normal"
			self.view.roi_files_list.del_button["state"] = "disabled"
		
		elif len(roi_files_cursor) > 0:
			self.view.image_files_list.add_button["state"] = "disabled"
			self.view.roi_files_list.add_button["state"] = "disabled"
			self.view.image_files_list.del_button["state"] = "disabled"
			self.view.roi_files_list.del_button["state"] = "normal"

	def roi_del_button(self):
		self.file_list_modified = True
		roi_files_cursor = self.view.roi_files_list.listbox.curselection()
		if len(roi_files_cursor) == 0:
			return True

		index_to_del = roi_files_cursor[0]
		self.view.roi_files_list.listbox.delete(index_to_del)
		self.model.roi_files_list.pop(index_to_del)

		if len(self.model.roi_files_list) == 0:
			self.view.next_button["state"] = "disabled"
			return True

		if self.model.check_file_list_valid():
			self.view.next_button['state'] = 'normal'
		else:
			self.view.next_button['state'] = 'disabled'

		if index_to_del >= len(self.model.roi_files_list):
			index = len(self.model.roi_files_list)-1
		else:
			index = index_to_del

		self.view.roi_files_list.listbox.selection_set(index)
		self.view.roi_files_list.listbox.see(index)
		self.view.roi_files_list.listbox.activate(index)
		self.view.roi_files_list.listbox.selection_anchor(index)

	def option_event(self):
		self.view.next_button['state'] = 'disabled'
		self.view.save_load_label['text'] = ''
		for options_object in [self.view.setting,self.view.voxelSetting,self.view.featureClass]:
			for i, option in enumerate(options_object.options_list):
				show_flag = options_object.options_vars[option].get()
				option_dict = options_object.options_dicts[i]

				if option_dict['has_entry'] or option_dict['has_entries']:
					if show_flag == 1:
						options_object.show_entries(option)
					else:
						options_object.hide_entries(option)		

				if option == 'voxelBased':
					if show_flag:
						self.view.featureClass.options_vars['shape'].set(0)
						self.view.featureClass.options_buttons['shape']['state'] = 'disabled'
						self.view.voxelSetting.activate_all()
					else:
						self.view.featureClass.options_buttons['shape']['state'] = 'normal'
						for voxelSetting_option in self.view.voxelSetting.options_list:
							if voxelSetting_option == 'voxelBased':
								self.view.voxelSetting.options_vars[voxelSetting_option].set(0)
							else:
								self.view.voxelSetting.options_buttons[voxelSetting_option]['state'] = 'disabled'
								self.view.voxelSetting.options_vars[voxelSetting_option].set(0)
								self.view.voxelSetting.hide_entries(voxelSetting_option)

				elif option == 'shape':
					if show_flag:
						self.view.voxelSetting.deactivate_all()
						self.view.voxelSetting.options_vars['voxelBased'].set(0)
					else:
						self.view.voxelSetting.options_buttons['voxelBased']['state'] = 'normal'

	def directory_radio(self):
		self.directory_radio_flag = True
		selection = "You selected the option " + str(self.view.directory_radio.radio_var.get())

		if self.directory_browse_flag == True:
			self.view.next_button['state'] = 'normal'

		if self.view.directory_radio.radio_var.get()==1:
			if self.model.directory_setup == 'diff':
				self.file_list_modified = False
			self.model.directory_setup = 'same'

		elif self.view.directory_radio.radio_var.get()==2:
			if self.model.directory_setup == 'same':
				self.file_list_modified = False
				self.model.image_path = ''
				self.model.roi_path = ''
			self.model.directory_setup = 'diff'
