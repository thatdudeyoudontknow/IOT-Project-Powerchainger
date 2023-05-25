from app import app

if __name__=='__main__':
# Als dit bestand direct wordt uitgevoerd (d.w.z. als het de "hoofdmodule" is),
# dan starten we de Flask-applicatie door de run()-methode van app aan te roepen.
# De debug=True-parameter zorgt ervoor dat de app in de debug-modus wordt uitgevoerd.
    app.run(debug=True)


#In deze code wordt de app-instantie geïmporteerd vanuit het app-bestand. 
# Als dit bestand rechtstreeks wordt uitgevoerd (d.w.z. als het de "hoofdmodule" is), 
# wordt de run()-methode van app aangeroepen om de Flask-applicatie te starten. 
# De debug=True-parameter zorgt ervoor dat de app wordt uitgevoerd in de debug-modus, 
# wat handig kan zijn tijdens het ontwikkelen en testen van de app.