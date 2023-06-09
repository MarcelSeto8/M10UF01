#!/usr/bin/python
import requests
import time
from fabulous import utils, image
from textual.app import App, ComposeResult
from textual.widgets import Label, Button
from textual import events
import webbrowser
global list_perritos
list_perritos = []

class Cachorreria(App):
	
	CSS_PATH = "style.css"
		
	def compose(self) -> ComposeResult:
		self.close_button = Button("Exit", id = "close")
		self.list_dogs = Button("List Dogs", id = "list_dogs")
		self.next_dog = Button("Next Dog", id = "next_dog")
		self.list_dogs_empty = Label("", id = "empty_dogs")
		self.vaciar_list_dogs = Button("Vacia Lista", id = "vaciar_list")

		yield Label("Bienvenida a la tierna app de cachorritos", id="title")
		yield self.list_dogs
		yield self.vaciar_list_dogs
		yield self.list_dogs_empty
		yield self.next_dog
		yield self.close_button
		

	def listRaces(self):
		api_url = "https://dog.ceo/api/breeds/list/all"

		response = requests.get(api_url)
		info_perro = (response.json())

		perro = info_perro['message']
		for p in perro:
			list_perritos.append(p)

		
	def randomPerrito(self):
		api_url = "https://dog.ceo/api/breeds/image/random"

		response = requests.get(api_url)

		if response.status_code == 200:
			info_perro = (response.json())
			perro = info_perro['message']

			images = requests.get(perro).content
			image_name = "perrito.png"

			with open(image_name, "wb") as handler:
				handler.write(images)
				img = image.Image(image_name)
				webbrowser.open(image_name)


	def on_mount(self) -> None:
		self.screen.styles.background = "darkblue"
		self.close_button.styles.background = "red"


	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "list_dogs":
			self.listRaces()
			#game_dogs_list = ", ".join(list_perritos)
			num_dogs = len(list_perritos)
			dog_chunks = [list_perritos[i:i+5] for i in range(0, num_dogs, 5)]
			formatted_dogs = "\n".join(", ".join(chunk) for chunk in dog_chunks)

			self.list_dogs_empty.update("Lista de perros:\n "+str(formatted_dogs))
		
		if event.button.id == "vaciar_list":
			self.list_dogs_empty.update("")
		
		if event.button.id == "next_dog":
			self.randomPerrito()

		if event.button.id == "close":
			self.exit(event.button.id)

if __name__ == "__main__":
	app = Cachorreria()
	app.run()
