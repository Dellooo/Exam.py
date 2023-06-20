import csv
class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    def __init__(self,name):
        self.name=data.csv

def get_data(self):
    try:
        file=open(self.name,'r') #apro il file in modalità lettura
        data=[] #lista di liste per i dati
        for line in file:
            line=line.strip() #rimuovo caratteri di spaziatura
            if line: #se la riga non è vuota
                values=line.split(',') #divido la riga in base alla virgola
                if len(values)==2:
                    try:
                        data=str(values[0]) #data come stringa
                        passengers=int(values[1]) #numero di passeggeri come intero
                        data.append([date,passengers]) #aggiungo i dati alla lista
                    except ValueError: #tolgo errore se il numero di passeggeri non è un intero
                        continue #vado alla riga dopo
                else:
                    continue
        file.close()
        return data
    except FileNotFoundError:
        raise ExamException('Errore,file non trovato')
    except Exception as e:
        raise ExamException('errore lettura file')

def compute_avg_monthly_difference(time_series,first_year,last_year):
    try:
        min_year=int(first_year)
        max_year=int(last_year)
    except ValueError:
        raise ExamException('Errore, estremi intervallo non numerici')
    if min_year > max_year:
        raise ExamException('errore scelta anni per intervallo')

selected_data=[]
for date,passegeners in time_series:
    year=int(date.split('-')[0])
    if year>= min_year and year <= max_year:
        selected_data.append([date,passengers])

monthly_differences = [0] * 12 #lista per la differenza media mensile
if len(Selected_data) > 2: #check che ci siano almeno 3 anni di dati 
    for i in range(len(selected_data)-2): #ciclo svolto su tutti i dati tranne l'ultimo
        current_month=int(selected_data[i][0].split('-')[1]) #mese anno corrente
        next_month = int(selected_data[i+1][0].split('-')[1]) # mese anno successivo
        difference = selected_data[i+1][1] - selected_data[i][1] # calcolo la differenza tra i passeggeri dei due anni
        monthly_differences[current_month-1] += difference # incremento la differenza media mensile
            
        num_years = max_year - min_year + 1 # numero di anni nell'intervallo
        monthly_differences = [diff / num_years for diff in monthly_differences] # calcolo la differenza media mensile
        return monthly_differences




    



                    
        