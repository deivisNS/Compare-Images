import numpy
import cv2


class Compare():

	def __init__(self, images):

		"""abrimos las dos imagenes y siguiente indicamos como se leera:
		1 es para leerla en cv2.IMREAD_COLOR que lee la imagen a color pero ignorando la transparencia.
		2 es para leerla en cv2.IMREAD_GRAYSCALE que la lee con escalas de grises.
		3 es para leerla en cv2.IMREAD_UNCHANGED que la lee con todo y su transparencia."""
		self.img_1 = cv2.imread(images[0], 1)

		self.img_2 = cv2.imread(images[1], 1)

		"""obtenemos el ancho y largo de las imagenes al igual que el canal que tienen (el canal es si
		la imagen tienen transparencia, solo a color o esta en escala de grises)"""
		self.size_1 = self.img_1.shape

		self.size_2 = self.img_2.shape

		self.message = f"El tamaño y canal de la primera imagen es {self.size_1[1]}x{self.size_1[0]} y su canal es {self.size_1[2]}.\n"

		self.message += f"El tamaño y canal de la segunda imagen es {self.size_2[1]}x{self.size_2[0]} y su canal es {self.size_2[2]}.\n"


	def check(self, change = False):

		if self.size_1 == self.size_2:

			self.message += "Tienen el mismo tamaño y el mismo canal.\n"

		else:

			self.message += "El tamaño o canal es diferente.\n"

			if change == True:
				
				"""cambiamos el tamaño de unas de las imagenes, ingresando la imagen a modificar, seguido
				de una tupla con el alto y ancho"""
				self.img_2 = cv2.resize(self.img_2, (self.size_1[1], self.size_1[0]))

				self.message += "Se ha cambiado el tamaño de la segunda imagen para poder continuar con la comparacion.\n"


	def process_comparison(self):
		
		try:

			"""crea dos matices de las imagenes para poder comparar cada px y notar si a travez de esa
			comparacion de px hay diferencias"""
			differences = cv2.absdiff(self.img_1, self.img_2)

			"""obtenemos cuantos px fueron diferentes, ejemplo: si devuelve un 0.0 es que no hubo diferencias,
			pero si devuelve otro valor como un 2.0 es que hubo un 2% de diferencias al comparar los px"""
			diff_left = numpy.mean(differences)

			"""cambiamos el resultado de la comparacion de imagenes a escala de grises"""
			find_diff = cv2.cvtColor(differences, cv2.COLOR_BGR2GRAY)

			"""creamos una mascara con umbral (es dificil explicar los parametros pero sirve para crear una
			mascara negra donde se denotan las diferencias)"""
			ret, mask = cv2.threshold(find_diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

			"""tomamos el resultado de la comparacion y le colocamos la mascara [mask != 0] (si no hay 
			diferencias entonces la mascara sera totalmente negra) seguido indicamos de que color se mostraran
			las diferencias [0, 255, 0]( el primer numero es azul, el segundo es verde y el ultimo es rojo.
			asi que estamos indicando que queremos las diferencias en verde)"""
			differences[mask != 255] = [0, 255, 0]

			self.message += f"Pixeles de diferencias: {diff_left}\n"

			if diff_left > 1:

				self.message += "Se han encontrado diferencias.\n"

				if diff_left > 1 and 3 >= diff_left:

					self.message += "Las diferencias son minimas. Puede que sea por que alguna imagen tiene distinto tamaño,\npor tener alguna frase corta y de poco tamaño en el o por que tenga alguna mancha.\n"

				if diff_left > 3 and 7 >= diff_left:

					self.message += "Las diferencias pueden ser evidentes en la imagen. Puede que sea por que alguna imagen tiene distinto tamaño y haya algo que no esta en la otra.\n"

				if diff_left > 7:

					self.message += "Las diferencias son muchas. Nada mas que comentar *_*\n"

			else:

				self.message += "Las images son iguales.\n" 

			"""mostramos las imagenes"""
			cv2.imshow("img_1", self.img_1)

			cv2.imshow("img_2", self.img_2)

			cv2.imshow("diff", differences)

			"""guardamos la imagen con las diferencias"""
			cv2.imwrite("./difference/image_diff.jpg", differences)

			"""para cerrar la o las ventanas de imagenes. si esta en 0 es para que se puedan cerrar al presionar
			una letra, si es mayor a 0 entonces se cerrar en esa cantidad de tiempo pero lo hace a travez de 
			milisegundos (si quieres 4 segundos entonces seria 4000)"""
			cv2.waitKey(0)
			
			"""destruye todas las ventanas"""	
			cv2.destroyAllWindows()

		except:

			self.message += "Ha ocurrido algo, tal vez las imagenes tienen distintos canales o distintos tamaños,\npor favor usa el metodo check de la clase para verificar y tambien puedes habilitar el\nparametro change a True para que una de las imagenes se adapte a la otra y asi poder\ncompararla.\n Ejemplo: img.check(change = True)"

		finally:

			with open("./difference/info.txt", "w") as info:

				info.write(self.message)
				

img = Compare(["2.jpg", "into_imagen.jpg"])

img.check(change = True)

img.process_comparison()
