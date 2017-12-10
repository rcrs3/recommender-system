from appJar import gui
import numpy as np
#import dataprocess


movie_entry = "Movies:"
search_btn = "search_btn"
message_lbl = "message_lbl"
app = gui("Recommendation System")
#movie_list = np.array([])
movie_list = ["Iron Man"]


def subwindow():	
	#Subwindow Configuration
	subwindow_title = "Recommended Movies"
	movies_list_lbl = "movies_list"
	app.startSubWindow(subwindow_title, modal=True)
	app.setGeometry("400x400")
	app.addEmptyMessage(movies_list_lbl)
	app.setMessage(movies_list_lbl, "oi")
	app.showSubWindow(subwindow_title)
	app.destroySubWindow()


def getMoviesText(movies):
	msg = ""
	for i in range(0, len(movies)):
		msg.append(movies + "\n")
	return msg
	


def getEntry(btn):
	movie = app.getEntry(movie_entry)
	if movie in movie_list:
		app.setMessage(message_lbl, "")
		subwindow()
	else:
		app.setMessage(message_lbl, "This movie isn't in our database")
	print movie


def main():
	#global movie_list
	#movie_list = np.append(movie_list,dataprocess.get_movies())
	startGUI()

def startGUI():
	#Basic GUI Configuration
	app.setGeometry("500x200")
	app.setLocation("CENTER")

	#Labels Configuration
	app.addLabelAutoEntry(movie_entry, movie_list)
	app.setEntryDefault(movie_entry, "Enter a movie here...")

	#Button Configuration
	app.addNamedButton("Search", search_btn, getEntry)

	#Message Configuration
	app.addEmptyMessage(message_lbl)

	app.go()


if __name__ == '__main__':
	main()
