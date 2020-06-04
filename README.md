# Stock Price
A simple project to get Live Stock Price of any Company that is listed on NSE(National Stock Exchange)

## Technologies Used in this Project are:

1. HTML/CSS/Javascript for Front End
2. Jquery and Ajax for talking to Back End 
3. Python, Beautiful Soup 4 and Flask for Back End

### The Flow of Project:

First of all Download all the files and save it in a folder. Open the folder on your favourite *IDE* and run the *Virtual Environment*.    
To run simple type `env\Scripts\activate.bat` in the terminal . Now that the *Virtual Environment* is running we are good to go!  

**Back End**  
Building the `core.py` file is the core part of the project. It fetches Live Price of any Stock. Basically it Webscrape from **TickerTape**.
The Web Scraping is done using a Python Library called `BeautifulSoup 4`.  

Now to host the `core.py` file and get request from *Front End* we use `FLASK`, a Web Framework. This is implemented on `app.py`.
`app.py` defines all routes of the server.
It imports the `core.py` file and handles the **POST** requests from *Front End* and returns `JSON` object file having the **current Price**.  

To run the file simply type `flask run` in the terminal.  

**Front End**  
Building a simple Interactive `HTML` page using `CSS` and `JavaScript`. It takes *Company Name* as an input and shows the **Live Price**
as output on *Click* of a Button. The Page also provides *Auto Suggestions* of *Company Names*. On *Click* of the Button, it sends 
**POST** request using `Jquery` and `AJAX`.  Using `JavaScript`, **POST** request is sent in every minute, updating the **Live Price**.

Make sure that the `Flask app` is running. Open your Browser and go to `http://127.0.0.1:5000/` to see the `home page`

**Type any Company name and Get Live Price of your favourite Stocks**
