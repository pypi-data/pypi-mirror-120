import tkinter as tk
import tkinter.font as tkFont
import tkinter.scrolledtext as ScrolledText
from tkinter import StringVar, IntVar

class View():
	def __init__(self, parent, controller):
		self.step = 'Step 1'
		self.controller = controller


		self.init_params(self.controller)

		self.wiz_steps = WizList(parent)
		self.instruction = self.init_instruction(parent)
		self.path_entry = self.init_path_entry(parent)	
		self.save_load_label = self.init_save_load_label(parent)			
		self.save_load_label_text = ''
		
		self.next_button = self.init_button(parent,self.params['next_button']) 
		self.back_button = self.init_button(parent,self.params['back_button'])
		self.load_button = self.init_button(parent,self.params['load_button'])
		self.save_button = self.init_button(parent,self.params['save_button'])
		self.browse_dir_button = self.init_button(parent,self.params['browse_dir_button'])

		self.all_files_list = FileList(parent,self.params['all_files_list'],self.controller)
		self.image_files_list = FileList(parent,self.params['image_files_list'],self.controller)
		self.roi_files_list = FileList(parent,self.params['roi_files_list'],self.controller)
		self.directory_radio = RadioSelect(parent,self.params['directory_radio'],self.controller)

		self.logs = self.init_logs(parent,self.params['logs'])

		self.hide_buttons()
		self.hide_path_entry()
		self.roi_files_list.hide()
		self.image_files_list.hide()
		self.all_files_list.hide()

		self.setting = ExtractionOptions(parent,self.params['setting'],self.controller)
		self.voxelSetting = ExtractionOptions(parent,self.params['voxelSetting'],self.controller)
		self.featureClass = ExtractionOptions(parent,self.params['featureClass'],self.controller)
		self.init_voxelSetting()
		
		self.wiz_steps.activate(self.step)
		self.show_step1(parent, controller)
		self.next_button['state'] = 'disabled'

	def init_params(self,controller):
		# logging parameters
		logs = {'font':'Arial','fontsize':12,'x':250,'y':160,'width':500,'height':300,'text':'logs'}

		# button parameters
		next_button = {'font':'Arial','fontsize':12,'x':730,'y':520,'width':64,'height':24,'text':'Next','command':controller.next}
		back_button = {'font':'Arial','fontsize':12,'x':640,'y':520,'width':64,'height':24,'text':'Back','command':controller.back}
		load_button = {'font':'Arial','fontsize':12,'x':250,'y':350,'width':64,'height':24,'text':'Load','command':controller.load}
		save_button = {'font':'Arial','fontsize':12,'x':250+64+24,'y':350,'width':64,'height':24,'text':'Save','command':controller.save}
		browse_dir_button = {'font':'Arial','fontsize':12,'x':730,'y':123,'width':64,'height':24,'text':'Browse','command':controller.browse_dir}
		
		# directory setup parameters
		directory_radio = {'font':'Arial','fontsize':12,'x':250,'y':160,'width':232,'height':100, 'dx2':232+12,  \
						'label_fontsize':16,'label_y':160,'label_height':26, \
						'button_font':'Arial','button_fontsize':12,'button_y':None,'button_width':None, \
						'text1':'Images & ROIs in Same Folder','text2':'Images & ROIs in Subfolders'}
		
		# path entry parameters
		path_entry = {'font':'Arial','fontsize':12,'x':250,'y':120,'width':472,'height':30}

		# save / load label
		save_load_label = {'font':'Arial','fontsize':12,'x':250,'y':350+32,'width':None,'height':None,'text':''}
		
		# file list object parameters
		all_files_list = {'font':'Arial','fontsize':12,'x':250,'y':160,'width':175,'height':100,  \
						'label_fontsize':16,'label_y':138,'label_height':26, \
						'button_font':'Arial','button_fontsize':12,'button_y':None,'button_width':None, \
						'button_height':24, 'add_x':None, 'del_x':None,'text':'All Files'}
		
		image_files_list = {'font':'Arial','fontsize':12,'x':437,'y':160,'width':175,'height':100,  \
						'label_fontsize':16,'label_y':138,'label_height':26, \
						'button_font':'Arial','button_fontsize':12,'button_y':None,'button_width':64, \
						'button_height':24, 'add_x':437, 'del_x':437+68,'text':'Image Files'}
		
		roi_files_list = {'font':'Arial','fontsize':12,'x':624,'y':160,'width':175,'height':100,  \
						'label_fontsize':16,'label_y':138,'label_height':26, \
						'button_font':'Arial','button_fontsize':12,'button_y':None,'button_width':64, \
						'button_height':24, 'add_x':624, 'del_x':624+68,'text':'ROI Files'}

		# setting parameters
		force2D = {'has_entry':False,'dx':None, 'width':None,'height':12+4,'has_entries':False,"dy":12,'default':None}
		normalize = {'has_entry':False,'dx':None, 'width':None,'height':12+4,'has_entries':False,'dy':12,'default':None}
		binWidth = {'has_entry':True,'entry_type':float(25.0),'dx':90, 'width':32,'height':12+4, 'has_entries':False,'dy':12,'default':25.0}
		removeOutliers = {'has_entry':True,'entry_type':float(3.0),'dx':135, 'width':32,'height':12+4,'has_entries':False,'dy':12,'default':3.0}
		resampledPixelSpacing = {'has_entry':False,'entry_type':float(3.0),'dx':[24,24+32+4,24+2*(32+4)], 'width':32,'height':12+4,'has_entries':True,'dy':12+16,'default':[3.0,3.0,3.0]}

		setting_list = [('force2D',force2D),('normalize',normalize),('binWidth',binWidth),\
						('removeOutliers',removeOutliers),('resampledPixelSpacing',resampledPixelSpacing)]

		setting = {'font':'Arial','lb_fontsize':16,'x':250,'y':160,'lb_width':150,'lb_height':32+4, \
						'btn_fontsize':12,'btn_x':250,'btn_y':160+24,'btn_dy':12+16, 'btn_width':150,'btn_height':12+16, \
						'option_list':setting_list,'text':'Settings'}

		# voxelSetting parameters
		voxelBased = {'has_entry':False,'dx':None, 'width':None,'height':12+4,'has_entries':False,"dy":12,'default':None}
		maskedKernel = {'has_entry':False,'dx':None, 'width':None,'height':12+4,'has_entries':False,'dy':12,'default':None}
		downSampling = {'has_entry':False,'dx':None, 'width':None,'height':12+4,'has_entries':False,'dy':12,'default':None}
		kernelRadius = {'has_entry':True,'entry_type':int(2),'dx':90+32, 'width':32,'height':12+4, 'has_entries':False,'dy':12,'default':2}
		voxelBatch = {'has_entry':True,'entry_type':int(10000),'dx':90+16, 'width':64,'height':12+4,'has_entries':False,'dy':12,'default':10000}
		initValue = {'has_entry':True,'entry_type':float(0.0),'dx':90, 'width':32,'height':12+4,'has_entries':False,'dy':12,'default':0.0}

		voxelSetting_list = [('voxelBased',voxelBased),('maskedKernel',maskedKernel),('downSampling',downSampling),\
							('kernelRadius',kernelRadius),('voxelBatch',voxelBatch),('initValue',initValue)]

		voxelSetting = {'font':'Arial','lb_fontsize':16,'x':250+210,'y':160,'lb_width':150,'lb_height':32+4, \
						'btn_fontsize':12,'btn_x':250+210,'btn_y':160+24,'btn_dy':12+16, 'btn_width':150,'btn_height':12+16, \
						'option_list':voxelSetting_list,'text':'Voxel Settings'}

		# featureClass parameters
		shape = {'has_entry':False,'dx':None, 'width':None,'height':12+4,'has_entries':False,"dy":12,'default':None}
		firstorder = {'has_entry':False,'dx':None, 'width':None,'height':12+4,'has_entries':False,"dy":12,'default':None}
		glcm = {'has_entry':False,'dx':None, 'width':None,'height':12+4,'has_entries':False,"dy":12,'default':None}
		glszm = {'has_entry':False,'dx':None, 'width':None,'height':12+4,'has_entries':False,"dy":12,'default':None}
		glrlm = {'has_entry':False,'dx':None, 'width':None,'height':12+4,'has_entries':False,"dy":12,'default':None}
		ngtdm = {'has_entry':False,'dx':None, 'width':None,'height':12+4,'has_entries':False,"dy":12,'default':None}
		gldm = {'has_entry':False,'dx':None, 'width':None,'height':12+4,'has_entries':False,"dy":12,'default':None}

		featureClass_list =[('shape',shape),('firstorder',firstorder),('glcm',glcm),('glszm',glszm),('glrlm',glrlm),('ngtdm',ngtdm),('gldm',gldm)]

		featureClass = {'font':'Arial','lb_fontsize':16,'x':250+390,'y':160,'lb_width':150,'lb_height':32+4, \
						'btn_fontsize':12,'btn_x':250+390,'btn_y':160+24,'btn_dy':12+16, 'btn_width':150,'btn_height':12+16, \
						'option_list':featureClass_list,'text':'Feature Classes'}

		# pack parameters
		self.params= {'path_entry':path_entry,'browse_dir_button':browse_dir_button, 'back_button':back_button, \
						'next_button':next_button, 'load_button':load_button,'save_button':save_button, \
						'all_files_list':all_files_list, 'image_files_list':image_files_list, 'roi_files_list':roi_files_list, \
						'setting':setting,'voxelSetting':voxelSetting,'featureClass':featureClass, \
						'save_load_label':save_load_label,'directory_radio':directory_radio,'logs':logs}

	def init_logs(self,parent,params):
		logs = ScrolledText.ScrolledText(parent, state='disabled')
		# logs['justify'] = 'left'
		# label['text'] = 'Browse'
		# label['bg'] = '#F0F0F0'
		# label['fg'] = '#000000'
		#logs['anchor'] = 'nw'
		logs['font'] = tkFont.Font(family=params['font'],size=params['fontsize'])
		logs.place(x=params['x'],y=params['y'],width=params['width'],height=params['height'])

		return logs

	def init_voxelSetting(self):
		for voxelSetting_option in self.voxelSetting.options_list:
			if voxelSetting_option == 'voxelBased':
				self.voxelSetting.options_vars[voxelSetting_option].set(0)
			else:
				self.voxelSetting.options_buttons[voxelSetting_option]['state'] = 'disabled'
				self.voxelSetting.options_vars[voxelSetting_option].set(0)
				self.voxelSetting.hide_entries(voxelSetting_option)

	def init_instruction(self, parent):
		font = 'Arial'; fontsize = 30
		x = 250; y = 70; width = 555; height = None
		
		label = tk.Label(parent)
		label['justify'] = 'left'
		label['text'] = 'Browse'
		label['bg'] = '#F0F0F0'
		label['fg'] = '#000000'
		label['anchor'] = 'nw'
		label['text'] = ''
		label['font'] = tkFont.Font(family=font,size=fontsize)
		label.place(x=x,y=y,width=width,height=height)

		return label

	def init_button(self,parent,params):
		button = tk.Button(parent)
		button['justify'] = 'center'
		button['text'] = params['text']
		button['relief'] = 'raised'
		button['bg'] = '#FFFFFF'
		button['fg'] = '#000000'
		button['state'] = 'normal'
		button['font'] = tkFont.Font(family=params['font'],size=params['fontsize'])
		button.place(x=params['x'],y=params['y'],width=params['width'],height=params['height'])
		button['command'] = params['command']

		return button

	def hide_buttons(self):
		self.browse_dir_button.place(x=-1000)
		self.next_button.place(x=-1000)
		self.back_button.place(x=-1000)
		self.load_button.place(x=-1000)
		self.save_button.place(x=-1000)
		self.logs.place(x=-1000)

	def show_button(self,button_key):
		params = self.params[button_key]

		if params['text'] == 'Next':
			self.next_button.place(x=params['x'])
		elif params['text'] == 'Back':
			self.back_button.place(x=params['x'])
		elif params['text'] == 'Browse':
			self.browse_dir_button.place(x=params['x'])
		elif params['text'] == 'Save':
			self.save_button.place(x=params['x'])
		elif params['text'] == 'Load':
			self.load_button.place(x=params['x'])
		elif params['text'] == 'logs':
			self.logs.place(x=params['x'])

	def init_path_entry(self, parent):
		
		params = self.params['path_entry']

		entry = tk.Entry(parent)
		entry.contents = StringVar()
		entry.contents.set('')
		entry['textvariable'] = entry.contents
		entry['borderwidth'] = '2px'
		entry['justify'] = 'left'
		entry['bg']= '#FFFFFF'
		entry['fg'] = '#333333'
		entry['font'] = tkFont.Font(family=params['font'],size=params['fontsize'])
		entry.place(x=params['x'],y=params['y'],width=params['width'],height=params['height'])

		return entry

	def show_path_entry(self):
		params = self.params['path_entry']
		self.path_entry.place(x=params['x']) # ,y=params['y'],width=params['width'],height=params['height'])

	def hide_path_entry(self):
		self.path_entry.place(x=-1000) #,y=-1000)

	def init_save_load_label(self,parent):
		params = self.params['save_load_label']

		label = tk.Label(parent)
		label['fg'] = '#000000'
		label['bg'] = '#F0F0F0'
		label['justify'] = 'left'
		label['text'] = ''
		label['anchor'] = 'nw'
		label['font'] = tkFont.Font(family=params['font'],size=params['fontsize'])
		label.place(x=params['x'],y=params['y'],width=params['width'],height=params['height'])

		return label

	def hide_save_load_label(self):
		self.save_load_label.place(x=-1000)
		pass

	def show_save_load_label(self):
		params = self.params['save_load_label']
		self.save_load_label['text'] = self.save_load_label_text
		self.save_load_label.place(x=params['x'])

	def show_step1(self, parent, controller):
		self.instruction['text'] = 'Set Extraction Parameters:'
		self.hide_buttons()
		self.hide_path_entry()
		self.directory_radio.hide()
		self.setting.show()
		self.voxelSetting.show()
		self.featureClass.show()
		self.show_save_load_label()
		self.show_button('next_button')
		self.show_button('save_button')
		self.show_button('load_button')

	def show_step2(self, parent, controller):
		self.instruction['text'] = 'Select Data Directory:'
		self.hide_buttons()
		self.hide_save_load_label()
		self.setting.hide()
		self.featureClass.hide()
		self.voxelSetting.hide()
		self.all_files_list.hide()
		self.image_files_list.hide()
		self.roi_files_list.hide()
		self.show_path_entry()
		self.show_button('next_button')
		self.show_button('back_button')
		self.show_button('browse_dir_button')
		self.directory_radio.show()
		self.next_button['text'] = 'Next'

	def show_step3(self, parent, controller):
		self.instruction['text'] = 'Select the Images Folder:'
		self.hide_buttons()
		self.directory_radio.hide()
		self.show_button('next_button')
		self.show_button('back_button')
		self.show_button('browse_dir_button')

	def show_step4(self, parent, controller):
		self.instruction['text'] = 'Select the ROIs Folder:'
		self.hide_buttons()
		self.all_files_list.hide()
		self.image_files_list.hide()
		self.roi_files_list.hide()
		self.show_path_entry()
		self.show_button('next_button')
		self.show_button('back_button')
		self.show_button('browse_dir_button')
		self.next_button['text'] = 'Next'

	def show_step5(self, parent, controller):
		self.instruction['text'] = 'Verify Images and ROIs:'
		self.hide_buttons()
		self.hide_path_entry()
		self.directory_radio.hide()
		self.all_files_list.show()
		self.image_files_list.show()
		self.roi_files_list.show()
		self.show_button('back_button')
		self.show_button('next_button')
		self.next_button['text'] = 'Next'

	def show_extraction(self, parent, controller):
		self.instruction['text'] = 'Proceed to Extraction:'
		self.hide_buttons()		
		self.all_files_list.hide()
		self.image_files_list.hide()
		self.roi_files_list.hide()
		self.show_button('back_button')
		self.show_button('next_button')
		self.next_button['text'] = 'Proceed'
		# self.show_button('logs')

