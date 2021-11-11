copertura = []

class Persona:
    def __init__(self,ruolo, nome, cognome, eta):
        self.ruolo= ruolo
        self.nome = nome
        self.cognome = cognome
        self.eta = eta
    
    def bonjour(self):
        print(self.ruolo ,':', self.nome, self.cognome,'(anni', self.eta,')')

class Docente(Persona):
    def __init__(self,nome, cognome, corsi, eta):
        super().__init__('Docente UNITS', nome, cognome, eta)
        self.corsi = corsi
    def riempi_copertura(self):
        for item in self.corsi:
            copertura.append(item)

    def bonjour(self):
        
        if self.eta < 40:
            Persona.bonjour(self)
            print('> Docente dei corsi : ')
            for item in self.corsi:
                print(item)
                
        else:
            print(self.ruolo ,':', self.nome, self.cognome,'(anni > 40)')
            for item in self.corsi:
                print(item)
                

class Studente(Persona):
    def __init__(self, nome, cognome, corsi, eta):
        super().__init__('Studente di UNITS',nome , cognome,eta)

        self.corsi = corsi

    def bonjour(self):
        Persona.bonjour(self)
        print('> Studente dei corsi: ')
        for item in self.corsi:
            print(item,',')

class TecnicoAmministrativo(Persona):
    def __init__(self, nome, cognome, edificio, eta):
        super().__init__('Tecnico Amministrativo',nome, cognome, eta)
        self.edificio = edificio

    def bonjour(self):
        Persona.bonjour(self)
        print("> Tecnico dell'edificio ", self.edificio)

obj_LucaPernice = Studente('Luca','Pernice',['Analsi 1','Geometria 1','Programmazione','Inglese','Botanica'],19)
obj_LucaPernice.bonjour()

obj_Germano = TecnicoAmministrativo('Germano','Menoraglio','Edificio H3',45)
obj_Germano.bonjour()

obj_profAnnio = Docente('Annio','Spadafora',['Analsi 1','Geometria 1','Programmazione'],42)
obj_profAnnio.bonjour()

obj_profCannamibio = Docente('Gianfranco', 'Cannamibio',['Inglese'],12)

def copertura_totale(lista_di_docenti, studente):
    for item in copertura:
        copertura.remove(item)
    for item in lista_di_docenti:
        item.riempi_copertura()
    print('Ricerca copertura per lo studente ',studente.nome)
    i = 0
    e = 0
    while i<len(studente.corsi):
        if studente.corsi[i] not in copertura:
            print('Non e coperto per ',studente.corsi[i])
        else:
            e += 1
        i+=1 
    if e == len(studente.corsi):
        print('Lo studente ',studente.nome,'e coperto in tutte le materie')
    


copertura_totale([obj_profAnnio,obj_profCannamibio],obj_LucaPernice)
copertura_totale([obj_profAnnio],obj_LucaPernice)

print('------------------------------------')
print(copertura)
print('------------------------------------')
for i, item in enumerate(copertura):
    print('Removing #{} "{}"'.format(i, item))
    copertura.remove(item)
    print(copertura)
print('------------------------------------')
print (copertura)
print('------------------------------------')


# Non usare accentate, specialmente nelle variabili o negli oggetti. ASCII standard
# push ce non va a quei due
#  fine cose nuove (quasi)
# che tutti abbiano capito CSVFile
# isintance (per sanitizzazone)
# numero linee nel CSVFile
# anomalia con la media
# previsione con la differenza fra gli ultimi due punti (non serve il fit!) --> ipotesi del modello, scritta come commento
# command line arguments ( e che non usino input())
#Valutazioen modello: aggiungeremo i dizionari







