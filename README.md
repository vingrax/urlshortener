# urlshortener
Django Token based website for url shortening

Install required packages:
pip install -r requirements.txt

Run migrations:
python manage.py migrate

Start the development server:
python manage.py runserver

Navigate to this link:
http://localhost:8000/
This is currently set to redirect to the login page 

# Creating a User

In the register form Enter any username and password

Up on sucessfull creation you will be able to login to the url shortener and retrieval page.

# URL APIs
Enter any text into the Create Shortened Input
Site will return a link to the original website u provided

Enter the same shortened link to retrieve link and you will receive the original link.

# Note 
Current only the html pages themseleves do not require authentication.
The shorten and retrieve API endpoints specified in the JS scripts is where decorators are used