class RadioSelect:
	def __init__(self, parent, params, controller):

		self.params = params
		self.init_radioselect(parent,controller)

	def init_radioselect(self,parent,controller):
		params = self.params

		self.radio_var = IntVar()

		radio_same = tk.Radiobutton(parent, text=params['text1'], variable = self.radio_var,value=1,command=controller.directory_radio)
		radio_same["fg"] = "#333333"
		radio_same["bg"]= "#F0F0F0"
		radio_same["justify"] = "left"
		radio_same["anchor"] = "nw"
		radio_same["font"] = tkFont.Font(family=params['font'],size=params['label_fontsize'])
		radio_same.place(x=params['x'], y=params['label_y'], width=params['width'], height=params['label_height'])

		self.radio_same = radio_same

		self.radio_diff_x = params['x']+params['dx2']
		radio_diff = tk.Radiobutton(parent, text=params['text2'], variable = self.radio_var,value=2,command=controller.directory_radio)
		radio_diff["fg"] = "#333333"
		radio_diff["bg"] = "#F0F0F0"
		radio_diff["justify"] = "left"
		radio_diff["anchor"] = "nw"
		radio_diff["font"] = tkFont.Font(family=params['font'],size=params['label_fontsize'])
		radio_diff.place(x=self.radio_diff_x, y=params['label_y'], width=params['width'], height=params['label_height'])

		self.radio_same = radio_same
		self.radio_diff = radio_diff

	def show(self):
		params = self.params
		self.radio_same.place(x=params['x'])
		self.radio_diff.place(x=self.radio_diff_x)

	def hide(self):
		self.radio_same.place(x=-1000)
		self.radio_diff.place(x=-1000)

