#init.py is de dunder van onze app. 
#als de app 'opstart' is dit het bestand wat aangeroepen wordt.

#in deze regel importeren we de module flask
from flask import Flask


#in deze regel defineren we app als een instantie van de Flask-klasse.
app=Flask(__name__)

#Door de regel app = Flask(__name__) te schrijven, maken we een nieuwe -
# instantie van de Flask-klasse aan en slaan we deze op in de variabele app. 
# Deze instantie wordt gebruikt om onze Flask-applicatie te configureren en te runnen. 
# De parameter __name__ geeft aan dat we de huidige module (init.py) -
# als de naam van de applicatie gebruiken. Dit is belangrijk omdat Flask -
# verschillende paden en locaties zal gebruiken op basis van de naam van de module waarin het wordt uitgevoerd.



# Hier importeren we de "views" module van onze app
from app import views



# Door het importeren van de "views" module -
# zorgen we ervoor dat de routes en views in dat bestand -
# worden uitgevoerd wanneer de app wordt opgestart. 
# Dit stelt ons in staat om de juiste routes en functionaliteit aan de app toe te voegen.
