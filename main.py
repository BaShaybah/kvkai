from kvdesign.tools.hotreloader import App


class Main(App):
	CLASSES    = [
		"UISwitch",
		"UIButton",
		"UITouchRipple",
	]

	main_folder = "Collection"
	KVROOT      = "kvroot.kv"
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.icon = "assets/img/uik_logo.png"

	

if __name__ == "__main__":
	Main().run()
	
