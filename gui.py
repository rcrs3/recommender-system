from appJar import gui

movie_entry = "Movies:"
search_btn = "search_btn"
message_lbl = "message_lbl"
app = gui("Recommendation System")
movie_list = ["Spider Man", "Iron Man", "Iron Maiden"]

def getEntry(btn):
	movie = app.getEntry(movie_entry)
	if movie in movie_list:
		app.setMessage(message_lbl, "")
	else:
		app.setMessage(message_lbl, "This movie isn't in our database")
	print movie

def main():
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