class ExtractionOptions:
	def __init__(self, parent, params, controller):

		self.params = params
		self.options_list = [a_tuple[0] for a_tuple in self.params['option_list']]
		self.options_dicts = [a_tuple[1] for a_tuple in self.params['option_list']]
		self.options_buttons = {}
		self.options_vars = {}
		self.options_entries = {}
		self.options_strings = {}
		self.init_options(parent,controller)

	def init_options(self,parent,controller):
		params = self.params

		label = tk.Label(parent)
		label["fg"] = "#000000"
		label["bg"]= "#F0F0F0"
		label["justify"] = "left"
		label["anchor"] = "nw"
		label["text"] = params['text']
		label["font"] = tkFont.Font(family=params['font'],size=params['lb_fontsize'])
		label.place(x=params['x'], y=params['y'], width=params['lb_width'], height=params['lb_height'])

		self.label = label

		for i, option in enumerate(self.options_list):
			option_dict = self.options_dicts[i]
			var = IntVar()
			y_i = params['btn_y'] + i*params['btn_dy']
			check_button=tk.Checkbutton(parent,text=option,variable=var)
			check_button["fg"] = "#333333"
			check_button["bg"] = "#F0F0F0"
			check_button["justify"] = "left"
			check_button["relief"] = "flat"
			check_button["offvalue"] = "0"
			check_button["onvalue"] = "1"
			check_button["font"] = tkFont.Font(family=params['font'],size=params['btn_fontsize'])
			check_button.place(x=params['btn_x'],y=y_i)
			check_button.place(height=params['btn_height'])
			check_button['state'] = 'normal'
			check_button["command"] = controller.option_event
			
			self.options_buttons[option] = check_button
			self.options_vars[option] = var

			has_entry = option_dict['has_entry']
			has_entries = option_dict['has_entries']
			if has_entry:
				entry_string = StringVar() #HERER
				entry_string.set(option_dict['default'])
				entry = tk.Entry(parent,textvariable=entry_string)
				entry['font'] = tkFont.Font(family=params['font'],size=params['btn_fontsize'])
				entry.place(x=-1000,y=y_i,width=option_dict['width'])
				self.options_entries[option] = entry
				self.options_strings[option] = entry_string
			elif has_entries:
					option_entries = []
					option_strings = []
					for j in range(3):
						dx = option_dict['dx'][j]
						entry_string = StringVar()
						entry_string.set(option_dict['default'][j])
						entry = tk.Entry(parent,textvariable=entry_string)
						entry['font'] = tkFont.Font(family=params['font'],size=params['btn_fontsize'])
						entry.place(x=-1000,y=y_i+option_dict['dy'],width=option_dict['width'])
						option_entries.append(entry)
						option_strings.append(entry_string)
					self.options_entries[option] = option_entries
					self.options_strings[option] = option_strings

	def hide(self):
		self.label.place(x=-1000)
		for i, option in enumerate(self.options_list):
			self.options_buttons[option].place(x=-1000)
			option_dict = self.options_dicts[i]
			has_entry = option_dict['has_entry']
			has_entries = option_dict['has_entries']
			if has_entry:
				self.options_entries[option].place(x=-1000)
			elif has_entries:
					for j in range(3):
						self.options_entries[option][j].place(x=-1000)

	def show(self):
		params = self.params
		self.label.place(x=params['x'])

		for i, option in enumerate(self.options_list):
			self.options_buttons[option].place(x=params['btn_x'])
			if self.options_vars[option].get() == 1:
				option_dict = self.options_dicts[i]
				has_entry = option_dict['has_entry']
				has_entries = option_dict['has_entries']

				if has_entry:
					self.options_entries[option].place(x=params['x']+option_dict['dx'])
				elif has_entries:
					for j in range(3):
						self.options_entries[option][j].place(x=params['x']+option_dict['dx'][j])

	def show_entries(self, option):
		if self.options_vars[option].get() == 1:
			params = self.params
			option_index = self.options_list.index(option)
			option_dict = self.options_dicts[option_index]
			
			if option_dict['has_entry']:
					self.options_entries[option].place(x=params['x']+option_dict['dx'])
			elif option_dict['has_entries']:
				for j in range(3):
					self.options_entries[option][j].place(x=params['x']+option_dict['dx'][j])

	def hide_entries(self, option):
		option_index = self.options_list.index(option)
		option_dict = self.options_dicts[option_index]

		if option_dict['has_entry']:
			self.options_entries[option].place(x=-1000)
		elif option_dict['has_entries']:
			for j in range(3):
				self.options_entries[option][j].place(x=-1000)

	def deactivate_all(self):
		for option in self.options_list:
			self.options_buttons[option]['state'] = 'disabled'

	def activate_all(self):
		for option in self.options_list:
			self.options_buttons[option]['state'] = 'normal'

