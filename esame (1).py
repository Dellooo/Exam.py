from datetime import datetime

class ExamException(Exception):
    pass

# classe CSVFile fatta in classe per memorizzare e leggere i dati da un file CSV

class CSVFile:

    def __init__(self, name):
        # set nome file come da richiesta
        self.name = name

    def get_data(self):
        #  lista vuota per salvare tutti i dati
        data = []
        #try open file
        try:
            with open(self.name,'r') as mio_file:
                # ciclo for per leggere linea per linea
                for line in mio_file:
                    # utilizzo strip() per rimuovere spazi 
                    #splitto ogni linea sulla virgola
                    line = line.strip().split(',')
                    data.append(line)
        
        except Exception as e:
            raise ExamException('Errore nella lettura del file: "{}"'.format(e))

        #numero di colonne ignorando l'intestazione (riguarda attentamente la lezione/esercitazione)
        colonne = len(data[0]) 
        #creo nuova lista dove metterò mumero preciso di colonne per riga 
        new_lines = []
        for line in data:
            new_lines.append(line[:colonne])
        
        return new_lines

#NUOVA CLASSE !!!!!!FONDAMENTALE!!!!!! CHE DEVE RICHIAMARE CLASSE CSVFile VISTA A LEZIONE!
class CSVTimeSeriesFile(CSVFile):

    def __init__(self, name):
        super().__init__(name)
    # converto le date ed il numero di passeggeri 
    #rimuovo le righe che hanno problemi
    def _conversion_data(self, data):
        # separo l'intestazione per evitare problemi in seguito
        header = data[0]
        data = data[1:]
        # controllo il formato dei dati e lo converto
        converted_data = []
        for line in data:
            converted_line = self._check_line(line)
            converted_data.append(converted_line)
        # creo una nuova lista dove appendo solo le righe che rispettano la condizione---> lista non vuota
        perfect_data = []
        for line in converted_data:
            if line:
                perfect_data.append(line)
        # rimetto l'intestazione ai dati per evitare problemi
        perfect_data = [header] + perfect_data
        data = perfect_data
        #ritorno data . lista associata alla perfect list
        return data

    # controllo e converto i valori riga per riga
    def _check_line(self,line):
        new_line = line
        try:
            #provo a trasformare il primo elemento in un datetime
            date = datetime.strptime(line[0], '%Y-%m')
            # assegno a valore il valore del secondo elemento intero 
            valore = int(line[1])
            #possibile errore se valore è negativo
            if valore < 0:
                raise ValueError
            #numero passeggeri non intero????
            if float(line[1]) - valore != 0:
                raise ValueError
            # assegno a new_line una lista con i nuovi elementi 'valore e date'
            new_line = [date, valore]
        #prendo tutte le possibili eccezioni 
        #assegno a 'new_Line' una lista vuota
        except ValueError:
            new_line = []
        
        return new_line
        
    def _check_dates(self, dates):
        # controllo che non ci siano date duplicate usando set() che unisce
        if len(set(dates)) != len(dates):
            raise ExamException('Errore: ci sono date duplicate')
        # controllo se le date sono ordinate
        for i in range(len(dates)-1):
            if dates[i] > dates[i+1]:
                raise ExamException('Errore: le date non sono ordinate')
        
        return dates

    def get_data(self):
        #richiamo il metodo get_data della classe genitore 
        data = super().get_data()

        # trasformo i valori nella lista 'data' con il metodo scritto precedentemente conversion_data
        data = self._conversion_data(data)

        # creo una lista dove salvo solo la prima colonna , no intestazione
        dates = []
        for line in data[1:]: # salto intestazione
            dates.append(line[0])
        # controllo delle date
        dates = self._check_dates(dates)

        # ritorno la lista 'data'
        return data

# metodo esterno per calcolare la variazione media del 
# numero di passeggeri per ogni mese  
def compute_avg_monthly_difference(time_series, first_year, last_year):
    # provo a convertire 
    try:
        first_year = int(first_year)
        last_year =  int(last_year)
    except ValueError:
        raise ExamException('Errore: anno in formato non valido')
    # gli anni devono essere positivi
    if first_year < 0 or last_year < 0:
        raise ExamException('Errore: anno non positivo')
    # 'first_year' deve essere inferiore a 'last_year'
    if first_year > last_year:
        raise ExamException('Errore: anni in ordine non valido')
    # converto la lista di liste in un dizionario dove la chiave è la data eD il valore è il numero di passeggeri
    dictionary_time_series = {}
    for line in time_series[1:]: 
        # salto l'intestazione
        date = line[0]
        value = line[1]
        dictionary_time_series[date] = value

    # creo il sottoinsieme del dizionario 
    time_series_subset = {}
    for key in dictionary_time_series:
        if first_year <= key.year <= last_year:
            time_series_subset[key] = dictionary_time_series[key]

    # creo un altro dizionario di 12 elementi, dove la chiave è il mese ed il valore è una lista contenente il numero di passeggeri di ogni anno per quel mese
    months = {}
    for i in range(1,13):
        months[i] = []
    # ciclo sulle chiavi del dizionario sottoinsieme
    #estraggo il mese dalla chiave 
    # utilizzando key.month assegno il risultato a month
    #accedo alla lista corrispondente al mese all'interno del dizionario 'months' e appendo 'value' (valore 
    # associato a key nel dizionario time_series_subset) alla lista del mese corrispondente 
    # in 'months'
    for key in time_series_subset:
        month = key.month
        value = time_series_subset[key]
        months[month].append(value)
    
    # CALCOLO LA DIFFERENZA MEDIA PER OGNI MESE
    def media(months):
        #come da consegna per l'esame se la lista dei valori per ogni mese è vuota oppure ho un solo valore , devo ritornare 0
        if len(months) <= 1:
            return 0
        #sennò bisogna calcolare la media tra ultimo e primo valore
        else:
            return (months[-1] - months[0] )/(len(months)-1)

    # creo una lista vuota per salvare le medie dei valori per ogni mese
    months_medie = []
    # ciclo sui valori del dizionario 'months' e calcolo la differenza media per ogni mese 
    for value in months.values():
        months_medie.append(media(value))

    #ritorno la lista conclusa 
    return months_medie

##################################################################################
######ESEMPIO DI OUTPUT E CONFRONTA RISULTATI RISPETTO A QUELLI FATTI A MANO######
##################################################################################
###################FAI TEST SALVANDO DATA.CSV CAMBIANDO I DATI IN ERRORI E PROVA A VEDERE SE HAI ALZATO LE ECCEZZIONI GIUSTE#########################

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series=time_series_file.get_data()
print(time_series)
differenza_media=compute_avg_monthly_difference(time_series,1949,1960)
print(differenza_media)


#########################################
#######TEST CON DATASBAGLIATA.CSV########
#differenza_media=compute_avg_monthly_difference(time_series,-100,1951)
#print(differenza_media)
#time_series_file = CSVTimeSeriesFile(name='data sbagliata.csv')
#time_series=time_series_file.get_data()
#differenza_media=compute_avg_monthly_difference(time_series,1949,1950)
#print(differenza_media)