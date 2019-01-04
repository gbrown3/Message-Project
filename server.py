"""
Written by Gabriel Brown
"""
# Base Python libraries
import json
import time

# Flask and server libraries
from flask import Flask, render_template, make_response, request

# My classes
from supporting_classes.message import Message
from supporting_classes.guest import Guest
from supporting_classes.reservation import Reservation
from supporting_classes.company import Company

app = Flask(__name__)


guests = []
companies = []
templates = [] # Each template is an ordered list of message parts, with variables as seperate elements in the list
# TODO: explain my template system better somewhere


# Load in Guest and reservation data

with open("./json/Guests.json") as json_file:

    guest_res_data = json.load(json_file)

    for guest_object in guest_res_data:

        # Generate the reservation object
        roomNumber = guest_object["reservation"]["roomNumber"]
        startTime = guest_object["reservation"]["startTimestamp"]
        endTime = guest_object["reservation"]["endTimestamp"]

        reservation = Reservation(roomNumber, startTime, endTime)

        # Generate the guest object
        ID = guest_object["id"]
        firstName = guest_object["firstName"]
        lastName = guest_object["lastName"]

        guest = Guest(ID, firstName, lastName, reservation)
        guests.append(guest)


for guest in guests:

    print(guest)



# Load in Company data

with open("./json/Companies.json") as json_file:

    company_data = json.load(json_file)

    for company_obj in company_data:

        ID = company_obj["id"]
        name = company_obj["company"]
        city = company_obj["city"]
        timezone = company_obj["timezone"]

        company = Company(ID, name, city, timezone)
        companies.append(company)

for company in companies:

    print(company)



# Load in Template data
with open("./json/Templates.json") as json_file:

    template_data = json.load(json_file)

    for template in template_data:

        templates.append(template["template"])  # TODO: revisit this and decide whether each template needs an id or not

for template in templates:

    print(template)



# Routes
@app.route("/")
def index():

    Message.greeting = determine_greeting()

    # Make a sample message
    message = Message(templates[0], guests[0], companies[0])
    print(message.message)

    return app.send_static_file("index.html")
    #return render_template("index.html")


# Other methods

# TODO: it would be cool to let this take in a local time as well,
# so that users connecting to the server from different time zones
# could pass in their local time and still get an appropriate greeting,
# not just a greeting appropriate to wherever the server is located
def determine_greeting():
    """
    Return string representing a greeting that is appropriate for the current time and timezone, i.e.
    Good morning, Good afternoon, Good evening
    """
    localtime = time.localtime(time.time())
    hour = localtime[3]

    if hour >= 5 and hour < 12:

        return "Good morning"

    elif hour >= 12 and hour < 5:

        return "Good afternoon"

    else:

        return "Good evening"




if __name__ == "__main__":
    # debug mode makes changes instantly visible
    app.run(debug=True)



















