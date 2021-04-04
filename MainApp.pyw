import json
import math
import os
import shutil
import checklistcombobox
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter import filedialog
from tkinter import font as tkFont
from datetime import datetime


# --------------------------------------------------------------------------------------------------
# MAIN APP CLASS
class App():
	def __init__(self):
		self.root = Tk()		
		# theme and font color
		self.main_theme = "grey35"
		self.text_color = "white"
		self.main_button_color = "grey45"
		self.selected_button_color = "DarkOrange2"
		self.critical_button_color = "firebrick2"
		self.safe_button_color = "green3"
		self.main_font = tkFont.Font(size=11, weight="bold")

		self.main_frame = None
		self.loadMenu()

	# --------------------------------------------------------------------------------------------------
	# --------------------------------------------FUNCTIONS---------------------------------------------
	# --------------------------------------------------------------------------------------------------


	def writeDataAndLoadMenu(self):
		self.write_user_data()
		self.saveCurrentToDict()
		self.writeClipData()
		self.loadMenu()


	def loadMenu(self):
		if(self.main_frame != None):
			self.main_frame.destroy()
		self.root.title("Battlefield 5 Clip Organizer")
		self.root.geometry("664x373")
		self.root.minsize(664, 373)
		self.root.resizable(0,0)
		self.photo = PhotoImage(file="Icons/Misc/MenuBackground.png")
		self.canvas = Canvas(self.root, width=666, height=375)
		self.canvas.create_image(0, 0, anchor=NW, image=self.photo)
		self.canvas.place(x=-2, y=-2)

		# --------------------------------------------------------------------------------------------------
		# MENU BAR
		self.menubar = Menu(self.root, bg=self.main_theme, fg=self.text_color, activebackground="white", activeforeground='black')
		self.file = Menu(self.menubar, tearoff=0, bg=self.main_theme, fg=self.text_color, font=self.main_font)
		self.file.add_command(label="Help", command=self.INFO)
		self.menubar.add_cascade(label="File", menu=self.file)
		self.root.config(menu=self.menubar)

		self.clip_analyser_icon = PhotoImage(file="Icons/Misc/Analyser.png")
		self.clip_analyser_button = Button(self.root, relief="raised", bg=self.main_button_color, fg=self.text_color, image=self.clip_analyser_icon)
		self.clip_analyser_button['command'] = self.ClipAnalyser
		self.clip_analyser_button.image = self.clip_analyser_icon
		self.clip_analyser_button.place(x=422, y=50)

		self.clip_sorter_icon = PhotoImage(file="Icons/Misc/Sorter.png")
		self.clip_sorter_button = Button(self.root, relief="raised", bg=self.main_button_color, fg=self.text_color, image=self.clip_sorter_icon)
		self.clip_sorter_button['command'] = self.ClipSorter
		self.clip_sorter_button.image = self.clip_sorter_icon
		self.clip_sorter_button.place(x=422, y=151)

		self.clip_exit_icon = PhotoImage(file="Icons/Misc/Exit.png")
		self.clip_exit_button = Button(self.root, relief="raised", bg=self.main_button_color, fg=self.text_color, image=self.clip_exit_icon)
		self.clip_exit_button['command'] = self.root.destroy
		self.clip_exit_button.image = self.clip_exit_icon
		self.clip_exit_button.place(x=422, y=251)


	def destroyMenu(self):
		self.canvas.destroy()
		self.clip_sorter_button.destroy()
		self.clip_analyser_button.destroy()
		self.clip_exit_button.destroy()


	def loadClipAnalyser(self):
		self.main_frame.destroy()
		self.ClipAnalyser()

	def loadClipSorter(self):
		self.main_frame.destroy()
		self.ClipSorter()


	def ClipAnalyser(self):
		self.destroyMenu()
		self.root.title("Clip Analyzer")
		self.root.minsize(959, 861)
		self.root.resizable(False,False)
		self.main_theme = "grey35"
		self.text_color = "white"
		self.main_button_color = "grey45"
		self.selected_button_color = "DarkOrange2"
		self.critical_button_color = "firebrick2"
		self.safe_button_color = "green3"
		self.main_font = tkFont.Font(size=11, weight="bold")
		self.root['bg'] = self.main_theme
		self.root.protocol("WM_DELETE_WINDOW", self.on_root_closing)

		# --------------------------------------------------------------------------------------------------
		# MENU BAR
		self.menubar = Menu(self.root, bg=self.main_theme, fg=self.text_color, activebackground="white", activeforeground='black')
		self.file = Menu(self.menubar, tearoff=0, bg=self.main_theme, fg=self.text_color, font=self.main_font)
		self.file.add_command(label="Help", command=self.INFO)
		self.file.add_command(label="Preferences", command=self.openPreferencesWindow)
		self.file.add_command(label="Scan Clip Folder", command=self.scanClipFolder)
		self.file.add_separator()
		self.file.add_command(label="Clip Sorter", command=self.loadClipSorter)
		self.file.add_command(label="Main Menu", command=self.writeDataAndLoadMenu)
		self.menubar.add_cascade(label="File", menu=self.file)
		self.root.config(menu=self.menubar)

		# --------------------------------------------------------------------------------------------------
		# MAIN CLIP DATA BASE
		self.main_data_base = dict()

		# --------------------------------------------------------------------------------------------------
		# USER CONFIG & VARIABLES
		self.write_last_clip = True
		self.clip_data_base_file_path = ""
		self.clip_video_folder_path = ""
		self.user_config_file_path = ""

		self.current_clip_index = 0

		self.primary_weapon_selected = None
		self.secondary_weapon_selected = None

		self.map_selected = None

		self.gadget1_selected = None
		self.gadget2_selected = None
		self.gadget3_selected = None

		####################################################################################################
		####################################################################################################
		# CLIP DATA VARIABLES

		"""
		BUG 
		- When scrolling in clip sorter on vertical monitor setup canvas can be blocked outside the scroll zone...

		TO ADD :
		
		- dans la partie "clip sorter" ajouter la possibilité de copier les clips vers un autre dossier

		- ajouter un menu pour sauvegarder de presets de classe
		- possibilite de changer le nom du clip +++
		- ajouter une zone de texte limite 140 ou 240 char? => comment on gere les accents ++
		- fct pour copier dans le clip board les parametres du clip +
		- lien avec le battle report? (mais dead game donc pk?) +

		
		self.clip_name_list[self.current_clip_index]
		
		self.country_selected
		
		self.clip_grade_selected
		
		self.kill_count_selected
		
		self.class_selected
		
		self.primary_weapon_selected
		self.secondary_weapon_selected
		self.melee_weapon_selected
		self.gadget_1_selected
		self.gadget_2_selected
		self.gadget_3_selected

		self.reinforcements_selected
	
		self.vehicule_selected
		self.map_selected

		"""
		####################################################################################################
		####################################################################################################


		# --------------------------------------------------------------------------------------------------
		# MAIN STACK FRAME
		self.main_frame = Frame(self.root, borderwidth=0, bg=self.main_theme)
		self.main_frame.pack()	

		# --------------------------------------------------------------------------------------------------
		# MAIN RIGHT STACK FRAME
		self.main_stack_frame = Frame(self.main_frame, borderwidth=0, bg=self.main_theme)
		self.main_stack_frame.pack(side=RIGHT)	

		# --------------------------------------------------------------------------------------------------
		# CLIP NAME LABEL
		self.clip_label_frame = Frame(self.main_stack_frame, borderwidth=0, bg=self.main_theme)
		self.clip_label_frame.pack(side=TOP)

		self.combobox_button_frame = LabelFrame(self.clip_label_frame, text="Quick clip acces", font=self.main_font, labelanchor="n", borderwidth=2, bg=self.main_theme, fg=self.text_color, height=64)
		self.combobox_button_frame.pack(side=LEFT)

		self.clip_scroll_list = Combobox(self.combobox_button_frame, width=40, height=40, justify=LEFT, state="readonly")
		self.clip_scroll_list.pack(side=LEFT, padx=5, pady=5)

		self.scroll_list_retrieve = Button(self.combobox_button_frame, text="Select", font=self.main_font, bg=self.main_button_color, fg=self.text_color, command=self.scrollListRetrieve)
		self.scroll_list_retrieve.pack(side=LEFT, padx=5, pady=5)

		self.clip_name_frame = LabelFrame(self.clip_label_frame, text="Current Clip", font=self.main_font, labelanchor="n", borderwidth=2, bg=self.main_theme, fg=self.text_color, height=65)
		self.clip_name_frame.pack(side=LEFT, fill=Y, expand=True)

		clip_name_font = tkFont.Font(size=16, weight="bold")
		
		self.clip_label = Label(self.clip_name_frame, text="", font=clip_name_font, bg=self.main_theme, fg=self.text_color, anchor=N, width=40)
		self.clip_label.pack(side=LEFT, padx=5, pady=5, fill=Y)

		# --------------------------------------------------------------------------------------------------
		# COUNTRY & VEHICULES & GRADE & KILL & TAGS FRAME
		self.country_tags_frame = Frame(self.main_stack_frame, bg=self.main_theme)
		self.country_tags_frame.pack(side=TOP, fill=X)

		# --------------------------------------------------------------------------------------------------
		# COUNTRY BUTTON SELECTOR
		self.country_vehicule_frame = LabelFrame(self.country_tags_frame, bg=self.main_theme, bd=2, width=426, height=410)
		self.country_vehicule_frame.pack_propagate(0)
		self.country_vehicule_frame.pack(side=LEFT, fill=BOTH, expand=True)

		self.country_frame = LabelFrame(self.country_vehicule_frame, text="Nation", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color)
		self.country_frame.pack(side=LEFT, anchor=N, padx=(10,0), pady=5)

		self.country_selected = None
		self.last_COUNTRY_clicked = None

		# germany button
		iconGE = PhotoImage(file="Icons/Country/Small/GE.png")
		self.buttonGE = Button(self.country_frame, text="GE", relief="raised", bg=self.main_button_color, image=iconGE)
		self.buttonGE.image = iconGE
		self.buttonGE['command'] = self.buttonGE_clicked
		self.buttonGE.pack(side=TOP, pady=(0,5))
		# japon button
		iconJP = PhotoImage(file="Icons/Country/Small/JP.png")
		self.buttonJP = Button(self.country_frame, text="JP", relief="raised", bg=self.main_button_color, image=iconJP)
		self.buttonJP.image = iconJP
		self.buttonJP['command'] = self.buttonJP_clicked
		self.buttonJP.pack(side=TOP, pady=(0,5))
		# united kingdom button
		iconUK = PhotoImage(file="Icons/Country/Small/UK.png")
		self.buttonUK = Button(self.country_frame, text="UK", relief="raised", bg=self.main_button_color, image=iconUK)
		self.buttonUK.image = iconUK
		self.buttonUK['command'] = self.buttonUK_clicked
		self.buttonUK.pack(side=TOP, pady=(0,5))
		# united states of america button
		iconUSA = PhotoImage(file="Icons/Country/Small/USA.png")
		self.buttonUSA = Button(self.country_frame, text="USA", relief="raised", bg=self.main_button_color, image=iconUSA)
		self.buttonUSA.image = iconUSA
		self.buttonUSA['command'] = self.buttonUSA_clicked
		self.buttonUSA.pack(side=TOP, pady=(0,5))

		self.button_COUNTRY_ref = [self.buttonGE, self.buttonJP, self.buttonUK, self.buttonUSA]

		# --------------------------------------------------------------------------------------------------
		# GRADE & KILL & TAGS && MEDIA CONTROL
		self.grade_media_frame = LabelFrame(self.country_tags_frame, borderwidth=2, bg=self.main_theme, fg=self.text_color)
		self.grade_media_frame.pack(side=LEFT, anchor=N, fill=Y)

		# --------------------------------------------------------------------------------------------------
		# SAVE & RESET & MEDIA CONTROL FRAME
		self.save_r_media_frame = Frame(self.grade_media_frame, borderwidth=0, bg=self.main_theme)
		self.save_r_media_frame.pack(side=TOP, fill=X)

		# --------------------------------------------------------------------------------------------------
		# SAVE & RESET FRAME
		self.save_reset_frame = LabelFrame(self.save_r_media_frame, text="Data", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color)
		self.save_reset_frame.pack(side=LEFT, padx=(7,0))

		# --------------------------------------------------------------------------------------------------
		# SAVE BUTTON
		save_icon = PhotoImage(file="Icons/Misc/Save.png")
		self.save_button = Button(self.save_reset_frame, relief="raised", bg=self.safe_button_color, fg=self.text_color, image=save_icon)
		self.save_button.image = save_icon
		self.save_button['command'] = self.button_save_clicked
		self.save_button.pack(side=TOP)

		# --------------------------------------------------------------------------------------------------
		# RESET BUTTON
		reset_icon = PhotoImage(file="Icons/Misc/Reset.png")
		self.reset_button = Button(self.save_reset_frame, relief="raised", bg=self.critical_button_color, fg=self.text_color, image=reset_icon)
		self.reset_button.image = reset_icon
		self.reset_button['command'] = self.button_reset_clicked
		self.reset_button.pack(side=TOP)

		# --------------------------------------------------------------------------------------------------
		# NEXT & PREVIOUS & PLAY FRAME
		self.next_previous_play_frame = LabelFrame(self.save_r_media_frame, text="Media control", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color)
		self.next_previous_play_frame.pack(side=RIGHT, padx=5, pady=5)

		# --------------------------------------------------------------------------------------------------
		# PREVIOUS CLIP BUTTON
		previous_icon = PhotoImage(file="Icons/Misc/Previous.png")
		self.previous_clip_button = Button(self.next_previous_play_frame, relief="raised", bg=self.main_button_color, fg=self.text_color, image=previous_icon)
		self.previous_clip_button.image = previous_icon
		self.previous_clip_button['command'] = self.button_previous_clicked
		self.previous_clip_button.pack(side=LEFT, padx=(0,5), pady=5)

		# --------------------------------------------------------------------------------------------------
		# PLAY CLIP IN DEFAULT PLAYER BUTTON
		play_icon = PhotoImage(file="Icons/Misc/Play.png")
		self.play_clip = Button(self.next_previous_play_frame, relief="raised", bg=self.main_button_color, image=play_icon)
		self.play_clip.image = play_icon
		self.play_clip['command'] = self.openInDefaultPlayer
		self.play_clip.pack(side=LEFT, pady=5)

		# --------------------------------------------------------------------------------------------------
		# NEXT CLIP BUTTON
		next_icon = PhotoImage(file="Icons/Misc/Next.png")
		self.next_clip_button = Button(self.next_previous_play_frame, relief="raised", bg=self.main_button_color, fg=self.text_color, image=next_icon)
		self.next_clip_button.image = next_icon
		self.next_clip_button['command'] = self.button_next_clicked
		self.next_clip_button.pack(side=LEFT, padx=(5,0), pady=5)

		# --------------------------------------------------------------------------------------------------
		# GRADE BUTTON SELECTOR
		self.grade_kill_tag_frame = Frame(self.grade_media_frame, bg=self.main_theme)
		self.grade_kill_tag_frame.pack(side=TOP, anchor=N)

		self.grade_kill_counter_frame = Frame(self.grade_kill_tag_frame, borderwidth=2, bg=self.main_theme, width=434)
		self.grade_kill_counter_frame.pack(side=TOP, fill=X)

		self.grade_frame = LabelFrame(self.grade_kill_counter_frame, text="Grade clip", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color)
		self.grade_frame.pack(side=LEFT, padx=5, pady=5)

		self.button_star_pressed = [False,False,False,False,False]
		self.clip_grade_selected = None

		# star button 1
		iconSTAR = PhotoImage(file="Icons/Misc/Star.png")
		self.buttonSTAR1 = Button(self.grade_frame, relief="raised", bg=self.main_button_color, image=iconSTAR)
		self.buttonSTAR1.image = iconSTAR
		self.buttonSTAR1['command'] = self.buttonSTAR1_clicked
		self.buttonSTAR1.pack(side=LEFT)
		# star button 2
		self.buttonSTAR2 = Button(self.grade_frame, relief="raised", bg=self.main_button_color, image=iconSTAR)
		self.buttonSTAR2.image = iconSTAR
		self.buttonSTAR2['command'] = self.buttonSTAR2_clicked
		self.buttonSTAR2.pack(side=LEFT)
		# star button 3
		self.buttonSTAR3 = Button(self.grade_frame, relief="raised", bg=self.main_button_color, image=iconSTAR)
		self.buttonSTAR3.image = iconSTAR
		self.buttonSTAR3['command'] = self.buttonSTAR3_clicked
		self.buttonSTAR3.pack(side=LEFT)
		# star button 4
		self.buttonSTAR4 = Button(self.grade_frame, relief="raised", bg=self.main_button_color, image=iconSTAR)
		self.buttonSTAR4.image = iconSTAR
		self.buttonSTAR4['command'] = self.buttonSTAR4_clicked
		self.buttonSTAR4.pack(side=LEFT)
		# star button 5
		self.buttonSTAR5 = Button(self.grade_frame, relief="raised", bg=self.main_button_color, image=iconSTAR)
		self.buttonSTAR5.image = iconSTAR
		self.buttonSTAR5['command'] = self.buttonSTAR5_clicked
		self.buttonSTAR5.pack(side=LEFT)

		self.button_STAR_ref = [self.buttonSTAR1, self.buttonSTAR2, self.buttonSTAR3, self.buttonSTAR4, self.buttonSTAR5]

		# --------------------------------------------------------------------------------------------------
		# KILL COUNTER
		self.kill_counter_frame = LabelFrame(self.grade_kill_counter_frame, text="Kill Counter", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color)
		self.kill_counter_frame.pack(side=RIGHT, padx=5, pady=5)

		self.mouse_over_kill_counter = False
		self.kill_counter = 0

		# minus button
		button_font = tkFont.Font(size=16, weight="bold")
		iconVIRTUAL = PhotoImage(width=1, height=1)
		self.buttonMINUS = Button(self.kill_counter_frame, text="-", fg="white", font=button_font, relief="raised", bg=self.main_button_color, width=3, height=1)
		self.buttonMINUS['command'] = self.buttonMINUS_clicked
		self.buttonMINUS.pack(side=LEFT)

		# kill count button
		button_font = tkFont.Font(size=18, weight="bold")
		self.buttonKILLCOUNTER = Button(self.kill_counter_frame, text=str(self.kill_counter), fg="white",relief="raised", font=button_font, bg=self.main_button_color, width=3, height=1)
		self.buttonKILLCOUNTER['command'] = self.buttonKILLCOUNTER_clicked
		self.buttonKILLCOUNTER.bind("<Enter>", self._on_enter_kill_counter)
		self.buttonKILLCOUNTER.bind("<Leave>", self._on_leave_kill_counter)
		self.buttonKILLCOUNTER.bind_all("<MouseWheel>", self._on_mousewheel)
		self.buttonKILLCOUNTER.pack(side=LEFT)

		# plus button
		button_font = tkFont.Font(size=16, weight="bold")
		iconVIRTUAL = PhotoImage(width=1, height=1)
		self.buttonPLUS = Button(self.kill_counter_frame, text="+", fg="white", font=button_font, relief="raised", bg=self.main_button_color, width=3, height=1)
		self.buttonPLUS['command'] = self.buttonPLUS_clicked
		self.buttonPLUS.pack(side=LEFT)

		# --------------------------------------------------------------------------------------------------
		# CLASS BUTTON SELECTOR
		# class button frame
		self.class_frame = LabelFrame(self.grade_media_frame, text="Class selector", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color)
		self.class_frame.pack(side=TOP, pady=(25,5))

		# button class tab
		self.class_selected = None
		self.last_CLASS_clicked = None

		# button ASSAULT
		iconASSAULT = PhotoImage(file="Icons/Class/ASSAULT.png")
		self.buttonASSAULT = Button(self.class_frame, relief="raised", bg=self.main_button_color, image=iconASSAULT)
		self.buttonASSAULT.image = iconASSAULT
		self.buttonASSAULT['command'] = self.buttonASSAULT_clicked
		self.buttonASSAULT.pack(side=LEFT)

		# button MEDIC
		iconMEDIC = PhotoImage(file="Icons/Class/MEDIC.png")
		self.buttonMEDIC = Button(self.class_frame, relief="raised", bg=self.main_button_color, image=iconMEDIC)
		self.buttonMEDIC.image = iconMEDIC
		self.buttonMEDIC['command'] = self.buttonMEDIC_clicked
		self.buttonMEDIC.pack(side=LEFT)

		# button SUPPORT
		iconSUPPORT = PhotoImage(file="Icons/Class/SUPPORT.png")
		self.buttonSUPPORT = Button(self.class_frame, relief="raised", bg=self.main_button_color, image=iconSUPPORT)
		self.buttonSUPPORT.image = iconSUPPORT
		self.buttonSUPPORT['command'] = self.buttonSUPPORT_clicked
		self.buttonSUPPORT.pack(side=LEFT)

		# button RECON
		iconRECON = PhotoImage(file="Icons/Class/RECON.png")
		self.buttonRECON = Button(self.class_frame, relief="raised", bg=self.main_button_color, image=iconRECON)
		self.buttonRECON.image = iconRECON
		self.buttonRECON['command'] = self.buttonRECON_clicked
		self.buttonRECON.pack(side=LEFT)

		self.button_CLASS_ref = [self.buttonASSAULT, self.buttonMEDIC, self.buttonSUPPORT, self.buttonRECON]

		# --------------------------------------------------------------------------------------------------
		# WEAPON FRAME
		self.weapon_frame = LabelFrame(self.main_stack_frame, text="Weapons", font=self.main_font, labelanchor="n", borderwidth=2, bg=self.main_theme, fg=self.text_color, width=842)
		#self.weapon_frame.pack_propagate(0)
		self.weapon_frame.pack(side=TOP, fill=BOTH, expand=True)

		self.w1_w2_g1_g2_g3_frame = Frame(self.weapon_frame, bg=self.main_theme)
		self.w1_w2_g1_g2_g3_frame.pack(side=TOP)

		# --------------------------------------------------------------------------------------------------
		# PRIMARY WEAPON BUTTON
		self.primary_weapon_frame = LabelFrame(self.w1_w2_g1_g2_g3_frame, text="Primary", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color, width=332, height=361)
		self.primary_weapon_frame.pack_propagate(False)
		self.primary_weapon_frame.pack(side=LEFT, padx=2, pady=2)

		self.primary_weapon_frame_left = Frame(self.primary_weapon_frame, bg=self.main_theme, borderwidth=0)
		self.primary_weapon_frame_left.pack(side=LEFT, anchor=N)

		self.primary_weapon_frame_right = LabelFrame(self.primary_weapon_frame, bg=self.main_theme, borderwidth=0)
		self.primary_weapon_frame_right.pack(side=RIGHT, anchor=N)

		self.button_primary_weapon_ref = []

		# --------------------------------------------------------------------------------------------------
		# SECONDARY WEAPON & MELEE FRAME
		self.secondary_melee_frame = Frame(self.w1_w2_g1_g2_g3_frame, borderwidth=0, bg=self.main_theme)
		self.secondary_melee_frame.pack(side=LEFT, anchor=N)

		# --------------------------------------------------------------------------------------------------
		# SECONDARY WEAPON BUTTON
		self.secondary_weapon_frame = LabelFrame(self.secondary_melee_frame, text="Secondary", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color)
		#self.secondary_weapon_frame.pack_propagate(False)
		self.secondary_weapon_frame.pack(side=TOP, anchor=N, padx=2, pady=2)

		self.secondary_weapon_frame_left = Frame(self.secondary_weapon_frame, bg=self.main_theme, borderwidth=0)
		self.secondary_weapon_frame_left.pack(side=LEFT, anchor=N)

		self.secondary_weapon_frame_right = LabelFrame(self.secondary_weapon_frame, bg=self.main_theme, borderwidth=0)
		self.secondary_weapon_frame_right.pack(side=RIGHT, anchor=N)

		self.button_secondary_weapon_ref = []

		# --------------------------------------------------------------------------------------------------
		# GADGETS BUTTON
		self.gadget_frame = LabelFrame(self.w1_w2_g1_g2_g3_frame, text="Gadgets", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color, width=318, height=361)
		#self.gadget_frame.pack_propagate(False)
		self.gadget_frame.pack(side=LEFT, anchor=N, padx=2, pady=2)
		
		self.gadget1_frame = Frame(self.gadget_frame, borderwidth=0, bg=self.main_theme, width=106, height=300)
		#self.gadget1_frame.pack_propagate(False)
		self.gadget1_frame.pack(side=LEFT, anchor=N)

		self.gadget2_frame = Frame(self.gadget_frame, borderwidth=0, bg=self.main_theme, width=106, height=300)
		#self.gadget2_frame.pack_propagate(False)
		self.gadget2_frame.pack(side=LEFT, anchor=N)

		self.gadget3_frame = Frame(self.gadget_frame, borderwidth=0, bg=self.main_theme, width=106, height=300)
		#self.gadget3_frame.pack_propagate(False)
		self.gadget3_frame.pack(side=LEFT, anchor=N)
		
		self.frame_gadget_ref = [self.gadget1_frame, self.gadget2_frame, self.gadget3_frame]
		self.button_gadget_ref = [[None], [None], [None]]

		# --------------------------------------------------------------------------------------------------
		# MELEE BUTTON
		self.melee_frame = LabelFrame(self.secondary_melee_frame, text="Melee", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color, width=318, height=361)
		self.melee_frame.pack(side=TOP)

		melee_icon = PhotoImage(file="Icons/Melee/Melee 1.png")
		self.melee_button = Button(self.melee_frame, relief="raised", bg=self.main_button_color, image=melee_icon)
		self.melee_button['command'] = self.button_melee_clicked
		self.melee_button.image = melee_icon
		self.melee_button.pack(side=TOP)
		self.melee_weapon_selected = None

		# --------------------------------------------------------------------------------------------------
		# REINFORCEMENTS BUTTON
		self.reinforcements_frame = LabelFrame(self.country_vehicule_frame, text="Squad Call", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color)
		self.reinforcements_frame.pack(side=LEFT, anchor=N, padx=(5,0), pady=5)
		self.button_reinforcement_ref = []
		self.reinforcements_selected = set()

		# --------------------------------------------------------------------------------------------------
		# VEHICULES BUTTON
		self.vehicules_frame = LabelFrame(self.country_vehicule_frame, text="Vehicules", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color)
		self.vehicules_frame.pack(side=LEFT, anchor=N, padx=(5,0), pady=5)
		
		self.button_vehicules_ref = []
		self.vehicule_selected = set()

		# --------------------------------------------------------------------------------------------------
		# MAP SELECTOR
		self.map_button_ref = []
		self.map_frame = LabelFrame(self.main_frame, text="Map", font=self.main_font, labelanchor="n", borderwidth=2, bg=self.main_theme, fg=self.text_color)
		self.map_frame.pack(side=LEFT, anchor=N, padx=(0,0), fill=Y)
		self.loadMapButton()

		# --------------------------------------------------------------------------------------------------
		# STATIC WEAPON & PICKUP
		self.static_weapon_frame = LabelFrame(self.country_vehicule_frame, text="Other", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color)
		self.static_weapon_frame.pack(side=LEFT, anchor=N, padx=(5,5), pady=5)
		self.button_static_ref = []
		self.static_weapon_selected = set()
		self.loadStaticWeaponButton()

		# --------------------------------------------------------------------------------------------------
		# ADDITIONAL TAG BUTTON
		self.tag_set = set()

		self.tag_frame = LabelFrame(self.grade_kill_tag_frame, text="Additional Tags", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color)
		self.tag_frame.pack(side=BOTTOM, padx=5, pady=5)

		self.tag_row1_frame = Frame(self.tag_frame, borderwidth=0, bg=self.main_theme)
		self.tag_row1_frame.pack(side=TOP)

		self.tag_row2_frame = Frame(self.tag_frame, borderwidth=0, bg=self.main_theme)
		self.tag_row2_frame.pack(side=TOP)

		self.tag_row3_frame = Frame(self.tag_frame, borderwidth=0, bg=self.main_theme)
		self.tag_row3_frame.pack(side=TOP)

		# FUN TAG BUTTON
		iconFUN = PhotoImage(file="Icons/Tags/Funny.png")
		self.fun_tag_button = Button(self.tag_row1_frame, text="Fun", relief="raised", bg=self.main_button_color, fg=self.text_color, image=iconFUN)
		self.fun_tag_button.image = iconFUN
		self.fun_tag_button['command'] = self.button_fun_clicked
		self.fun_tag_button.pack(side=LEFT)
		# WTF TAG BUTTON
		iconWTF = PhotoImage(file="Icons/Tags/Wtf.png")
		self.wtf_tag_button = Button(self.tag_row1_frame, text="WTF", relief="raised", bg=self.main_button_color, fg=self.text_color, image=iconWTF)
		self.wtf_tag_button.image = iconWTF
		self.wtf_tag_button['command'] = self.button_wtf_clicked
		self.wtf_tag_button.pack(side=LEFT)
		# MONSTERKILL TAG BUTTON
		iconMONSTERKILL = PhotoImage(file="Icons/Tags/Monsterkill.png")
		self.monsterkill_tag_button = Button(self.tag_row1_frame, text="Monsterkill", relief="raised", bg=self.main_button_color, fg=self.text_color, image=iconMONSTERKILL)
		self.monsterkill_tag_button.image = iconMONSTERKILL
		self.monsterkill_tag_button['command'] = self.button_monsterkill_clicked
		self.monsterkill_tag_button.pack(side=LEFT)
		# LUCKY TAG BUTTON
		iconLUCKY = PhotoImage(file="Icons/Tags/Lucky.png")
		self.lucky_tag_button = Button(self.tag_row1_frame, text="Lucky", relief="raised", bg=self.main_button_color, fg=self.text_color, image=iconLUCKY)
		self.lucky_tag_button.image = iconLUCKY
		self.lucky_tag_button['command'] = self.button_lucky_clicked
		self.lucky_tag_button.pack(side=LEFT)
		# ROADKILL TAG BUTTON
		iconROADKILL = PhotoImage(file="Icons/Tags/Roadkill.png")
		self.roadkill_tag_button = Button(self.tag_row1_frame, text="Roadkill", relief="raised", bg=self.main_button_color, fg=self.text_color, image=iconROADKILL)
		self.roadkill_tag_button.image = iconROADKILL
		self.roadkill_tag_button['command'] = self.button_roadkill_clicked
		self.roadkill_tag_button.pack(side=LEFT)
		# TAG ROW 2

		# BUG TAG BUTTON
		iconBUG = PhotoImage(file="Icons/Tags/Bug.png")
		self.bug_tag_button = Button(self.tag_row2_frame, text="Bug", relief="raised", bg=self.main_button_color, fg=self.text_color, image=iconBUG)
		self.bug_tag_button.image = iconBUG
		self.bug_tag_button['command'] = self.button_bug_clicked
		self.bug_tag_button.pack(side=LEFT)
		# FRAGMOVIE TAG BUTTON
		iconFRAGMOVIE = PhotoImage(file="Icons/Tags/Fragmovie.png")
		self.fragmovie_tag_button = Button(self.tag_row2_frame, text="Fragmovie", relief="raised", bg=self.main_button_color, fg=self.text_color, image=iconFRAGMOVIE)
		self.fragmovie_tag_button.image = iconFRAGMOVIE
		self.fragmovie_tag_button['command'] = self.button_fragmovie_clicked
		self.fragmovie_tag_button.pack(side=LEFT)
		# INSANE TAG BUTTON
		iconINSANE = PhotoImage(file="Icons/Tags/Insane.png")
		self.insane_tag_button = Button(self.tag_row2_frame, text="Insane", relief="raised", bg=self.main_button_color, fg=self.text_color, image=iconINSANE)
		self.insane_tag_button.image = iconINSANE
		self.insane_tag_button['command'] = self.button_insane_clicked
		self.insane_tag_button.pack(side=LEFT)
		# UNLUCKY TAG BUTTON
		iconUNLUCKY = PhotoImage(file="Icons/Tags/Unlucky.png")
		self.unlucky_tag_button = Button(self.tag_row2_frame, text="Unlucky", relief="raised", bg=self.main_button_color, fg=self.text_color, image=iconUNLUCKY)
		self.unlucky_tag_button.image = iconUNLUCKY
		self.unlucky_tag_button['command'] = self.button_unlucky_clicked
		self.unlucky_tag_button.pack(side=LEFT)
		# ONE DEAG TAG BUTTON
		iconONEDEAG = PhotoImage(file="Icons/Tags/One Deag.png")
		self.one_deag_tag_button = Button(self.tag_row2_frame, text="One Deag", relief="raised", bg=self.main_button_color, fg=self.text_color, image=iconONEDEAG)
		self.one_deag_tag_button.image = iconONEDEAG
		self.one_deag_tag_button['command'] = self.button_one_deag_clicked
		self.one_deag_tag_button.pack(side=LEFT)

		self.tag_button_ref = [self.fun_tag_button, self.wtf_tag_button, self.monsterkill_tag_button, self.lucky_tag_button, self.roadkill_tag_button, self.bug_tag_button, self.fragmovie_tag_button, self.insane_tag_button, self.unlucky_tag_button, self.one_deag_tag_button]

		# --------------------------------------------------------------------------------------------------
		# loading infantry data from file
		self.return_code, self.infantry_data = self.loadData("Data/Infantry.json")
		if(self.return_code == -1):
			self.showError("Error loading infantry data file !", self.infantry_data)
			self.root.destroy()

		# --------------------------------------------------------------------------------------------------
		# loading user config when window is done created
		self.last_opened_clip = ""
		self.loadUserConfig()
		self.loadClipDataBase()
		self.clip_name_list = None
		self.clip_name_list = self.getClipList()
		self.findLastOpenedClip()
		if(self.clip_name_list != None):
			self.clip_label['text'] = self.clip_name_list[self.current_clip_index]

		# --------------------------------------------------------------------------------------------------
		# LOAD SCROLL LIST CLIP NAME
		self.clip_scroll_list['value'] = self.getClipListAlt()
		self.loadCurrentClipData()




	####################################################################################################
	####################################################################################################
	####################################################################################################
	####################################################################################################




	def ClipSorter(self):
		self.destroyMenu()
		self.root.title("Clip Finder")
		self.root.minsize(959, 805)
		self.root.resizable(True,True)
		self.main_theme = "grey35"
		self.main_theme_darker = "grey30"
		self.text_color = "white"
		self.main_button_color = "grey45"
		self.selected_button_color = "DarkOrange2"
		self.critical_button_color = "firebrick2"
		self.safe_button_color = "green3"
		self.main_font = tkFont.Font(size=11, weight="bold")
		self.root['bg'] = self.main_theme
		self.root.protocol("WM_DELETE_WINDOW", self.on_root_closing2)

		# --------------------------------------------------------------------------------------------------
		# MENU BAR
		self.menubar = Menu(self.root, bg=self.main_theme, fg=self.text_color, activebackground="white", activeforeground='black')
		self.file = Menu(self.menubar, tearoff=0, bg=self.main_theme, fg=self.text_color, font=self.main_font)
		self.file.add_command(label="Help", command=self.INFO)
		self.file.add_command(label="Preferences", command=self.openPreferencesWindow)
		self.file.add_command(label="Scan Clip Folder", command=self.scanClipFolder)
		self.file.add_separator()
		self.file.add_command(label="Clip Analyzer", command=self.loadClipAnalyser)
		self.file.add_command(label="Main Menu", command=self.loadMenu)
		self.menubar.add_cascade(label="File", menu=self.file)
		self.root.config(menu=self.menubar)

		# --------------------------------------------------------------------------------------------------
		# MAIN CLIP DATA BASE
		self.main_data_base = dict()

		# --------------------------------------------------------------------------------------------------
		# USER CONFIG & VARIABLES
		self.write_last_clip = False
		self.clip_data_base_file_path = ""
		self.clip_video_folder_path = ""
		self.user_config_file_path = ""

		self.country_selected = None
		self.clip_grade_selected = None
		self.kill_counter = 0

		self.class_selected = None

		self.primary_weapon_selected = None
		self.secondary_weapon_selected = None
		self.melee_weapon_selected = None

		self.gadget1_selected = None
		self.gadget2_selected = None
		self.gadget3_selected = None

		self.reinforcements_selected = set()
		self.vehicule_selected = set()
		self.static_weapon_selected = set()

		self.map_selected = None

		self.tag_set = set()

		# --------------------------------------------------------------------------------------------------
		# INITIAL LOADING
		self.loadUserConfig()
		self.loadClipDataBase()

		# --------------------------------------------------------------------------------------------------
		# MAIN FRAME
		self.main_frame = Frame(self.root, borderwidth=0, bg=self.main_theme)
		self.main_frame.pack(fill=BOTH, expand=True)

		# --------------------------------------------------------------------------------------------------
		# FILTER FRAME
		self.filter_frame = LabelFrame(self.main_frame, text="Filters", font=self.main_font, labelanchor="n", borderwidth=2, bg=self.main_theme, fg=self.text_color)
		self.filter_frame.pack(side=LEFT, anchor=N)

		# --------------------------------------------------------------------------------------------------
		# RESULT & BUTTON FRAME
		self.result_button_frame = Frame(self.main_frame, borderwidth=0, bg=self.main_theme)
		self.result_button_frame.pack(side=LEFT, fill=BOTH, expand=True)

		# --------------------------------------------------------------------------------------------------
		# RESULT FRAME
		self.result_frame = LabelFrame(self.result_button_frame, text="Results", font=self.main_font, labelanchor="n", borderwidth=2, bg=self.main_theme, fg=self.text_color)
		self.result_frame.pack(side=TOP, fill=BOTH, expand=True)



		# --------------------------------------------------------------------------------------------------
		# RESULTS LISTBOX & SCROLL BAR
		
		
		self.canvas = Canvas(self.result_frame, bg=self.main_theme)
		
		self.scrollbar = Scrollbar(self.result_frame, orient=VERTICAL, command=self.canvas.yview)
		self.scroll_frame = Frame(self.canvas, bg=self.main_theme)
		self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
		self.scroll_frame.bind('<Enter>', self._bound_to_mousewheel)
		self.scroll_frame.bind('<Leave>', self._unbound_to_mousewheel)
		#self.scroll_frame.pack(fill=BOTH, expand=True)
		self.canvas.create_window(0, 0, anchor=NW, window=self.scroll_frame)
		self.canvas.configure(yscrollcommand=self.scrollbar.set)

		self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
		self.scrollbar.pack(side=RIGHT, fill=Y)
		# used to store 3 elements list for each clip matching [clip name, checkButton variable, frame containing checkButton and label reference]
		self.resultList = []


		self.select_button_frame = LabelFrame(self.result_button_frame, bg=self.main_theme, bd=2)
		self.select_button_frame.pack(side=TOP, fill=X)

		self.select_all_button = Button(self.select_button_frame, text="Select All", font=self.main_font, bg=self.main_button_color, fg=self.text_color, command=self.select_all_button_clicked)
		self.select_all_button.pack(side=LEFT, padx=5, pady=5)

		self.deselect_all_button = Button(self.select_button_frame, text="Deselect All", font=self.main_font, bg=self.main_button_color, fg=self.text_color, command=self.deselect_all_button_clicked)
		self.deselect_all_button.pack(side=LEFT, padx=5, pady=5)

		self.copy_selected_button = Button(self.select_button_frame, text="Copy to folder", font=self.main_font, bg=self.main_button_color, fg=self.text_color, command=self.export_copy_selected_button_clicked)
		self.copy_selected_button.pack(side=RIGHT, padx=5, pady=5)

		self.txt_selected_button = Button(self.select_button_frame, text="Export clip name", font=self.main_font, bg=self.main_button_color, fg=self.text_color, command=self.export_txt_selected_button_clicked)
		self.txt_selected_button.pack(side=RIGHT, padx=5, pady=5)
		


		# --------------------------------------------------------------------------------------------------
		# KILL MIN MAX FRAME
		self.min_max_frame = LabelFrame(self.filter_frame, text="Kills", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color)
		self.min_max_frame.pack(fill=X, padx=5, pady=5)

		# --------------------------------------------------------------------------------------------------
		# MIN KILL COUNTER
		self.kill_counter_frame1 = LabelFrame(self.min_max_frame, text="Min", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color)
		self.kill_counter_frame1.pack(side=LEFT, padx=(5, 2), pady=(0,5))

		self.mouse_over_kill_counter1 = False
		self.kill_counter1 = -1
		# minus button
		button_font = tkFont.Font(size=16, weight="bold")
		iconVIRTUAL = PhotoImage(width=1, height=1)
		self.buttonMINUS1 = Button(self.kill_counter_frame1, text="-", fg="white", font=button_font, relief="raised", bg=self.main_button_color, width=3, height=1)
		self.buttonMINUS1['command'] = self.buttonMINUS_clicked1
		self.buttonMINUS1.pack(side=LEFT)
		# kill count button
		button_font = tkFont.Font(size=18, weight="bold")
		self.buttonKILLCOUNTER1 = Button(self.kill_counter_frame1, text="X", fg="white",relief="raised", font=button_font, bg=self.main_button_color, width=3, height=1)
		self.buttonKILLCOUNTER1['command'] = self.buttonKILLCOUNTER_clicked1
		self.buttonKILLCOUNTER1.bind("<Enter>", self._on_enter_kill_counter1)
		self.buttonKILLCOUNTER1.bind("<Leave>", self._on_leave_kill_counter1)
		self.buttonKILLCOUNTER1.bind("<MouseWheel>", self._on_mousewheel1)
		self.buttonKILLCOUNTER1.pack(side=LEFT)
		# plus button
		button_font = tkFont.Font(size=16, weight="bold")
		iconVIRTUAL = PhotoImage(width=1, height=1)
		self.buttonPLUS1 = Button(self.kill_counter_frame1, text="+", fg="white", font=button_font, relief="raised", bg=self.main_button_color, width=3, height=1)
		self.buttonPLUS1['command'] = self.buttonPLUS_clicked1
		self.buttonPLUS1.pack(side=LEFT)

		# --------------------------------------------------------------------------------------------------
		# MAX KILL COUNTER
		self.kill_counter_frame2 = LabelFrame(self.min_max_frame, text="Max", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color)
		self.kill_counter_frame2.pack(side=RIGHT, padx=(2,5), pady=(0,5))

		self.mouse_over_kill_counter2 = False
		self.kill_counter2 = -1
		# minus button
		button_font = tkFont.Font(size=16, weight="bold")
		iconVIRTUAL = PhotoImage(width=1, height=1)
		self.buttonMINUS2 = Button(self.kill_counter_frame2, text="-", fg="white", font=button_font, relief="raised", bg=self.main_button_color, width=3, height=1)
		self.buttonMINUS2['command'] = self.buttonMINUS_clicked2
		self.buttonMINUS2.pack(side=LEFT)
		# kill count button
		button_font = tkFont.Font(size=18, weight="bold")
		self.buttonKILLCOUNTER2 = Button(self.kill_counter_frame2, text="X", fg="white",relief="raised", font=button_font, bg=self.main_button_color, width=3, height=1)
		self.buttonKILLCOUNTER2['command'] = self.buttonKILLCOUNTER_clicked2
		self.buttonKILLCOUNTER2.bind("<Enter>", self._on_enter_kill_counter2)
		self.buttonKILLCOUNTER2.bind("<Leave>", self._on_leave_kill_counter2)
		self.buttonKILLCOUNTER2.bind("<MouseWheel>", self._on_mousewheel2)
		self.buttonKILLCOUNTER2.pack(side=LEFT)
		# plus button
		button_font = tkFont.Font(size=16, weight="bold")
		iconVIRTUAL = PhotoImage(width=1, height=1)
		self.buttonPLUS2 = Button(self.kill_counter_frame2, text="+", fg="white", font=button_font, relief="raised", bg=self.main_button_color, width=3, height=1)
		self.buttonPLUS2['command'] = self.buttonPLUS_clicked2
		self.buttonPLUS2.pack(side=LEFT)


		# GRADE BUTTON
		self.grade_frame = LabelFrame(self.filter_frame, text="Grade clip", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color)
		self.grade_frame.pack(side=TOP, padx=5, pady=5)

		self.button_star_pressed = [False,False,False,False,False]
		self.clip_grade_selected = None

		# star button 1
		iconSTAR = PhotoImage(file="Icons/Misc/Star.png")
		self.buttonSTAR1 = Button(self.grade_frame, relief="raised", bg=self.main_button_color, image=iconSTAR)
		self.buttonSTAR1.image = iconSTAR
		self.buttonSTAR1['command'] = self.buttonSTAR1_clicked
		self.buttonSTAR1.pack(side=LEFT)
		# star button 2
		self.buttonSTAR2 = Button(self.grade_frame, relief="raised", bg=self.main_button_color, image=iconSTAR)
		self.buttonSTAR2.image = iconSTAR
		self.buttonSTAR2['command'] = self.buttonSTAR2_clicked
		self.buttonSTAR2.pack(side=LEFT)
		# star button 3
		self.buttonSTAR3 = Button(self.grade_frame, relief="raised", bg=self.main_button_color, image=iconSTAR)
		self.buttonSTAR3.image = iconSTAR
		self.buttonSTAR3['command'] = self.buttonSTAR3_clicked
		self.buttonSTAR3.pack(side=LEFT)
		# star button 4
		self.buttonSTAR4 = Button(self.grade_frame, relief="raised", bg=self.main_button_color, image=iconSTAR)
		self.buttonSTAR4.image = iconSTAR
		self.buttonSTAR4['command'] = self.buttonSTAR4_clicked
		self.buttonSTAR4.pack(side=LEFT)
		# star button 5
		self.buttonSTAR5 = Button(self.grade_frame, relief="raised", bg=self.main_button_color, image=iconSTAR)
		self.buttonSTAR5.image = iconSTAR
		self.buttonSTAR5['command'] = self.buttonSTAR5_clicked
		self.buttonSTAR5.pack(side=LEFT)

		self.button_STAR_ref = [self.buttonSTAR1, self.buttonSTAR2, self.buttonSTAR3, self.buttonSTAR4, self.buttonSTAR5]


		# MELEE BUTTON
		self.melee_frame = LabelFrame(self.filter_frame, text="Melee", font=self.main_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg=self.text_color, width=318, height=361)
		self.melee_frame.pack(side=TOP)
		melee_icon = PhotoImage(file="Icons/Melee/Melee 1.png")
		self.melee_button = Button(self.melee_frame, relief="raised", bg=self.main_button_color, image=melee_icon)
		self.melee_button['command'] = self.button_melee_clicked
		self.melee_button.image = melee_icon
		self.melee_button.pack(side=TOP)


		# NATION FILTER FRAME & LABEL & SCROLL LIST
		self.nation_frame = Frame(self.filter_frame, borderwidth=0, bg=self.main_theme)
		self.nation_frame.pack(side=TOP, padx=5, pady=5)

		self.nation_label = Label(self.nation_frame, text="Nation", font=self.main_font, bg=self.main_theme, fg=self.text_color, anchor=N, width=16)
		self.nation_label.pack(side=LEFT, fill=X, padx=2, pady=2)

		self.nation_scroll_list = checklistcombobox.ChecklistCombobox(self.nation_frame, checkbutton_height=2, width=25, height=40, justify=LEFT, state="readonly")
		self.nation_scroll_list.pack(side=LEFT, padx=5, pady=5)

		# MAP FILTER FRAME & LABEL & SCROLL LIST
		self.map_frame = Frame(self.filter_frame, borderwidth=0, bg=self.main_theme)
		self.map_frame.pack(side=TOP, padx=5, pady=5)

		self.map_label = Label(self.map_frame, text="Map", font=self.main_font, bg=self.main_theme, fg=self.text_color, anchor=N, width=16)
		self.map_label.pack(side=LEFT, fill=X, padx=2, pady=2)

		self.map_scroll_list = checklistcombobox.ChecklistCombobox(self.map_frame, checkbutton_height=2, width=25, height=40, justify=LEFT, state="readonly")
		self.map_scroll_list.pack(side=LEFT, padx=5, pady=5)


		# CLASS FILTER FRAME & LABEL & SCROLL LIST
		self.class_frame = Frame(self.filter_frame, borderwidth=0, bg=self.main_theme)
		self.class_frame.pack(side=TOP, padx=5, pady=5)

		self.class_label = Label(self.class_frame, text="Class", font=self.main_font, bg=self.main_theme, fg=self.text_color, anchor=N, width=16)
		self.class_label.pack(side=LEFT, fill=X, padx=2, pady=2)

		self.class_scroll_list = checklistcombobox.ChecklistCombobox(self.class_frame, checkbutton_height=2, width=25, height=40, justify=LEFT, state="readonly")
		self.class_scroll_list.pack(side=LEFT, padx=5, pady=5)

		
		# PRIMARY WEAPON FILTER FRAME & LABEL & SCROLL LIST
		self.w1_frame = Frame(self.filter_frame, borderwidth=0, bg=self.main_theme)
		self.w1_frame.pack(side=TOP, padx=5, pady=5)

		self.w1_label = Label(self.w1_frame, text="Primary Weapon", font=self.main_font, bg=self.main_theme, fg=self.text_color, anchor=N, width=16)
		self.w1_label.pack(side=LEFT, fill=X, padx=2, pady=2)

		self.w1_scroll_list = checklistcombobox.ChecklistCombobox(self.w1_frame, checkbutton_height=2, width=25, height=40, justify=LEFT, state="readonly")
		self.w1_scroll_list.pack(side=LEFT, padx=5, pady=5)


		# SECONDARY WEAPON FILTER FRAME & LABEL & SCROLL LIST
		self.w2_frame = Frame(self.filter_frame, borderwidth=0, bg=self.main_theme)
		self.w2_frame.pack(side=TOP, padx=5, pady=5)

		self.w2_label = Label(self.w2_frame, text="Secondary Weapon", font=self.main_font, bg=self.main_theme, fg=self.text_color, anchor=N, width=16)
		self.w2_label.pack(side=LEFT, fill=X, padx=2, pady=2)

		self.w2_scroll_list = checklistcombobox.ChecklistCombobox(self.w2_frame, checkbutton_height=2, width=25, height=40, justify=LEFT, state="readonly")
		self.w2_scroll_list.pack(side=LEFT, padx=5, pady=5)


		# GADGET 1 FILTER FRAME & LABEL & SCROLL LIST
		self.g1_frame = Frame(self.filter_frame, borderwidth=0, bg=self.main_theme)
		self.g1_frame.pack(side=TOP, padx=5, pady=5)

		self.g1_label = Label(self.g1_frame, text="First Gadget", font=self.main_font, bg=self.main_theme, fg=self.text_color, anchor=N, width=16)
		self.g1_label.pack(side=LEFT, fill=X, padx=2, pady=2)

		self.g1_scroll_list = checklistcombobox.ChecklistCombobox(self.g1_frame, checkbutton_height=2, width=25, height=40, justify=LEFT, state="readonly")
		self.g1_scroll_list.pack(side=LEFT, padx=5, pady=5)


		# GADGET 2 FILTER FRAME & LABEL & SCROLL LIST
		self.g2_frame = Frame(self.filter_frame, borderwidth=0, bg=self.main_theme)
		self.g2_frame.pack(side=TOP, padx=5, pady=5)

		self.g2_label = Label(self.g2_frame, text="Second Gadget", font=self.main_font, bg=self.main_theme, fg=self.text_color, anchor=N, width=16)
		self.g2_label.pack(side=LEFT, fill=X, padx=2, pady=2)

		self.g2_scroll_list = checklistcombobox.ChecklistCombobox(self.g2_frame, checkbutton_height=2, width=25, height=40, justify=LEFT, state="readonly")
		self.g2_scroll_list.pack(side=LEFT, padx=5, pady=5)


		# GADGET 3 FILTER FRAME & LABEL & SCROLL LIST
		self.g3_frame = Frame(self.filter_frame, borderwidth=0, bg=self.main_theme)
		self.g3_frame.pack(side=TOP, padx=5, pady=5)

		self.g3_label = Label(self.g3_frame, text="Third Gadget", font=self.main_font, bg=self.main_theme, fg=self.text_color, anchor=N, width=16)
		self.g3_label.pack(side=LEFT, fill=X, padx=2, pady=2)

		self.g3_scroll_list = checklistcombobox.ChecklistCombobox(self.g3_frame, checkbutton_height=2, width=25, height=40, justify=LEFT, state="readonly")
		self.g3_scroll_list.pack(side=LEFT, padx=5, pady=5)


		# SQUAD CALL FILTER FRAME & LABEL & SCROLL LIST
		self.squad_call_frame = Frame(self.filter_frame, borderwidth=0, bg=self.main_theme)
		self.squad_call_frame.pack(side=TOP, padx=5, pady=5)

		self.squad_call_label = Label(self.squad_call_frame, text="Squad Call", font=self.main_font, bg=self.main_theme, fg=self.text_color, anchor=N, width=16)
		self.squad_call_label.pack(side=LEFT, fill=X, padx=2, pady=2)

		self.squad_call_scroll_list = checklistcombobox.ChecklistCombobox(self.squad_call_frame, checkbutton_height=2, width=25, height=40, justify=LEFT, state="readonly")
		self.squad_call_scroll_list.pack(side=LEFT, padx=5, pady=5)


		# VEHICULE FILTER FRAME & LABEL & SCROLL LIST
		self.vehicule_frame = Frame(self.filter_frame, borderwidth=0, bg=self.main_theme)
		self.vehicule_frame.pack(side=TOP, padx=5, pady=5)

		self.vehicule_label = Label(self.vehicule_frame, text="Vehicules", font=self.main_font, bg=self.main_theme, fg=self.text_color, anchor=N, width=16)
		self.vehicule_label.pack(side=LEFT, fill=X, padx=2, pady=2)

		self.vehicule_scroll_list = checklistcombobox.ChecklistCombobox(self.vehicule_frame, checkbutton_height=2, width=25, height=40, justify=LEFT, state="readonly")
		self.vehicule_scroll_list.pack(side=LEFT, padx=5, pady=5)


		# STATIC WEAPON FILTER FRAME & LABEL & SCROLL LIST
		self.static_weapon_frame = Frame(self.filter_frame, borderwidth=0, bg=self.main_theme)
		self.static_weapon_frame.pack(side=TOP, padx=5, pady=5)

		self.static_weapon_label = Label(self.static_weapon_frame, text="Static Weapon \n& Pickup", font=self.main_font, bg=self.main_theme, fg=self.text_color, anchor=N, width=16)
		self.static_weapon_label.pack(side=LEFT, fill=X, padx=2, pady=2)

		self.static_weapon_scroll_list = checklistcombobox.ChecklistCombobox(self.static_weapon_frame, checkbutton_height=2, width=25, height=40, justify=LEFT, state="readonly")
		self.static_weapon_scroll_list.pack(side=LEFT, padx=5, pady=5)


		# TAG FILTER FRAME & LABEL & SCROLL LIST
		self.tags_frame = Frame(self.filter_frame, borderwidth=0, bg=self.main_theme)
		self.tags_frame.pack(side=TOP, padx=5, pady=5)

		self.tags_label = Label(self.tags_frame, text="Tag", font=self.main_font, bg=self.main_theme, fg=self.text_color, anchor=N, width=16)
		self.tags_label.pack(side=LEFT, fill=X, padx=2, pady=2)

		self.tags_scroll_list = checklistcombobox.ChecklistCombobox(self.tags_frame, checkbutton_height=2, width=25, height=40, justify=LEFT, state="readonly")
		self.tags_scroll_list.pack(side=LEFT, padx=5, pady=5)

		self.apply_button = Button(self.filter_frame, text="Apply Filters", font=self.main_font, bg=self.main_button_color, fg=self.text_color, command=self.findClipMatching)
		self.apply_button.pack(side=TOP, padx=5, pady=5)

		self.loadCheckScrollList()


	def _bound_to_mousewheel(self, event):
		self.canvas.bind_all("<MouseWheel>", self._on_mousewheel3)   

	def _unbound_to_mousewheel(self, event):
		self.canvas.unbind_all("<MouseWheel>") 

	def _on_mousewheel3(self, event):
		self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


	def cleanResultList(self):
		for element in self.resultList:
			element[2].destroy()
		self.resultList.clear()


	def select_all_button_clicked(self):
		for e in self.resultList:
			e[1].set(True)

	def deselect_all_button_clicked(self):
		for e in self.resultList:
			e[1].set(False)


	def export_copy_selected_button_clicked(self):
		dst = filedialog.askdirectory()
		if(dst != ""):
			self.copy_selected_button['state'] = DISABLED
			for element in self.resultList:
				if(element[1].get()):
					src = self.clip_video_folder_path + "/" + element[0]
					shutil.copy(src, dst)
			self.showInfo("Success !", "Copied selected clip to folder\nFolder at :"+dst)
			self.copy_selected_button['state'] = NORMAL

	def export_txt_selected_button_clicked(self):
		dst = filedialog.askdirectory()
		now = datetime.now()
		filename = now.strftime("%d-%m-%Y %H-%M-%S")
		content = ""
		if(dst != ""):
			for element in self.resultList:
				if(element[1].get()):
					content += element[0] + "\n"

			f = open(dst+"/"+filename+".txt", "w")
			f.write(content)
			f.close()
			self.showInfo("Success !", "Copied selected clip name to text file\nFile at :"+dst)

					


	def loadCheckScrollList(self):
		# ---------------------------------------------------
		self.nation_scroll_list.config(values=["Germany", "United Kingdom", "Japan", "United States of America"])
		# ---------------------------------------------------
		code, map_data = self.loadData("Data/Maps.json")
		if(code != -1):
			map_list = self.getMapList(map_data)
			self.map_scroll_list.config(values=map_list)
		else:
			self.showError("Error", "Error while loading Map data from file !")
		# ---------------------------------------------------
		self.class_scroll_list.config(values=["Assault", "Medic", "Support", "Recon"])
		# ---------------------------------------------------
		code, w_data = self.loadData("Data/Infantry.json")
		if(code != -1):
			weapon1_list = w_data["ASSAULT"]["W1"] + w_data["MEDIC"]["W1"] + w_data["SUPPORT"]["W1"] + w_data["RECON"]["W1"]
			weapon1_list.sort()
			self.w1_scroll_list.config(values=weapon1_list)
			self.w1_scroll_list.config(height=20)
			# -------------------------
			weapon2_list = w_data["W2"]
			weapon2_list.sort()
			self.w2_scroll_list.config(values=weapon2_list)
			# -------------------------
			g1_list = list(set(w_data["ASSAULT"]["G1"] + w_data["MEDIC"]["G1"] + w_data["SUPPORT"]["G1"] + w_data["RECON"]["G1"]))
			g1_list.sort()
			self.g1_scroll_list.config(values=g1_list)
			# -------------------------
			g2_list = list(set(w_data["ASSAULT"]["G2"] + w_data["RECON"]["G2"]))
			g2_list.sort()
			self.g2_scroll_list.config(values=g2_list)
			# -------------------------
			g3_list = list(set(w_data["ASSAULT"]["G3"] + w_data["MEDIC"]["G3"] + w_data["SUPPORT"]["G3"] + w_data["RECON"]["G3"]))
			g3_list.sort()
			self.g3_scroll_list.config(values=g3_list)
			# -------------------------
			statics_list = w_data["STATIC WEAPONS & PICKUP"]
			statics_list.sort()
			self.static_weapon_scroll_list.config(values=statics_list)
		else:
			self.showError("Error", "Error while loading Weapon data from file !")

		# ---------------------------------------------------
		code, r_data = self.loadData("Data/Reinforcements.json")
		if(code != -1):
			sq_list = list(set(r_data["GE"] + r_data["UK"] + r_data["USA"] + r_data["JP"]))
			sq_list.sort()
			self.squad_call_scroll_list.config(values=sq_list)
		else:
			self.showError("Error", "Error while loading Reinforcements data from file !")

		# ---------------------------------------------------
		code, v_data = self.loadData("Data/Vehicules.json")
		if(code != -1):
			v_list = list(set(
				v_data["GE"]["TANKS"]["LIGHT"] +
				v_data["GE"]["TANKS"]["MEDIUM"] +
				v_data["GE"]["TANKS"]["HEAVY"] +
				v_data["GE"]["PLANES"]["LIGHT"] +
				v_data["GE"]["PLANES"]["HEAVY"] +
				v_data["UK"]["TANKS"]["LIGHT"] +
				v_data["UK"]["TANKS"]["MEDIUM"] +
				v_data["UK"]["TANKS"]["HEAVY"] +
				v_data["UK"]["PLANES"]["LIGHT"] +
				v_data["UK"]["PLANES"]["HEAVY"] +
				v_data["USA"]["TANKS"]["LIGHT"] +
				v_data["USA"]["TANKS"]["MEDIUM"] +
				v_data["USA"]["TANKS"]["HEAVY"] +
				v_data["USA"]["PLANES"]["LIGHT"] +
				v_data["USA"]["PLANES"]["HEAVY"] +
				v_data["JP"]["TANKS"]["LIGHT"] +
				v_data["JP"]["TANKS"]["MEDIUM"] +
				v_data["JP"]["TANKS"]["HEAVY"] +
				v_data["JP"]["PLANES"]["LIGHT"] +
				v_data["JP"]["BOATS"]))
			v_list.sort()
			self.vehicule_scroll_list.config(values=v_list)
			self.vehicule_scroll_list.config(height=20)
		else:
			self.showError("Error", "Error while loading Reinforcements data from file !")

		# ---------------------------------------------------
		tags_list = ["Unlucky","Insane","Lucky","Monsterkill","One Deag","WTF","Fragmovie","Bug","Roadkill","Fun"]
		tags_list.sort()
		self.tags_scroll_list.config(values=tags_list)


	def humanToKey(self, country_list):
		key_list = []
		if(type(country_list) == list):
			for country in country_list:
				if(country == "Germany"):
					key_list.append("GE")
				elif(country == "United Kingdom"):
					key_list.append("UK")
				elif(country == "Japan"):
					key_list.append("JP")
				elif(country == "United States of America"):
					key_list.append("USA")
				else:
					continue
		else:
			if(country_list == "Germany"):
				key_list.append("GE")
			elif(country_list == "United Kingdom"):
				key_list.append("UK")
			elif(country_list == "Japan"):
				key_list.append("JP")
			elif(country_list == "United States of America"):
				key_list.append("USA")
		if(len(key_list) != 0):
			return key_list
		return ""


	def retriveFilters(self):
		self.country_selected = self.humanToKey(self.nation_scroll_list.get())
		self.map_selected = self.map_scroll_list.get()
		self.class_selected = self.class_scroll_list.get()
		self.primary_weapon_selected = self.w1_scroll_list.get()
		self.secondary_weapon_selected = self.w2_scroll_list.get()
		self.gadget1_selected = self.g1_scroll_list.get()
		self.gadget2_selected = self.g2_scroll_list.get()
		self.gadget3_selected = self.g3_scroll_list.get()
		self.reinforcements_selected = self.squad_call_scroll_list.get()
		self.vehicule_selected = self.vehicule_scroll_list.get()
		self.static_weapon_selected = self.static_weapon_scroll_list.get()
		self.tag_set = self.tags_scroll_list.get()

		filters = dict()

		if(self.clip_grade_selected != None):
			filters["GRADE"] = self.clip_grade_selected

		if(self.kill_counter1 != -1 or self.kill_counter2 != -1):
			filters["KILL"] = [self.kill_counter1,self.kill_counter2]

		if((type(self.class_selected) == list and len(self.class_selected)) or (self.class_selected != "")):
			filters["CLASS"] = self.class_selected

		if((type(self.primary_weapon_selected) == list and len(self.primary_weapon_selected)) or (self.primary_weapon_selected != "")):
			filters["W1"] = self.primary_weapon_selected

		if((type(self.secondary_weapon_selected) == list and len(self.secondary_weapon_selected)) or (self.secondary_weapon_selected != "")):
			filters["W2"] = self.secondary_weapon_selected

		if((type(self.gadget1_selected) == list and len(self.gadget1_selected)) or (self.gadget1_selected != "")):
			filters["G1"] = self.gadget1_selected

		if((type(self.gadget2_selected) == list and len(self.gadget2_selected)) or (self.gadget2_selected != "")):
			filters["G2"] = self.gadget2_selected

		if((type(self.gadget3_selected) == list and len(self.gadget3_selected)) or (self.gadget3_selected != "")):
			filters["G3"] = self.gadget3_selected

		if(self.melee_weapon_selected != None):
			filters["MELEE"] = self.melee_weapon_selected

		if((type(self.map_selected) == list and len(self.map_selected)) or (self.map_selected != "")):
			filters["MAP"] = self.map_selected

		if((type(self.country_selected) == list and len(self.country_selected)) or (self.country_selected != "")):
			filters["COUNTRY"] = self.country_selected

		if((type(self.vehicule_selected) == list and len(self.vehicule_selected)) or (self.vehicule_selected != "")):
			filters["VEHICULE"] = self.vehicule_selected

		if((type(self.reinforcements_selected) == list and len(self.reinforcements_selected)) or (self.reinforcements_selected != "")):
			filters["SR"] = self.reinforcements_selected

		if((type(self.static_weapon_selected) == list and len(self.static_weapon_selected)) or (self.static_weapon_selected != "")):
			filters["STATIC"] = self.static_weapon_selected

		if((type(self.tag_set) == list and len(self.tag_set)) or (self.tag_set != "")):
			filters["TAGS"] = self.tag_set

		return filters
	

	def findClipMatching(self):
		filters = self.retriveFilters()
		self.cleanResultList()
		match = dict()
		for clip in self.main_data_base:
			tt = 0
			for key in filters.keys():
				res = self.matchClipFilter(key, filters[key], self.main_data_base[clip])
				if(res):
					tt += 1
			if(tt == len(filters.keys())):
				match[clip] = self.main_data_base[clip]
		self.displayMatch(match)


	def matchClipFilter(self, key, filter_, clip_data):
		if(type(filter_) == list):
			if(clip_data[key] != None):
				if(key == "KILL"):
					if(clip_data[key] >= filter_[0] and clip_data[key] <= filter_[1]):
						return True
				else:
					if(type(clip_data[key]) == list):
						for element in filter_:
							if(element in clip_data[key]):
								return True
					else:
						for element in filter_:
							if(element == clip_data[key]):
								return True			
		else:
			if(clip_data[key] != None):
				if(type(clip_data[key]) == list):
					if(filter_ in clip_data[key]):
						return True
				else:
					if(filter_ == clip_data[key]):
						return True
		return False


	def prettifyClipData(self, clip_data):
		res = dict()
		for key in clip_data.keys():
			if(clip_data[key] != None and clip_data[key] != []):
				res[key] = clip_data[key]
		return res


	def displayMatch(self, match_dict):
		nb_results = len(list(match_dict.keys()))
		if(nb_results < 2):
			self.result_frame['text'] = str(nb_results) + " Result"
		else:
			self.result_frame['text'] = str(nb_results) + " Results"	

		for clip in match_dict.keys():
			pretty_clip = self.prettifyClipData(match_dict[clip])
			label_text = ""
			for key in pretty_clip.keys():
				if(key == "GRADE"):
					label_text += str(pretty_clip[key])+"/5, "
				elif(key == "KILL"):
					if(pretty_clip[key] > 1):
						label_text += str(pretty_clip[key])+" Kills, "
					else:
						label_text += str(pretty_clip[key])+" Kill, "
				elif(key == "MAP"):
					label_text += pretty_clip[key]+", "
				elif(key == "CLASS"):
					label_text += pretty_clip[key]+", "
				elif(key == "W1"):
					label_text += pretty_clip[key]+", "
				elif(key == "W2"):
					label_text += pretty_clip[key]+", "
				elif(key == "G1"):
					label_text += pretty_clip[key]+", "
				elif(key == "G2"):
					label_text += pretty_clip[key]+", "
				elif(key == "G3"):
					label_text += pretty_clip[key]+", "
				elif(key == "MELEE"):
					label_text += pretty_clip[key]+", "
				elif(key == "NATION"):
					label_text += pretty_clip[key]+", "
				elif(key == "VEHICULE"):
					if(type(pretty_clip[key]) == list):
						label_text += ", ".join(pretty_clip[key])+", "
					else:
						label_text += pretty_clip[key]+", "
				elif(key == "SR"):
					if(type(pretty_clip[key]) == list):
						label_text += ", ".join(pretty_clip[key])+", "
					else:
						label_text += pretty_clip[key]+", "
				elif(key == "STATIC"):
					if(type(pretty_clip[key]) == list):
						label_text += ", ".join(pretty_clip[key])+", "
					else:
						label_text += pretty_clip[key]+", "
				elif(key == "TAGS"):
					if(type(pretty_clip[key]) == list):
						label_text += ", ".join(pretty_clip[key])+", "
					else:
						label_text += pretty_clip[key]+", "
			f = LabelFrame(self.scroll_frame, bd=2, bg=self.main_theme, fg=self.text_color)
			f.pack(side=TOP, anchor=W)
			checkVar = BooleanVar()
			check = Checkbutton(f, bg=self.main_theme, variable = checkVar, onvalue = True, offvalue = False, height=1, width = 1)
			check.pack(side=LEFT)
			lc = Label(f, text=clip, height=1, font=self.main_font, bd=2, bg=self.main_theme_darker, fg=self.text_color, anchor=W)
			lc.pack(side=LEFT, anchor=W, fill=BOTH, expand=True,  padx=0, pady=0)
			ld = Label(f, text=label_text[:-2], height=1, font=self.main_font, bd=2, bg=self.main_theme, fg=self.text_color, anchor=W)
			ld.pack(side=LEFT, anchor=W, fill=BOTH, expand=True,  padx=0, pady=0)

			self.resultList.append([clip, checkVar, f])





	####################################################################################################
	####################################################################################################
	####################################################################################################
	####################################################################################################
	# --------------------------------------------------------------------------------------------------
	# PREFERENCE WINDOW
	def openPreferencesWindow(self):
		self.sub_win = Toplevel(self.root)
		self.sub_win.resizable(False, False)
		self.sub_win.grab_set()
		# main sub window frame
		frame_font = tkFont.Font(size=13, weight="bold")
		self.main_preference_frame = LabelFrame(self.sub_win, text="Set your preferences", font=frame_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg="white")
		self.main_preference_frame.pack(side=TOP)
		# clip folder frame
		self.clip_folder_frame = LabelFrame(self.main_preference_frame, text="Select clip folder", borderwidth=0, bg=self.main_theme, fg="white")
		self.clip_folder_frame.pack(side=TOP, padx=10, pady=10)
		# clip data folder frame
		self.clip_data_folder_frame = LabelFrame(self.main_preference_frame, text="Select folder location to save clip data base", borderwidth=0, bg=self.main_theme, fg="white")
		self.clip_data_folder_frame.pack(side=TOP, padx=10, pady=10)
		# validation button frame
		self.validation_frame = Frame(self.main_preference_frame, borderwidth=0, bg=self.main_theme)
		self.validation_frame.pack(side=TOP, padx=10, pady=10)

		# clip folder path label
		self.clip_folder_path_label = Label(self.clip_folder_frame, text=self.clip_video_folder_path, width=50, height=1, bg="lightgrey", anchor=W)
		self.clip_folder_path_label.pack(side=LEFT, fill=X, padx=2, pady=2)
		# browse button
		self.browse_button1 = Button(self.clip_folder_frame, text="Browse Folder", relief="raised", bg=self.main_button_color, fg="white")
		self.browse_button1['command'] = self.openClipFolderDialog
		self.browse_button1.pack(side=LEFT)

		# clip data base folder path label
		self.clip_data_path_label = Label(self.clip_data_folder_frame, text=self.clip_data_base_file_path, width=50, height=1, bg="lightgrey", anchor=W)
		self.clip_data_path_label.pack(side=LEFT, fill=X, padx=2, pady=2)
		# browse button
		self.browse_button2 = Button(self.clip_data_folder_frame, text="Browse Folder", relief="raised", bg=self.main_button_color, fg="white")
		self.browse_button2['command'] = self.openDataFolderDialog
		self.browse_button2.pack(side=LEFT)

		# validation button
		self.validate_button = Button(self.validation_frame, text="Save and Exit", relief="raised", bg=self.main_button_color, fg="white")
		self.validate_button['command'] = lambda window=self.sub_win:self.saveAndExitPreferences(window)
		self.validate_button.pack(side=TOP)



				
	# --------------------------------------------------------------------------------------------------
	# KILL COUNTER MOUSE EVENT BINDS & OTHER MOUSE BIND

	def _on_enter_kill_counter(self, enter):
		self.mouse_over_kill_counter = True

	def _on_leave_kill_counter(self, leave):
		self.mouse_over_kill_counter = False

	def _on_mousewheel(self, event):
		if(self.mouse_over_kill_counter):
			self.kill_counter += int(event.delta/120)
			if(self.kill_counter < 0):
				self.kill_counter = 0
			if(self.kill_counter > 999):
				self.kill_counter = 999
			self.buttonKILLCOUNTER['text'] = str(self.kill_counter)
			if(self.kill_counter > 0):
				self.buttonKILLCOUNTER['bg'] = self.selected_button_color
			else:
				self.buttonKILLCOUNTER['bg'] = self.main_button_color

	# --------------------------------------------------------------------------------------------------
	# PREFERENCES WINDOW FUNCTIONS

	def saveAndExitPreferences(self, window):
		self.write_user_data()
		self.loadClipDataBase()
		self.clip_name_list = self.getClipList()
		window.destroy()


	def openClipFolderDialog(self):
		self.clip_video_folder_path =  filedialog.askdirectory()
		self.clip_folder_path_label['text'] = self.clip_video_folder_path


	def openDataFolderDialog(self):
		self.clip_data_base_file_path =  filedialog.askdirectory()
		self.clip_data_path_label['text'] = self.clip_data_base_file_path


	def loadUserData(self):
		config_file = ""
		for file_name in os.listdir("User/"):
			if("config" in file_name and ".json" in file_name):
				config_file = file_name
				break
		if(config_file == ""):
			self.showError("Error while loading user config file !", "File doesn't exist !")
		else:
			code, data = self.loadData("User/"+config_file)
			if(code == -1):
				self.showError("Error while reading user config file !", data)
			else:
				return "User/"+config_file, data


	def loadUserConfig(self):
		config_file = ""
		for file_name in os.listdir("User/"):
			if("config" in file_name and ".json" in file_name):
				config_file = file_name
				break

		if(config_file == ""):
			self.showInfo("Important !", "No user config file found,\ncreating new one.")
			config_file = self.createUserConfig()
			code, data = self.loadData("User/"+config_file)
			if(code == -1):
				self.showError("Error while reading user config file !", data)
			else:
				self.user_config_file_path = "User/"+config_file
				self.clip_video_folder_path = data["CLIP_FILE_PATH"]
				self.clip_data_base_file_path = data["CLIP_DATA_BASE_PATH"]
				self.last_opened_clip = data["LAST_OPENED_CLIP"]
		else:
			code, data = self.loadData("User/"+config_file)
			if(code == -1):
				self.showError("Error while reading user config file !", data)
			else:
				self.user_config_file_path = "User/"+config_file
				self.clip_video_folder_path = data["CLIP_FILE_PATH"]
				self.clip_data_base_file_path = data["CLIP_DATA_BASE_PATH"]
				self.last_opened_clip = data["LAST_OPENED_CLIP"]


	def createUserConfig(self):
		now = datetime.now()
		filename = now.strftime("%d-%m-%Y %H-%M-%S")
		f = open("User/config"+filename+".json", "w")
		user_data = {"CLIP_FILE_PATH":"", "CLIP_DATA_BASE_PATH":"", "LAST_OPENED_CLIP":""}
		json.dump(user_data, f, indent=6)
		f.close()
		return "config"+filename+".json"


	def findLastOpenedClip(self):
		if(self.clip_name_list != None):
			if(self.last_opened_clip != "" and self.last_opened_clip in self.clip_name_list):
				self.current_clip_index = self.clip_name_list.index(self.last_opened_clip)


	def openInDefaultPlayer(self):
		if(self.clip_name_list != None):
			if(self.clip_name_list[self.current_clip_index] != None):
				os.startfile(self.clip_video_folder_path+"/"+self.clip_name_list[self.current_clip_index])


	def loadClipDataBase(self):
		if(self.clip_data_base_file_path != ""):
			if(os.path.isfile(self.clip_data_base_file_path+"/Clip_Sorter_Data_Base.json")):
				code, data = self.loadData(self.clip_data_base_file_path+"/Clip_Sorter_Data_Base.json")
				if(code != -1):
					self.main_data_base = data

	# --------------------------------------------------------------------------------------------------
	# OTHER FUNCTIONS

	def INFO(self):
		print("INFO")
		#print(self.main_data_base)


	# --------------------------------------------------------------------------------------------------

	def saveCurrentToDict(self):
		current_clip_data = self.getData()
		if(current_clip_data != None):
			current_clip_data_name = list(current_clip_data.keys())[0]
			if(current_clip_data_name not in self.main_data_base):
				self.main_data_base[current_clip_data_name] = current_clip_data[current_clip_data_name]
			else:
				self.main_data_base[current_clip_data_name] = current_clip_data[current_clip_data_name]

	# --------------------------------------------------------------------------------------------------

	def getData(self):
		if(self.clip_name_list != None):
			return {
				self.clip_name_list[self.current_clip_index] : 
				{
					"GRADE" : self.clip_grade_selected,
					"KILL" : self.kill_counter,
					"CLASS" : self.class_selected,
					"W1" : self.primary_weapon_selected,
					"W2" : self.secondary_weapon_selected,
					"G1" : self.gadget1_selected,
					"G2" : self.gadget2_selected,
					"G3" : self.gadget3_selected,
					"MELEE" : self.melee_weapon_selected,
					"MAP" : self.map_selected,
					"COUNTRY" : self.country_selected,
					"VEHICULE" : list(self.vehicule_selected),
					"SR" : list(self.reinforcements_selected),
					"STATIC" : list(self.static_weapon_selected),
					"TAGS" : list(self.tag_set)
				}
			}
		else:
			return None


	def cleanInterfaceSelection(self):
		self.cleanCountryButton()
		self.cleanGradeButton()
		self.cleanKillCounterButton()
		self.cleanClassButton()
		self.cleanPrimaryWeaponList()
		self.cleanSecondaryWeaponButton()
		self.cleanGadgetList()
		self.cleanButtonMelee()
		self.cleanReinforcements()
		self.cleanVehiculesList()
		self.cleanMapButton()
		self.cleanStaticWeapon()
		self.cleanTagButton()


	def setValue(self, grade, kill, class_, w1, w2, g1, g2, g3, melee, map_, country, vehicules, squad_calls, static_ws, tags):
		self.cleanInterfaceSelection()
		self.setClipGrade(grade)
		self.setKillCounter(kill)
		self.setClass(class_)
		self.setPrimaryWeapon(w1)
		self.setSecondaryWeapon(w2)
		self.setGadget1(g1)
		self.setGadget2(g2)
		self.setGadget3(g3)
		self.setMelee(melee)
		self.setMap(map_)
		self.setCountry(country)
		self.setVehicule(vehicules)
		self.setReinforcement(squad_calls)
		self.setStaticWeapon(static_ws)
		self.setTags(tags)

	# --------------------------------------------------------------------------------------------------

	def scrollListRetrieve(self):
		value = self.clip_scroll_list.get()
		if ("[No Data]" in value):
			value = value[:-12]
		self.updateCurrentClip(value)


	def updateScrollList(self):
		self.clip_scroll_list.destroy()
		self.clip_scroll_list = Combobox(self.combobox_button_frame, width=40, height=40, justify=LEFT, state="readonly")
		self.clip_scroll_list.pack(side=LEFT, padx=5, pady=5)
		self.clip_scroll_list['value'] = self.getClipListAlt()
		self.scroll_list_retrieve.destroy()
		self.scroll_list_retrieve = Button(self.combobox_button_frame, text="Select", font=self.main_font, bg=self.main_button_color, fg=self.text_color, command=self.scrollListRetrieve)
		self.scroll_list_retrieve.pack(side=LEFT, padx=5, pady=5)



	def updateCurrentClip(self, clip_name):
		if(self.clip_name_list != None):
			if(clip_name in self.clip_name_list):
				self.current_clip_index = self.clip_name_list.index(clip_name)
				self.clip_label['text'] = self.clip_name_list[self.current_clip_index]

			if(self.clip_name_list[self.current_clip_index] in self.main_data_base.keys()):
				dict_k = self.main_data_base[self.clip_name_list[self.current_clip_index]]
				self.setValue(dict_k["GRADE"], dict_k["KILL"], dict_k["CLASS"], dict_k["W1"], dict_k["W2"], dict_k["G1"], dict_k["G2"], dict_k["G3"], dict_k["MELEE"], dict_k["MAP"], dict_k["COUNTRY"], dict_k["VEHICULE"], dict_k["SR"], dict_k["STATIC"], dict_k["TAGS"])
			else:
				self.cleanInterfaceSelection()

	# --------------------------------------------------------------------------------------------------

	def scanClipFolder(self):
		self.write_user_data()
		self.saveCurrentToDict()
		self.writeClipData()
		self.clip_name_list = self.getClipList()
		self.clip_scroll_list['value'] = self.getClipListAlt()
		self.loadClipDataBase()


	def getClipList(self):
		clip_list = []
		if(self.clip_video_folder_path != ""):
			try:
				for clip in os.listdir(self.clip_video_folder_path):
					if(".mp4" in clip or ".MP4" in clip or ".mkv" in clip or ".MKV" in clip):
						clip_list.append(clip)
				return clip_list
			except Exception as e:
				self.showError("Error ", e)

	def getClipListAlt(self):
		clip_list = []
		if(self.clip_video_folder_path != ""):
			try:
				for clip in os.listdir(self.clip_video_folder_path):
					if(".mp4" in clip or ".MP4" in clip or ".mkv" in clip or ".MKV" in clip):
						if(self.hasData(clip)):
							clip_list.append(clip)
						else:
							clip_list.append(clip+"   [No Data]")
				return clip_list
			except Exception as e:
				self.showError("Error ", e)


	def hasData(self, clip_name):
		if(clip_name in self.main_data_base.keys()):
			cref = self.main_data_base[clip_name]
			if(cref["GRADE"] == 0 and cref["KILL"] == 0 and cref["CLASS"] == None and cref["W1"] == None and cref["W2"] == None and cref["G2"] == None and cref["G3"] == None and cref["MELEE"] == None and cref["MAP"] == None and cref["COUNTRY"] == None and cref["VEHICULE"] == [] and cref["SR"] == [] and cref["STATIC"] == [] and cref["TAGS"] == []):
				return False
			else:
				return True


	def on_root_closing(self):
		self.write_user_data()
		self.saveCurrentToDict()
		self.writeClipData()
		self.root.destroy()

	def on_root_closing2(self):
		self.write_user_data()
		self.root.destroy()


	def write_user_data(self):
		filename, user_data = self.loadUserData()
		user_data["CLIP_FILE_PATH"] = self.clip_video_folder_path
		user_data["CLIP_DATA_BASE_PATH"] = self.clip_data_base_file_path
		if(self.write_last_clip):
			if(self.clip_name_list != None):
				user_data["LAST_OPENED_CLIP"] = self.clip_name_list[self.current_clip_index]
		try:
			f = open(filename, "w")
			json.dump(user_data, f, indent=6)
			f.close()
		except Exception as e:
			self.showError("Error while loading user config file !", e)


	def loadData(self, json_file):
		try:
			file = open(json_file, "r")
			data = json.load(file)
			file.close()
			return 0, data
		except Exception as e:
			print(e)
			return -1, e


	def writeClipData(self):
		try:
			file = open(self.clip_data_base_file_path+"/Clip_Sorter_Data_Base.json", "w")
			json.dump(self.main_data_base, file, indent=6)
			file.close()
		except Exception as e:
			print(e)
			return -1


	def loadCurrentClipData(self):
		if(self.clip_name_list != None and self.main_data_base != None):
			if(self.clip_name_list[self.current_clip_index] in self.main_data_base.keys()):
				dict_k = self.main_data_base[self.clip_name_list[self.current_clip_index]]
				self.setValue(dict_k["GRADE"], dict_k["KILL"], dict_k["CLASS"], dict_k["W1"], dict_k["W2"], dict_k["G1"], dict_k["G2"], dict_k["G3"], dict_k["MELEE"], dict_k["MAP"], dict_k["COUNTRY"], dict_k["VEHICULE"], dict_k["SR"], dict_k["STATIC"], dict_k["TAGS"])
			else:
				self.cleanInterfaceSelection()

	# --------------------------------------------------------------------------------------------------

	def getPrimaryWeapon(self, data_set, selected_class):
		if(selected_class != "None"):
			return data_set[selected_class]["W1"]


	def loadPrimaryWeaponButton(self, data_set, selected_class):
		self.cleanPrimaryWeaponList()
		if(selected_class != None):
			weapon_list = self.getPrimaryWeapon(data_set, selected_class)
			if(weapon_list != None and "None" not in weapon_list):
				weapon_list_half_size = math.ceil(len(weapon_list)/2)
				self.button_primary_weapon_ref = [[None for x in range(2)] for x in range(weapon_list_half_size)]
				weapon_index = 0
				self.primary_weapon_selected = None
				for x in range(weapon_list_half_size):
					for y in range(2):
						if(weapon_index == len(weapon_list)):
							break
						else:
							if(selected_class == "ASSAULT"):
								weapon_icon = PhotoImage(file="Icons/Assault/"+weapon_list[weapon_index]+".png")
							elif(selected_class == "MEDIC"):
								weapon_icon = PhotoImage(file="Icons/Medic/"+weapon_list[weapon_index]+".png")
							elif(selected_class == "SUPPORT"):
								weapon_icon = PhotoImage(file="Icons/Support/"+weapon_list[weapon_index]+".png")
							else:
								weapon_icon = PhotoImage(file="Icons/Recon/"+weapon_list[weapon_index]+".png")
							if(y == 0):
								b = Button(self.primary_weapon_frame_left, command=lambda x=x, y=y:self.primaryWeaponHandler(x,y), text=weapon_list[weapon_index], relief="raised", bg=self.main_button_color, image=weapon_icon)
								b.image = weapon_icon
								self.button_primary_weapon_ref[x][y] = b
								b.pack(side=TOP)
							else:
								b = Button(self.primary_weapon_frame_right, command=lambda x=x, y=y:self.primaryWeaponHandler(x,y), text=weapon_list[weapon_index], relief="raised", bg=self.main_button_color, image=weapon_icon)
								b.image = weapon_icon
								self.button_primary_weapon_ref[x][y] = b
								b.pack(side=TOP)
						weapon_index += 1


	def cleanPrimaryWeaponList(self):
		for sub_list in self.button_primary_weapon_ref:
			for button in sub_list:
				if(button != None):
					button.destroy()
		self.button_primary_weapon_ref.clear()
		self.primary_weapon_selected = None


	def switchOffPrimaryButtonExcept(self):
		for element in self.button_primary_weapon_ref:
			for button in element:
				if(button != None):
					if(button['text'] == self.primary_weapon_selected):
						button['bg'] = self.selected_button_color
					else:
						button['bg'] = self.main_button_color


	def primaryWeaponHandler(self, x, y):
		if(self.button_primary_weapon_ref[x][y]['bg'] == self.selected_button_color):
			self.button_primary_weapon_ref[x][y]['bg'] = self.main_button_color
			self.primary_weapon_selected = None
		else:
			self.button_primary_weapon_ref[x][y]['bg'] = self.selected_button_color
			self.primary_weapon_selected = self.button_primary_weapon_ref[x][y]['text']
		self.switchOffPrimaryButtonExcept()
	
	# --------------------------------------------------------------------------------------------------

	def getSecondaryWeapon(self, data_set):
		return data_set["W2"]


	def loadSecondaryWeapon(self):
		self.cleanSecondaryWeaponButton()
		if(self.class_selected != None):
			code, data = self.loadData("Data/Infantry.json")
			if(code != -1):
				weapon_list = self.getSecondaryWeapon(data)
				if(weapon_list != None and "None" not in weapon_list):
					weapon_list_half_size = math.ceil(len(weapon_list)/2)
					self.button_secondary_weapon_ref = [[None for x in range(2)] for x in range(weapon_list_half_size)]
					weapon_index = 0
					self.secondary_weapon_selected = None
					for x in range(weapon_list_half_size):
						for y in range(2):
							if(weapon_index == len(weapon_list)):
								break
							else:
								weapon_icon = PhotoImage(file="Icons/Secondary/"+weapon_list[weapon_index]+".png")
								if(y == 0):
									b = Button(self.secondary_weapon_frame_left, command=lambda x=x, y=y:self.secondaryWeaponHandler(x,y), text=weapon_list[weapon_index], relief="raised", bg=self.main_button_color, image=weapon_icon)
									b.image = weapon_icon
									self.button_secondary_weapon_ref[x][y] = b
									b.pack(side=TOP)
								else:
									b = Button(self.secondary_weapon_frame_right, command=lambda x=x, y=y:self.secondaryWeaponHandler(x,y), text=weapon_list[weapon_index], relief="raised", bg=self.main_button_color, image=weapon_icon)
									b.image = weapon_icon
									self.button_secondary_weapon_ref[x][y] = b
									b.pack(side=TOP)
							weapon_index += 1


	def switchOffSecondaryButtonExcept(self):
		for element in self.button_secondary_weapon_ref:
			for button in element:
				if(button != None):
					if(button['text'] == self.secondary_weapon_selected):
						button['bg'] = self.selected_button_color
					else:
						button['bg'] = self.main_button_color


	def secondaryWeaponHandler(self, x, y):
		if(self.button_secondary_weapon_ref[x][y]['bg'] == self.selected_button_color):
			self.button_secondary_weapon_ref[x][y]['bg'] = self.main_button_color
			self.secondary_weapon_selected = None
		else:
			self.button_secondary_weapon_ref[x][y]['bg'] = self.selected_button_color
			self.secondary_weapon_selected = self.button_secondary_weapon_ref[x][y]['text']
		self.switchOffSecondaryButtonExcept()


	def cleanSecondaryWeaponButton(self):
		for button_tuple in self.button_secondary_weapon_ref:
			for button in button_tuple:
				if(button != None):
					#button['bg'] = self.main_button_color
					button.destroy()
		self.secondary_weapon_selected = None

	# --------------------------------------------------------------------------------------------------

	def loadGadgetButton(self, data_set, selected_class):
		self.cleanGadgetList()
		if(selected_class != None):
			for weapon in self.infantry_data[selected_class]:
				for i in range(1,4):
					gadget_num = "G"+str(i)
					if(gadget_num in weapon):
						for gadget_index in range(len(self.infantry_data[selected_class][weapon])):
							gadget_icon = PhotoImage(file="Icons/Gadgets/G"+str(i)+"/"+self.infantry_data[selected_class][weapon][gadget_index]+".png")
							b = Button(self.frame_gadget_ref[i-1], command=lambda x=i-1, y=gadget_index:self.gadgetHandler(x, y), text=self.infantry_data[selected_class][weapon][gadget_index], relief="raised", bg=self.main_button_color, image=gadget_icon)
							b.image = gadget_icon
							b.pack(side=TOP)
							self.button_gadget_ref[i-1].append(b)


	def gadgetHandler(self, x, y):
		for gadget_index in range(len(self.button_gadget_ref[x])):
			if(gadget_index == y):
				if(self.button_gadget_ref[x][gadget_index]['bg'] == self.selected_button_color):
					self.button_gadget_ref[x][gadget_index]['bg'] = self.main_button_color
					if(x == 0):
						self.gadget1_selected = None
					elif(x == 1):
						self.gadget2_selected = None
					elif(x == 2):
						self.gadget3_selected = None
					else:
						return
				else:
					self.button_gadget_ref[x][gadget_index]['bg'] = self.selected_button_color
					if(x == 0):
						self.gadget1_selected = self.button_gadget_ref[x][gadget_index]['text']
					elif(x == 1):
						self.gadget2_selected = self.button_gadget_ref[x][gadget_index]['text']
					elif(x == 2):
						self.gadget3_selected = self.button_gadget_ref[x][gadget_index]['text']
					else:
						return
			else:
				self.button_gadget_ref[x][gadget_index]['bg'] = self.main_button_color


	def cleanGadgetList(self):
		self.gadget1_selected = None
		self.gadget2_selected = None
		self.gadget3_selected = None
		for gadget_list in self.button_gadget_ref:
			for button in gadget_list:
				if(button != None):
					button.destroy()
			gadget_list.clear()

	# --------------------------------------------------------------------------------------------------

	def button_melee_clicked(self):
		if(self.melee_button['bg'] == self.selected_button_color):
			self.melee_button['bg'] = self.main_button_color
			self.melee_weapon_selected = None
		else:
			self.melee_button['bg'] = self.selected_button_color
			self.melee_weapon_selected = "Melee"


	def cleanButtonMelee(self):
		self.melee_button['bg'] = self.main_button_color
		self.melee_weapon_selected = None

	# --------------------------------------------------------------------------------------------------

	def loadReinforcements(self):
		self.cleanReinforcements()
		if(self.country_selected != None):
			code, data = self.loadData("Data/Reinforcements.json")
			if(code != -1):
				for reinf in data[self.country_selected]:
					reinf_icon = PhotoImage(file="Icons/Reinforcements/"+reinf+".png")
					b = Button(self.reinforcements_frame, command=lambda x=reinf:self.reinforcementHandler(x), text=reinf, relief="raised", bg=self.main_button_color, image=reinf_icon)
					b.image = reinf_icon
					b.pack(side=TOP)
					self.button_reinforcement_ref.append(b)


	def cleanReinforcements(self):
		for button in self.button_reinforcement_ref:
			if(button != None):
				button.destroy()
		self.button_reinforcement_ref.clear()
		self.reinforcements_selected.clear()


	def reinforcementHandler(self, x):
		for button in self.button_reinforcement_ref:
			if(button != None and button['text'] == x):
				if(button['bg'] == self.selected_button_color):
					button['bg'] = self.main_button_color
					self.reinforcements_selected.remove(x)
				else:
					button['bg'] = self.selected_button_color
					self.reinforcements_selected.add(x)

	# --------------------------------------------------------------------------------------------------

	def loadStaticWeaponButton(self):
		code, data = self.loadData("Data/Infantry.json")
		if(code != -1):
			for static_weapon in data["STATIC WEAPONS & PICKUP"]:
				sw_icon = PhotoImage(file="Icons/Vehicules/Statics/"+static_weapon+".png")
				b = Button(self.static_weapon_frame, command=lambda w_n=static_weapon:self.staticWeaponHandler(w_n), text=static_weapon, relief="raised", bg=self.main_button_color, image=sw_icon)
				b.image = sw_icon
				self.button_static_ref.append(b)
				b.pack(side=TOP)


	def staticWeaponHandler(self, weapon_name):
		for button in self.button_static_ref:
			if(button['text'] == weapon_name):
				if(weapon_name in self.static_weapon_selected):
					button['bg'] = self.main_button_color
					self.static_weapon_selected.remove(button['text'])
				else:
					button['bg'] = self.selected_button_color
					self.static_weapon_selected.add(button['text'])


	def cleanStaticWeapon(self):
		for button in self.button_static_ref:
			button['bg'] = self.main_button_color
		self.static_weapon_selected.clear()




	# --------------------------------------------------------------------------------------------------

	def getMapList(self, data):
		map_list = []
		for element in data["MAPS"]:
			map_list.append(element)
		return map_list


	def loadMapButton(self):
		code, map_data = self.loadData("Data/Maps.json")
		if(code != -1):
			map_list = self.getMapList(map_data)
			for map_index in range(len(map_list)):
				map_icon = PhotoImage(file="Icons/Maps/"+map_list[map_index]+".png")
				b = Button(self.map_frame, command=lambda map_index=map_index:self.mapHandler(map_index), text=map_list[map_index], relief="raised", bg=self.main_button_color, image=map_icon)
				b.image = map_icon
				self.map_button_ref.append(b)
				b.pack(side=TOP, pady=(0,0))
		#self.back_to_menu = Button(self.map_frame, text="Main\nMenu", font=self.main_font, bg=self.main_button_color, fg=self.text_color, command=self.loadMenu)
		#self.back_to_menu.pack(side=BOTTOM, fill=X)


	def mapHandler(self, map_index):
		for button_index in range(len(self.map_button_ref)):
			if(button_index == map_index):
				if(self.map_button_ref[button_index]['bg'] == self.selected_button_color):
					self.map_button_ref[button_index]['bg'] = self.main_button_color
					self.map_selected = None
				else:
					self.map_button_ref[button_index]['bg'] = self.selected_button_color
					self.map_selected = self.map_button_ref[button_index]['text']
			else:
				self.map_button_ref[button_index]['bg'] = self.main_button_color
		self.lockCountryExceptMap()
		self.loadVehiculesByMapsCountry()


	def lockMapExceptCountry(self):
		if(self.country_selected != None):
			code, map_data = self.loadData("Data/Maps.json")
			if(code != -1):
				for map_ in map_data["MAPS"]:
					for button in self.map_button_ref:
						if(button['text'] == map_):
							if(self.country_selected not in map_data["MAPS"][map_]):
								button['state'] = DISABLED
								button['bg'] = self.main_button_color
							else:
								button['state'] = NORMAL
								button['bg'] = self.main_button_color

							if(button['text'] == self.map_selected and button['state'] == DISABLED):
								self.map_selected = None

							if(button['text'] == self.map_selected and button['state'] == NORMAL):
								button['bg'] = self.selected_button_color
		else:
			for button in self.map_button_ref:
				button['state'] = NORMAL
				if(button['text'] ==self.map_selected):
					button['bg'] = self.selected_button_color


	def cleanMapButton(self):
		for button in self.map_button_ref:
			button['bg'] = self.main_button_color
			button['state'] = NORMAL
		self.map_selected = None

	# --------------------------------------------------------------------------------------------------

	def getVehiculeByMapsByCountry(self, data):
		return data[self.map_selected][self.country_selected]


	def loadVehiculesByMapsCountry(self):
		self.cleanVehiculesList()
		if(self.country_selected != None and self.map_selected != None):
			code, map_data = self.loadData("Data/Maps.json")
			if(code != -1):
				vehicules_type_list = self.getVehiculeByMapsByCountry(map_data["MAPS"])
				for vehicule in vehicules_type_list:
					vehicule_icon = PhotoImage(file="Icons/Vehicules/"+self.country_selected+"/"+vehicule+".png")
					b = Button(self.vehicules_frame, command=lambda x=vehicule:self.vehiculesHandler(x), text=vehicule, relief="raised", bg=self.main_button_color, image=vehicule_icon)
					b.image = vehicule_icon
					b.pack(side=TOP)
					self.button_vehicules_ref.append(b)


	def cleanVehiculesList(self):
		for button in self.button_vehicules_ref:
			if(button != None):
				button.destroy()
		self.button_vehicules_ref.clear()
		self.vehicule_selected.clear()


	def vehiculesHandler(self, x):
		for button in self.button_vehicules_ref:
			if(button['text'] == x):
				if(button['text'] in self.vehicule_selected):
					button['bg'] = self.main_button_color
					self.vehicule_selected.remove(button['text'])
				else:
					button['bg'] = self.selected_button_color
					self.vehicule_selected.add(button['text'])
			else:
				button['bg'] = self.main_button_color
				if(button['text'] in self.vehicule_selected):
					self.vehicule_selected.remove(button['text'])

	# --------------------------------------------------------------------------------------------------

	# ALERT BOX
	def showError(self, title, msg):
		messagebox.showerror(title, msg)

	def showInfo(self, title, msg):
		messagebox.showinfo(title, msg)

	# --------------------------------------------------------------------------------------------------

	def buttonASSAULT_clicked(self):
		self.updateCLASSbutton(self.button_CLASS_ref, self.buttonASSAULT)


	def buttonMEDIC_clicked(self):
		self.updateCLASSbutton(self.button_CLASS_ref, self.buttonMEDIC)	


	def buttonSUPPORT_clicked(self):
		self.updateCLASSbutton(self.button_CLASS_ref, self.buttonSUPPORT)


	def buttonRECON_clicked(self):
		self.updateCLASSbutton(self.button_CLASS_ref, self.buttonRECON)


	def updateCLASSbutton(self, button_ref_tab, clicked_button):
		if(clicked_button != self.last_CLASS_clicked):
			for button in button_ref_tab:
				if(button != clicked_button):
					button['bg'] = self.main_button_color
				else:
					button['bg'] = self.selected_button_color
					self.last_CLASS_clicked = button
					if(button == self.buttonASSAULT):
						self.class_selected = "ASSAULT"
					elif(button == self.buttonMEDIC):
						self.class_selected = "MEDIC"
					elif(button == self.buttonSUPPORT):
						self.class_selected = "SUPPORT"
					else:
						self.class_selected = "RECON"
		else:
			if(clicked_button['bg'] == self.main_button_color):
				clicked_button['bg'] = self.selected_button_color
				if(clicked_button == self.buttonASSAULT):
					self.class_selected = "ASSAULT"
				elif(clicked_button == self.buttonMEDIC):
					self.class_selected = "MEDIC"
				elif(clicked_button == self.buttonSUPPORT):
					self.class_selected = "SUPPORT"
				else:
					self.class_selected = "RECON"
			else:
				clicked_button['bg'] = self.main_button_color
				self.class_selected = None
			self.last_CLASS_clicked = clicked_button
		self.loadPrimaryWeaponButton(self.infantry_data, self.class_selected)
		self.loadGadgetButton(self.infantry_data, self.class_selected)
		self.loadSecondaryWeapon()


	def cleanClassButton(self):
		for button in self.button_CLASS_ref:
			button['bg'] = self.main_button_color
		self.class_selected = None

	# --------------------------------------------------------------------------------------------------

	def button_save_clicked(self):
		self.saveCurrentToDict()
		self.writeClipData()
		self.updateScrollList()


	def button_reset_clicked(self):
		self.cleanInterfaceSelection()

	# --------------------------------------------------------------------------------------------------

	def button_next_clicked(self):
		if(self.clip_name_list != None):
			self.saveCurrentToDict()
			if(self.current_clip_index < len(self.clip_name_list)-1):
				self.current_clip_index += 1
				self.clip_label['text'] = self.clip_name_list[self.current_clip_index]

			if(self.clip_name_list[self.current_clip_index] in self.main_data_base.keys()):
				dict_k = self.main_data_base[self.clip_name_list[self.current_clip_index]]
				self.setValue(dict_k["GRADE"], dict_k["KILL"], dict_k["CLASS"], dict_k["W1"], dict_k["W2"], dict_k["G1"], dict_k["G2"], dict_k["G3"], dict_k["MELEE"], dict_k["MAP"], dict_k["COUNTRY"], dict_k["VEHICULE"], dict_k["SR"], dict_k["STATIC"], dict_k["TAGS"])
			else:
				self.cleanInterfaceSelection()
			self.writeClipData()
			self.updateScrollList()
		
			
	def button_previous_clicked(self):
		if(self.clip_name_list != None):
			self.saveCurrentToDict()
			if(self.current_clip_index > 0):
				self.current_clip_index -= 1
				self.clip_label['text'] = self.clip_name_list[self.current_clip_index]

			if(self.clip_name_list[self.current_clip_index] in self.main_data_base.keys()):
				dict_k = self.main_data_base[self.clip_name_list[self.current_clip_index]]
				self.setValue(dict_k["GRADE"], dict_k["KILL"], dict_k["CLASS"], dict_k["W1"], dict_k["W2"], dict_k["G1"], dict_k["G2"], dict_k["G3"], dict_k["MELEE"], dict_k["MAP"], dict_k["COUNTRY"], dict_k["VEHICULE"], dict_k["SR"], dict_k["STATIC"], dict_k["TAGS"])
			else:
				self.cleanInterfaceSelection()
			self.writeClipData()
			self.updateScrollList()

	# --------------------------------------------------------------------------------------------------
	
	def buttonMINUS_clicked(self):
		if(self.kill_counter > 0):
			self.kill_counter -= 1
			self.buttonKILLCOUNTER['text'] = str(self.kill_counter)
		if(self.kill_counter > 0):
			self.buttonKILLCOUNTER['bg'] = self.selected_button_color
		else:
			self.buttonKILLCOUNTER['bg'] = self.main_button_color

	
	def buttonKILLCOUNTER_clicked(self):
		self.kill_counter = 0
		self.buttonKILLCOUNTER['text'] = str(self.kill_counter)
		self.buttonKILLCOUNTER['bg'] = self.main_button_color


	def buttonPLUS_clicked(self):
		self.kill_counter += 1
		self.buttonKILLCOUNTER['text'] = str(self.kill_counter)
		if(self.kill_counter > 0):
			self.buttonKILLCOUNTER['bg'] = self.selected_button_color
		else:
			self.buttonKILLCOUNTER['bg'] = self.main_button_color


	def cleanKillCounterButton(self):
		self.kill_counter = 0
		self.buttonKILLCOUNTER['text'] = str(self.kill_counter)
		self.buttonKILLCOUNTER['bg'] = self.main_button_color

	# --------------------------------------------------------------------------------------------------

	def buttonSTAR1_clicked(self):
		self.updateSTARbutton(self.button_STAR_ref, self.button_star_pressed, 0)


	def buttonSTAR2_clicked(self):
		self.updateSTARbutton(self.button_STAR_ref, self.button_star_pressed, 1)


	def buttonSTAR3_clicked(self):
		self.updateSTARbutton(self.button_STAR_ref, self.button_star_pressed, 2)


	def buttonSTAR4_clicked(self):
		self.updateSTARbutton(self.button_STAR_ref, self.button_star_pressed, 3)


	def buttonSTAR5_clicked(self):
		self.updateSTARbutton(self.button_STAR_ref, self.button_star_pressed, 4)


	def updateSTARbutton(self, button_star_ref, button_pressed_tab, index):
		if(button_pressed_tab[index]):
			if(index < 4 and button_pressed_tab[index+1]):
				for i in range(len(button_pressed_tab)):
					if(i <= index):
						button_pressed_tab[i] = True
						button_star_ref[i]['bg'] = self.selected_button_color
					else:
						button_pressed_tab[i] = False
						button_star_ref[i]['bg'] = self.main_button_color
				self.clip_grade_selected = index+1
			else:
				for i in range(0, index+1):
					button_pressed_tab[i] = False
					button_star_ref[i]['bg'] = self.main_button_color
				self.clip_grade_selected = None
		else:
			for i in range(len(button_pressed_tab)):
				if(i <= index):
					button_pressed_tab[i] = True
					button_star_ref[i]['bg'] = self.selected_button_color
				else:
					button_pressed_tab[i] = False
					button_star_ref[i]['bg'] = self.main_button_color
			self.clip_grade_selected = index+1


	def cleanGradeButton(self):
		for button in self.button_STAR_ref:
			button['bg'] = self.main_button_color
			button['bg'] = self.main_button_color
		for i in range(len(self.button_star_pressed)):
			self.button_star_pressed[i] = False
		self.clip_grade_selected = 0

	# --------------------------------------------------------------------------------------------------

	def buttonGE_clicked(self):
		self.updateCOUNTRYbutton(self.button_COUNTRY_ref, self.buttonGE)
		self.lockMapExceptCountry()


	def buttonJP_clicked(self):
		self.updateCOUNTRYbutton(self.button_COUNTRY_ref, self.buttonJP)	
		self.lockMapExceptCountry()


	def buttonUK_clicked(self):
		self.updateCOUNTRYbutton(self.button_COUNTRY_ref, self.buttonUK)
		self.lockMapExceptCountry()


	def buttonUSA_clicked(self):
		self.updateCOUNTRYbutton(self.button_COUNTRY_ref, self.buttonUSA)
		self.lockMapExceptCountry()


	def updateCOUNTRYbutton(self, button_ref_tab, clicked_button):
		if(clicked_button != self.last_COUNTRY_clicked):
			for button in button_ref_tab:
				if(button != clicked_button):
					button['bg'] = self.main_button_color
				else:
					button['bg'] = self.selected_button_color
					self.last_COUNTRY_clicked = button
					if(button == self.buttonGE):
						self.country_selected = "GE"
					elif(button == self.buttonJP):
						self.country_selected = "JP"
					elif(button == self.buttonUK):
						self.country_selected = "UK"
					else:
						self.country_selected = "USA"
		else:
			if(clicked_button['bg'] == self.main_button_color):
				clicked_button['bg'] = self.selected_button_color
				if(clicked_button == self.buttonGE):
					self.country_selected = "GE"
				elif(clicked_button == self.buttonJP):
					self.country_selected = "JP"
				elif(clicked_button == self.buttonUK):
					self.country_selected = "UK"
				else:
					self.country_selected = "USA"
			else:
				clicked_button['bg'] = self.main_button_color
				self.country_selected = None
			self.last_COUNTRY_clicked = clicked_button
		self.loadReinforcements()
		self.loadVehiculesByMapsCountry()


	def lockCountryExceptMap(self):
		if(self.map_selected != None):
			code, map_data = self.loadData("Data/Maps.json")
			if(code != -1):
				for button in self.button_COUNTRY_ref:
					if(button['text'] not in map_data["MAPS"][self.map_selected]):
						button['state'] = DISABLED
					else:
						button['state'] = NORMAL
		else:
			for button in self.button_COUNTRY_ref:
				button['state'] = NORMAL


	def cleanCountryButton(self):
		for button in self.button_COUNTRY_ref:
			button['bg'] = self.main_button_color
			button['state'] = NORMAL
		self.country_selected = None

	# --------------------------------------------------------------------------------------------------

	def button_fun_clicked(self):
		if(self.fun_tag_button['text'] in self.tag_set):
			self.tag_set.remove(self.fun_tag_button['text'])
			self.fun_tag_button['bg'] = self.main_button_color
		else:
			self.tag_set.add(self.fun_tag_button['text'])
			self.fun_tag_button['bg'] = self.selected_button_color


	def button_wtf_clicked(self):
		if(self.wtf_tag_button['text'] in self.tag_set):
			self.tag_set.remove(self.wtf_tag_button['text'])
			self.wtf_tag_button['bg'] = self.main_button_color
		else:
			self.tag_set.add(self.wtf_tag_button['text'])
			self.wtf_tag_button['bg'] = self.selected_button_color


	def button_monsterkill_clicked(self):
		if(self.monsterkill_tag_button['text'] in self.tag_set):
			self.tag_set.remove(self.monsterkill_tag_button['text'])
			self.monsterkill_tag_button['bg'] = self.main_button_color
		else:
			self.tag_set.add(self.monsterkill_tag_button['text'])
			self.monsterkill_tag_button['bg'] = self.selected_button_color


	def button_lucky_clicked(self):
		if(self.lucky_tag_button['text'] in self.tag_set):
			self.tag_set.remove(self.lucky_tag_button['text'])
			self.lucky_tag_button['bg'] = self.main_button_color
		else:
			self.tag_set.add(self.lucky_tag_button['text'])
			self.lucky_tag_button['bg'] = self.selected_button_color


	def button_roadkill_clicked(self):
		if(self.roadkill_tag_button['text'] in self.tag_set):
			self.tag_set.remove(self.roadkill_tag_button['text'])
			self.roadkill_tag_button['bg'] = self.main_button_color
		else:
			self.tag_set.add(self.roadkill_tag_button['text'])
			self.roadkill_tag_button['bg'] = self.selected_button_color


	def button_bug_clicked(self):
		if(self.bug_tag_button['text'] in self.tag_set):
			self.tag_set.remove(self.bug_tag_button['text'])
			self.bug_tag_button['bg'] = self.main_button_color
		else:
			self.tag_set.add(self.bug_tag_button['text'])
			self.bug_tag_button['bg'] = self.selected_button_color


	def button_fragmovie_clicked(self):
		if(self.fragmovie_tag_button['text'] in self.tag_set):
			self.tag_set.remove(self.fragmovie_tag_button['text'])
			self.fragmovie_tag_button['bg'] = self.main_button_color
		else:
			self.tag_set.add(self.fragmovie_tag_button['text'])
			self.fragmovie_tag_button['bg'] = self.selected_button_color


	def button_insane_clicked(self):
		if(self.insane_tag_button['text'] in self.tag_set):
			self.tag_set.remove(self.insane_tag_button['text'])
			self.insane_tag_button['bg'] = self.main_button_color
		else:
			self.tag_set.add(self.insane_tag_button['text'])
			self.insane_tag_button['bg'] = self.selected_button_color


	def button_unlucky_clicked(self):
		if(self.unlucky_tag_button['text'] in self.tag_set):
			self.tag_set.remove(self.unlucky_tag_button['text'])
			self.unlucky_tag_button['bg'] = self.main_button_color
		else:
			self.tag_set.add(self.unlucky_tag_button['text'])
			self.unlucky_tag_button['bg'] = self.selected_button_color


	def button_one_deag_clicked(self):
		if(self.one_deag_tag_button['text'] in self.tag_set):
			self.tag_set.remove(self.one_deag_tag_button['text'])
			self.one_deag_tag_button['bg'] = self.main_button_color
		else:
			self.tag_set.add(self.one_deag_tag_button['text'])
			self.one_deag_tag_button['bg'] = self.selected_button_color



	def cleanTagButton(self):
		self.fun_tag_button['bg'] = self.main_button_color
		self.wtf_tag_button['bg'] = self.main_button_color
		self.monsterkill_tag_button['bg'] = self.main_button_color
		self.lucky_tag_button['bg'] = self.main_button_color
		self.roadkill_tag_button['bg'] = self.main_button_color
		self.bug_tag_button['bg'] = self.main_button_color
		self.fragmovie_tag_button['bg'] = self.main_button_color
		self.insane_tag_button['bg'] = self.main_button_color
		self.unlucky_tag_button['bg'] = self.main_button_color
		self.one_deag_tag_button['bg'] = self.main_button_color
		self.tag_set.clear()

	# --------------------------------------------------------------------------------------------------
	# SETTERS

	def setClipGrade(self, grade):
		if(grade != None):
			if(grade < 0):
				grade = 0
			if(grade > 5):
				grade = 5
			self.clip_grade_selected = grade
			index = 1
			for button in self.button_STAR_ref:
				if(index <= grade):
					button['bg'] = self.selected_button_color
					index += 1


	def setKillCounter(self, kill):
		if(kill != None):
			if(kill < 0):
				kill = 0
			if(kill > 999):
				kill = 999
			self.kill_counter = kill
			self.buttonKILLCOUNTER['text'] = str(self.kill_counter)
			if(self.kill_counter > 0):
				self.buttonKILLCOUNTER['bg'] = self.selected_button_color
			else:
				self.buttonKILLCOUNTER['bg'] = self.main_button_color


	def setClass(self, class_):
		if(class_ != None):
			self.cleanClassButton()
			if(class_ == "ASSAULT"):
				self.buttonASSAULT_clicked()
			if(class_ == "MEDIC"):
				self.buttonMEDIC_clicked()
			if(class_ == "SUPPORT"):
				self.buttonSUPPORT_clicked()
			if(class_ == "RECON"):
				self.buttonRECON_clicked()


	def setPrimaryWeapon(self, w1):
		if(w1 != None):
			for element in self.button_primary_weapon_ref:
				for button in element:
					if(button != None):
						if(button['text'] == w1):
							button['bg'] = self.selected_button_color
							self.primary_weapon_selected = w1
						else:
							button['bg'] = self.main_button_color


	def setSecondaryWeapon(self, w2):
		if(w2 != None):
			for element in self.button_secondary_weapon_ref:
				for button in element:
					if(button != None):
						if(button['text'] == w2):
							button['bg'] = self.selected_button_color
							self.secondary_weapon_selected = w2
						else:
							button['bg'] = self.main_button_color


	def setGadget1(self, g1):
		if(g1 != None):
			for button in self.button_gadget_ref[0]:
				if(button != None):
					if(button['text'] == g1):
						button['bg'] = self.selected_button_color
						self.gadget1_selected = g1
					else:
						button['bg'] = self.main_button_color


	def setGadget2(self, g2):
		if(g2 != None):
			for button in self.button_gadget_ref[1]:
				if(button != None):
					if(button['text'] == g2):
						button['bg'] = self.selected_button_color
						self.gadget2_selected = g2
					else:
						button['bg'] = self.main_button_color


	def setGadget3(self, g3):
		if(g3 != None):
			for button in self.button_gadget_ref[2]:
				if(button != None):
					if(button['text'] == g3):
						button['bg'] = self.selected_button_color
						self.gadget3_selected = g3
					else:
						button['bg'] = self.main_button_color


	def setMelee(self, melee):
		if(melee != None):
			self.cleanButtonMelee()
			self.button_melee_clicked()


	def setMap(self, map_):
		if(map_ != None):
			self.cleanMapButton()
			for button in self.map_button_ref:
				if(button['text'] == map_):
					button['bg'] = self.selected_button_color
					self.map_selected = map_


	def setCountry(self, country):
		# NOT PROTECTED MAYBE NEEDS TO BE... (WHEN SELECTING COUNTRY WITH WRONG MAP)
		if(country != None):
			self.cleanCountryButton()
			if(country == "GE"):
				self.buttonGE_clicked()
			if(country == "UK"):
				self.buttonUK_clicked()
			if(country == "JP"):
				self.buttonJP_clicked()
			if(country == "USA"):
				self.buttonUSA_clicked()


	def setVehicule(self, vehicules):
		if(vehicules != None and len(vehicules) > 0):
			for vehicule in vehicules:
				for button in self.button_vehicules_ref:
					if(button['text'] == vehicule):
						if(button['text'] in self.vehicule_selected):
							button['bg'] = self.main_button_color
							self.vehicule_selected.remove(button['text'])
						else:
							button['bg'] = self.selected_button_color
							self.vehicule_selected.add(button['text'])
					else:
						button['bg'] = self.main_button_color
						if(button['text'] in self.vehicule_selected):
							self.vehicule_selected.remove(button['text'])


	def setReinforcement(self, squad_calls):
		if(squad_calls != None and len(squad_calls) > 0):
			for button in self.button_reinforcement_ref:
				for reinforcement in squad_calls:
					if(button != None and button['text'] == reinforcement):
						if(button['bg'] == self.selected_button_color):
							button['bg'] = self.main_button_color
							self.reinforcements_selected.remove(reinforcement)
						else:
							button['bg'] = self.selected_button_color
							self.reinforcements_selected.add(reinforcement)


	def setStaticWeapon(self, static_ws):
		if(static_ws != None and len(static_ws) > 0):
			self.cleanStaticWeapon()
			for button in self.button_static_ref:
				for weapon in static_ws:
					if(button['text'] == weapon):
						if(weapon in self.static_weapon_selected):
							button['bg'] = self.main_button_color
							self.static_weapon_selected.remove(button['text'])
						else:
							button['bg'] = self.selected_button_color
							self.static_weapon_selected.add(button['text'])


	def setTags(self, tags):
		if(tags != None and len(tags) > 0):
			for button in self.tag_button_ref:
				for tag in tags:
					if(button['text'] == tag):
						button['bg'] = self.selected_button_color
						self.tag_set.add(tag)

	# --------------------------------------------------------------------------------------------------
	# CLIP SORTER FUNCTIONS
	# --------------------------------------------------------------------------------------------------

	def _on_enter_kill_counter1(self, enter):
		self.mouse_over_kill_counter1 = True

	def _on_enter_kill_counter2(self, enter):
		self.mouse_over_kill_counter2 = True


	def _on_leave_kill_counter1(self, leave):
		self.mouse_over_kill_counter1 = False

	def _on_leave_kill_counter2(self, leave):
		self.mouse_over_kill_counter2 = False


	def _on_mousewheel1(self, event):
		if(self.mouse_over_kill_counter1):
			self.kill_counter1 += int(event.delta/120)
			if(self.kill_counter1 < -1):
				self.kill_counter1 = -1
			if(self.kill_counter1 > 999):
				self.kill_counter1 = 999
			
			if(self.kill_counter1 == -1):
				self.buttonKILLCOUNTER1['text'] = "X"
			else:
				self.buttonKILLCOUNTER1['text'] = str(self.kill_counter1)
			
			if(self.kill_counter1 > 0):
				self.buttonKILLCOUNTER1['bg'] = self.selected_button_color
			else:
				self.buttonKILLCOUNTER1['bg'] = self.main_button_color
		self.minToMaxBalance()

	def _on_mousewheel2(self, event):
		if(self.mouse_over_kill_counter2):
			self.kill_counter2 += int(event.delta/120)
			if(self.kill_counter2 < -1):
				self.kill_counter2 = -1
			if(self.kill_counter2 > 999):
				self.kill_counter2 = 999

			if(self.kill_counter2 == -1):
				self.buttonKILLCOUNTER2['text'] = "X"
			else:
				self.buttonKILLCOUNTER2['text'] = str(self.kill_counter2)

			if(self.kill_counter2 > 0):
				self.buttonKILLCOUNTER2['bg'] = self.selected_button_color
			else:
				self.buttonKILLCOUNTER2['bg'] = self.main_button_color
		self.maxToMinBalance()


	def buttonMINUS_clicked1(self):
		if(self.kill_counter1 >= 0):
			self.kill_counter1 -= 1
			if(self.kill_counter1 == -1):
				self.buttonKILLCOUNTER1['text'] = "X"
			else:
				self.buttonKILLCOUNTER1['text'] = str(self.kill_counter1)
		if(self.kill_counter1 > 0):
			self.buttonKILLCOUNTER1['bg'] = self.selected_button_color
		else:
			self.buttonKILLCOUNTER1['bg'] = self.main_button_color

	def buttonMINUS_clicked2(self):
		if(self.kill_counter2 >= 0):
			self.kill_counter2 -= 1
		if(self.kill_counter2 == -1):
			self.buttonKILLCOUNTER2['text'] = "X"
		else:
			self.buttonKILLCOUNTER2['text'] = str(self.kill_counter2)
		if(self.kill_counter2 > 0):
			self.buttonKILLCOUNTER2['bg'] = self.selected_button_color
		else:
			self.buttonKILLCOUNTER2['bg'] = self.main_button_color
		self.maxToMinBalance()

	
	def buttonKILLCOUNTER_clicked1(self):
		self.kill_counter1 = 0
		self.buttonKILLCOUNTER1['text'] = str(self.kill_counter1)
		self.buttonKILLCOUNTER1['bg'] = self.main_button_color

	def buttonKILLCOUNTER_clicked2(self):
		self.kill_counter2 = 0
		self.buttonKILLCOUNTER2['text'] = str(self.kill_counter2)
		self.buttonKILLCOUNTER2['bg'] = self.main_button_color
		self.maxToMinBalance()


	def buttonPLUS_clicked1(self):
		self.kill_counter1 += 1
		self.buttonKILLCOUNTER1['text'] = str(self.kill_counter1)
		if(self.kill_counter1 > 0):
			self.buttonKILLCOUNTER1['bg'] = self.selected_button_color
		else:
			self.buttonKILLCOUNTER1['bg'] = self.main_button_color
		self.minToMaxBalance()

	def buttonPLUS_clicked2(self):
		self.kill_counter2 += 1
		self.buttonKILLCOUNTER2['text'] = str(self.kill_counter2)
		if(self.kill_counter2 > 0):
			self.buttonKILLCOUNTER2['bg'] = self.selected_button_color
		else:
			self.buttonKILLCOUNTER2['bg'] = self.main_button_color


	def updateKillCounterButton1(self):
		if(self.kill_counter1 >= 0):
			if(self.kill_counter1 > 999):
				self.kill_counter1 = 999
			if(self.kill_counter1 > 0):
				self.buttonKILLCOUNTER1['text'] = str(self.kill_counter1)
				self.buttonKILLCOUNTER1['bg'] = self.selected_button_color
			else:
				self.buttonKILLCOUNTER1['text'] = str(self.kill_counter1)
				self.buttonKILLCOUNTER1['bg'] = self.main_button_color
		else:
			self.buttonKILLCOUNTER1['text'] = "X"#str(self.kill_counter1)
			self.buttonKILLCOUNTER1['bg'] = self.main_button_color

	def updateKillCounterButton2(self):
		if(self.kill_counter2 >= 0):
			if(self.kill_counter2 > 999):
				self.kill_counter2 = 999
			if(self.kill_counter2 > 0):
				self.buttonKILLCOUNTER2['text'] = str(self.kill_counter2)
				self.buttonKILLCOUNTER2['bg'] = self.selected_button_color
			else:
				self.buttonKILLCOUNTER2['text'] = str(self.kill_counter2)
				self.buttonKILLCOUNTER2['bg'] = self.main_button_color
		else:
			self.buttonKILLCOUNTER2['text'] = "X"#str(self.kill_counter2)
			self.buttonKILLCOUNTER2['bg'] = self.main_button_color


	def cleanKillCounterButton1(self):
		self.kill_counter1 = 0
		self.buttonKILLCOUNTER1['text'] = str(self.kill_counter1)
		self.buttonKILLCOUNTER1['bg'] = self.main_button_color

	def cleanKillCounterButton2(self):
		self.kill_counter2 = 0
		self.buttonKILLCOUNTER2['text'] = str(self.kill_counter2)
		self.buttonKILLCOUNTER2['bg'] = self.main_button_color


	def minToMaxBalance(self):
		if(self.kill_counter1 > self.kill_counter2):
			self.kill_counter2 = self.kill_counter1
			self.updateKillCounterButton2()

	def maxToMinBalance(self):
		if(self.kill_counter2 < self.kill_counter1):
			self.kill_counter1 = self.kill_counter2
			self.updateKillCounterButton1()

	# --------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	app = App()
	app.root.mainloop()