class FileList:
	def __init__(self, parent, params, controller):

		self.params = params
		self.init_filelist(parent,controller)

	def init_filelist(self,parent,controller):
		params = self.params

		label=tk.Label(parent)
		label["fg"] = "#333333"
		label["bg"]= "#F0F0F0"
		label["justify"] = "left"
		label["anchor"] = "nw"
		label["text"] = params['text']
		label["font"] = tkFont.Font(family=params['font'],size=params['label_fontsize'])
		label.place(x=params['x'], y=params['label_y'], width=params['width'], height=params['label_height'])


		listbox=tk.Listbox(parent)
		listbox["fg"] = "#333333"
		listbox["bg"]= "#FFFFFF"
		listbox["justify"] = "left"
		listbox["font"] = tkFont.Font(family=params['font'],size=params['fontsize'])
		listbox.place(x=params['x'], y=params['y'], width=params['width'], height=params['height'])

		if params['text']=='All Files':
			listbox.bind("<<ListboxSelect>>", controller.all_files_list_event)
		elif params['text']=='Image Files':
			listbox.bind("<<ListboxSelect>>", controller.image_files_list_event)
		elif params['text']=='ROI Files':
			listbox.bind("<<ListboxSelect>>", controller.roi_files_list_event)

		if params['button_font'] is not None:
			add_button=tk.Button(parent)
			add_button["fg"] = "#000000"
			add_button["bg"] = "#ffffff"
			add_button["justify"] = "center"
			add_button["text"] = 'Add'
			add_button["font"] = tkFont.Font(family=params['button_font'],size=params['button_fontsize'])
			add_button.place(x=params['add_x'],y=params['button_y'],width=params['button_width'],height=params['button_height'])
			add_button["state"] = 'normal'#"disabled"
			if params['text'] == 'Image Files':
				add_button['command'] = controller.image_add_button
			elif params['text'] == 'ROI Files':
				add_button['command'] = controller.roi_add_button

			del_button=tk.Button(parent)
			del_button["fg"] = "#000000"
			del_button["bg"] = "#ffffff"
			del_button["justify"] = "center"
			del_button["text"] = 'Remove'
			del_button["font"] = tkFont.Font(family=params['button_font'],size=params['button_fontsize'])
			del_button.place(x=params['del_x'],y=params['button_y'],width=params['button_width'],height=params['button_height'])
			del_button["state"] = "normal"
			if params['text'] == 'Image Files':
				del_button['command'] = controller.image_del_button
			elif params['text'] == 'ROI Files':
				del_button['command'] = controller.roi_del_button
		else:
			add_button = None
			del_button = None

		self.listbox = listbox
		self.label = label
		self.add_button = add_button
		self.del_button = del_button

	def hide(self):
		self.label.place(x=-1000)
		self.listbox.place(x=-1000)
		if self.params['button_font'] is not None:
			self.add_button.place(x=-1000)
			self.del_button.place(x=-1000)

	def show(self):
		params = self.params
		self.label.place(x=params['x'])
		self.listbox.place(x=params['x'],height=params['height'])
		if self.params['button_font'] is not None:
			self.del_button.place(x=params['del_x'],y=params['button_y'])
			self.add_button.place(x=params['add_x'],y=params['button_y'])

	def update_file_list(self,files_list):
		self.listbox.delete(0,self.listbox.size())
		for i, file in enumerate(files_list):
			self.listbox.insert( i, file)

class WizList:
	def __init__(self, parent):

		self.fontsize = 30
		self.padsize = 20
		self.dy = 90
		self.y = 70
		self.x = 50

		self.init_wizlist(parent)

	def init_wizlist(self,parent):

		textvars = ['Step 1','Step 2','Step 3','Step 4','Step 5']
		self.wiz_dict = {}

		i = 0
		for step_name in textvars:
			key = step_name

			self.wiz_dict[key] = self.add_step(step_name+'/5',parent)
			self.wiz_dict[key].place(x=self.x,y=self.y + i*self.dy)
			i+=1

	def add_step(self,text,parent):

		step=tk.Label(parent)

		step['fg'] = '#F0F0F0'
		step['bg'] = '#F0F0F0'
		step['justify'] = 'center'
		step['anchor'] = 'nw'
		step['text'] = text
		step['font'] = tkFont.Font(family='Arial',size=self.fontsize)

		return step

	def activate(self,key):
		self.wiz_dict[key]['fg'] = '#000000'
		pass

	def deactivate(self,key):
		self.wiz_dict[key]['fg'] = '#AAAAAA'
		pass

