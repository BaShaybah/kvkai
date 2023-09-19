"""
#################################################################
#                                                               #
#  Author   :  kahlid babiker                                   #
#  Email    :  khalidbabiker422@gamil.com                       #
#  github   :  github.com/kwargsman                             #
#  fb       :  Kindo kwargsman                                  #
#                                                               #
#                                                               #
#                                                               #
#                                                               #
#                                                               #
#                                                               #
#                                                               #
#################################################################
"""

__author__ = "kwargsman"

from kivy.app import App as Base

from kivy.lang import Builder
from kivy.logger import Logger
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty, ListProperty

import os
from os.path import join
import sys
import importlib

class BaseDB(dict):
	def __init__(self, data=None):
		""" init """
	
	def __setattr__(self, name, value):
		self[name] = value
	
	def __getattr__(self, name):
		return self[name]
		

class App(Base):

	CLASSES = ListProperty([
		"MainScreen",
	])

	supported_files = ListProperty(["py", "kv"])
	main_folder = StringProperty("Collection")
	KVROOT = StringProperty("")
	_KVROOT = StringProperty("")

	init_argv = sys.argv

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.sys_slash  = "\\" if sys.platform == "win32" else "/"
		self.env_name   = str(os.getcwd()).split(self.sys_slash)[-1]
		self.main_db    = BaseDB()

		self._KVROOT    = join(os.getcwd(), self.main_folder, self.KVROOT)


	def build(self):
		self.app_run    = self.get_running_app()
		self.approot    = None
		self.root       = Factory.RelativeLayout()

		return super().build()
	
	def on_start(self):
		self.title = self.env_name
		
		self.hot_start()
		Window.bind(on_keyboard=self.keys_down)
		Clock.schedule_interval(self.update,1/60)
			
		return super().on_start()
		
	def hot_start(self):
		try:
			for path, dir, lfile in os.walk(join(os.getcwd(), self.main_folder)) :
				for mfile in lfile:
					file = join(path, mfile)

					if file.endswith(".py"):
						imp = str(file).split(self.env_name)[1].replace(self.sys_slash, ".")
						imp = imp.lstrip(".").rstrip(".py")

						for cls in self.CLASSES:		
							if cls.lower() == imp.split(".")[-1]:
								exec(f"import {imp}")
								importlib.reload(eval(f"{imp}"))
								exec(f"from {self.main_folder}.{cls.lower()}.{cls.lower()} import {cls}")

					elif file.endswith(".kv") and file != self._KVROOT:
						Builder.load_file(file)

			self.rebuild()
			Logger.info(f"{self.title}: app start")	

		except Exception as e:
			self.error_view(e)


	@mainthread
	def update(self, *args):
		try:
			for path, dir, lfile in os.walk(join(os.getcwd(), self.main_folder)) :
				for mfile in lfile:
					file = join(path, mfile)
					value = self.main_db.__getattr__(join(path,file))

					with open(join(path, file)) as txtfile:
						text = txtfile.read()
						txtfile.close()
					if value != text:
					
						self.app_reloader(join(path,file))
						self.main_db.__setattr__(join(path,file), open(os.path.join(path,file),"r").read())
		
		except Exception as e:
			self.main_db.__setattr__(join(path,file), open(os.path.join(path,file),"r").read())
		

	def app_reloader(self, file):
		try:

			if file.endswith(".py"):
				imp = str(file).split(self.env_name)[1].replace(self.sys_slash, ".")
				imp = imp.lstrip(".").rstrip(".py")
				for cls in self.CLASSES:		
					if cls.lower() == imp.split(".")[-1]:

						exec(f"import {imp}")
						importlib.reload(eval(f"{imp}"))
						exec(f"from {self.main_folder}.{cls.lower()}.{cls.lower()} import {cls}")

						Factory.unregister(f"{cls}")
						Factory.register(f"{cls}", eval(f"{cls}"))

			elif file.endswith(".kv") and file != self._KVROOT:
				Builder.unload_file(file)
				Builder.load_file(file)
	
			self.rebuild()
			
		except Exception as e:
			self.error_view(e)
		

	def error_view(self, txt = ""):
		Logger.error(txt)
		
		self.approot = Factory.BoxLayout(padding=15)
		lbl = Factory.Label(text=str(txt), theme_text_color="Error",halign="left")
		self.approot.add_widget(lbl)

		self.root.clear_widgets()
		self.root.add_widget(self.approot)


	def rebuild(self, *args):
		try:
			#self.approot = self.build_app()

			Builder.unload_file(self._KVROOT)
			self.approot = Builder.load_file(self._KVROOT)

			self.root.clear_widgets()
			self.root.add_widget(self.approot)
			Logger.info(f"{self.title} : app reloaded")
			
		except Exception as e:
			self.error_view(e)



	def keys_down(self, *args):
		if args[1] == 286:
			self._restarting()	


	def _restarting(self):
		_has_execv = sys.platform != "win32"
		cmd = [sys.executable] + self.init_argv
		if not _has_execv:
			import subprocess

			subprocess.Popen(cmd)
			sys.exit(0)
		else:
			try:
				os.execv(sys.executable, cmd)
			except OSError:
				os.spawnv(os.P_NOWAIT, sys.executable, cmd)
				os._exit(0)

	


		






		
		
		
		
		
		
