
# from timeseria.time import dt
# item_count = 0
# tot_count  = 0
# for item in temperature_timeseries.filter(from_dt=dt(2019,4,1), to_dt=dt(2019,5,1)):
#     if item.data_loss == 0:
#         print('{},{:.2f}'.format(int(item.t), item.data['temperature']))
#         item_count+=1
#     tot_count+=1
# print(tot_count)
# print(item_count)


class ExamException(Exception):
    pass

class CSVTimeSeriesFile:

    def __init__(self, name):

        # Se il nome non e' una stringa, genero un errore e torno nel main
        if not isinstance(name, str):
            raise ExamException('Errore: il parametro "name" deve essere una stringa, non "{}"'.format(type(name)))

        # Setto il nome del file
        self.name = name

    # I parametri start e end sono None se l'utente non inserisce nulla (default)
    def get_data(self):

        # Inizializzo una lista vuota per salvare i valori
        values = []

        # Provo ad aprire il file per estrarci i dati. Se non ci riesco, prima avverto del'errore,
        # poi devo abortire. Questo e' un errore "un-recoverable", ovvero non posso proseguire con
        # la lettura dei dati se non riesco ad aprire il file!
        try:
            my_file = open(self.name, 'r')
        except Exception as e:
            
            # Ri-alzo l'errore come ExamException
            raise ExamException('Errore nella lettura del file: "{}"'.format(e))

        # Se riesco ad aprire il file, lo leggo linea per linea
        for line in my_file:

            # Faccio lo split di ogni linea sulla virgola
            elements = line.split(',')

            # Se NON sto processando l'intestazione...
            if elements[0] != 'epoch':
                
                # Setto l'epoch ed il valore
                try:
                    epoch = elements[0]
                    value = elements[1]
                except:
                    continue
                
                # Controllo che l'epoch sia un valore che posso interpretare come intero *arrotondandolo*:
                try:
                    epoch = round(float(epoch))
                except Exception as e:

                    # Stampo l'errore se voglio (i.e. per il debugging)
                    #print('Errore nela conversione dell\'epoch a int: "{}"'.format(e))

                    # Vado al prossimo "giro" del ciclo, quindi NON eseguo quanto viene dopo (ovvero l'append)
                    continue

                # Controllo che la temperatura sia un valore che posso interpretare come floating point:
                try:
                    value = float(value)
                except Exception as e:
                        
                    # Stampo l'errore
                    print('Errore nela conversione della temperatura a floating point: "{}"'.format(e))
                        
                    # Vado al prossimo "giro" del ciclo, quindi NON eseguo quanto viene dopo (ovvero l'append)
                    continue
                
                # Controllo che il timestamp sia successivo al precedente e che non sia un duplicato
                if len(values) > 0:
                    prev_epoch = values[-1][0]
                    if epoch <= prev_epoch:
                        raise ExamException('Timestamp non in ordine o duplicato.')
                
                # Infine aggiungo alla lista principale la lista annidata contenente l'epoch ed il valore
                values.append([epoch,value])
        
        # Chiudo il file
        my_file.close()

        # Quando ho processato tutte le righe ed eventualmente le ho
        # filtrate in base all'intervallo richiesto, ritorno i valori.
        
        # Posso voler alzare una eccezione.. le specifiche none rano chiare, va bene tutto.
        #if not values:
        #    raise ExamException('File vuoto')
        
        return values


def hourly_trend_changes(time_series):
    
    # Lista in cui salvero' i risultati
    results = []
    
    # Variabili di supporto
    count = 0
    hourly_changes = 0
    prev_item = None
    ongoing_trend = None
    
    # Inizio a processare le temperature orarie
    for item in time_series:

        # Incremento il contatore di elementi della serie temporale processati
        count = count + 1
        
        # Imposto due variabile che mi semplificano la vita
        item_epoch = item[0]
        item_value = item[1]

        # Se non ho un'elemento precedente, non posso avere cambi.
        # Setto il nuovo prev e vado all'elemento successivo
        if not prev_item:
            prev_item = item
            continue

        # Per semplificare...        
        prev_item_epoch = prev_item[0]
        prev_item_value = prev_item[1]

        # Ho cambiato ora?
        if int(prev_item_epoch / 3600) != int(item_epoch / 3600):
            
            # No, aggiungo il risultato alla lista dei risultati
            results.append(hourly_changes)
            
            # Resetto 
            hourly_changes = 0
            
        # Non ho ancora mai rilevato un trend? Non posso fare i confronti..
        if ongoing_trend is None:
            # setto il trend ongoing
            if (item_value - prev_item_value) > 0: 
                ongoing_trend = +1
            elif (item_value - prev_item_value) < 0: 
                ongoing_trend = -1
            else:
                ongoing_trend = 0
            continue
        else:
            # Setto il trend corrente
            if (item_value - prev_item_value) > 0: 
                current_trend = +1
            elif (item_value - prev_item_value) < 0: 
                current_trend = -1
            else:
                current_trend = 0
            
            # Confronto i trend ongoing e corrente ed agisco di conseguenze 
            if current_trend != ongoing_trend:
                hourly_changes += 1
                ongoing_trend = current_trend  
        
        # Set prev
        prev_item= item         

    # Aggiungo l'ultimo conteggio del trend
    results.append(hourly_changes)

    # Finito il ciclo su tutti gli elementi della serie temporale, ritorno i risultati
    return results


#==============================
# Main
#==============================

#time_series_file = CSVTimeSeriesFile(name='data.csv')
 
#time_series = time_series_file.get_data()
 
#results = hourly_trend_changes(time_series)
 
#print(results)            

#==============================
# Test  
#==============================
 
 
import unittest
import tempfile
import warnings


 
score = 0
 
class TestAndGrade(unittest.TestCase):

    # Roba per il testing
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)


    #===========================================================
    # Test per il 18: tre ore di dati, tutti i dati presenti.
    #===========================================================

    def test_correctness(self):
        
        with tempfile.NamedTemporaryFile('w+t') as file:
            
            file.write('epoch,temperature\n')

            # Prima ora
            file.write('3600,21\n')     
            file.write('4200,22\n')
            file.write('4800,23\n')
            file.write('5400,22\n')
            file.write('6000,21\n')
            file.write('6600,20\n')

            # Seconda ora
            file.write('7200,19\n')
            file.write('7800,18\n')
            file.write('8400,17\n')
            file.write('9000,16\n')
            file.write('9600,17\n')
            file.write('10200,18\n')
            
            # Terza ora
            file.write('10800,20\n')
            file.write('11400,21\n')
            file.write('12000,22\n')
            file.write('12600,23\n')
            file.write('13200,22\n')
            file.write('13800,21\n')
            
            # Torno all'inizio del file (necessario per i tmpfile) 
            file.seek(0) 

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            results = hourly_trend_changes(time_series)

            self.assertTrue(len(results) in [2,3])
            self.assertEqual(results[0], 1)
            self.assertEqual(results[1], 1)
            
            global score; score += 18 # Increase score
            
            # Controllo anche sull'ultima ora ed il suo cabio trend calcolato correttamente
            if len(results) == 3:
                if results[2] == 1:
                    score += 1 # Increase score



    #=====================================================
    # Controllo su cambi ora al limite
    #=====================================================

    def test_correctness_last_day(self):

        with tempfile.NamedTemporaryFile('w+t') as file:
            
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=3600
            for i in range(3):
                for j in range(6):
                    if j<3:
                        data='{},{}\n'.format(epoch, 20+j)
                    else:
                        data='{},{}\n'.format(epoch, 26-j)
                    file.write(data)
                    epoch+=600
            file.seek(0) # Torno all'inizio del file (necessario per i tmpfile) 
            
            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            results = hourly_trend_changes(time_series)
            
            self.assertEqual(results[0], 1)
            self.assertEqual(results[1], 2)
            self.assertEqual(results[2], 2)
    
            global score; score += 2 # Increase score

 
 
    #===================================================
    # Una sola misurazione per ora con inversione trend
    #===================================================
 
    def test_correctness_edge_cases_1(self):
        with tempfile.NamedTemporaryFile('w+t') as file:
              
            file.write('epoch,temperature\n')
            
            # Prima ora
            file.write('3600,22\n')
            
            # Seconda ora
            file.write('7200,21\n')
             
            # Terza ora
            file.write('10800,20\n')

            # Quarta ora
            file.write('14400,21\n')
            
#             # Prima ora
#             file.write('3600,22\n')
#             
#             # Seconda ora
#             file.write('7200,20\n')
#              
#             # Terza ora
#             file.write('10800,21\n')
            
            
            # Torno all'inizio del file
            file.seek(0)
 
            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            results = hourly_trend_changes(time_series)
            self.assertEqual(results, [0, 0, 0, 1])
 
            global score; score += 2 # Increase score


    #===================================================
    #  Test che ci sia la variabile "name" nell'init
    #===================================================
    def test_csv_file_interface(self):
 
        with tempfile.NamedTemporaryFile('w+t') as file:
              
            file.write('epoch,temperature\n')
            file.write('600,21\n')
            file.write('1200,22\n')
            file.seek(0)
 
            time_series_file = CSVTimeSeriesFile(name = file.name)
            time_series = time_series_file.get_data()
             
            # Test su lunghezze
            self.assertTrue(len(time_series) in [1,2])
 
            global score; score += 0.5 # Increase score
 
 
    #===================================================
    #  Test su errori esistenza e tipo del nome del file
    #===================================================

    def test_csv_file_interface_nonexisttent_file(self):
            
        with self.assertRaises(ExamException):
            time_series_file = CSVTimeSeriesFile(name='file_non_esistente.csv')
            time_series_file.get_data()
        global score; score += 0.5 # Increase score


    def test_csv_file_interface_wrong_type(self):
            
        with self.assertRaises(ExamException):
            time_series_file = CSVTimeSeriesFile(name=[])
            time_series_file.get_data()           

        with self.assertRaises(ExamException):
            time_series_file = CSVTimeSeriesFile(name=None)
            time_series_file.get_data()     

        global score; score += 0.5 # Increase score


    #===================================================
    #  Test su varie cose da gestire riguardo ad epoch
    #===================================================

    def test_csv_file_epoch_floating_point(self):

        with tempfile.NamedTemporaryFile('w+t') as file:
            
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            file.write('615.3333333333,21\n')  # Epoch floating point
            file.write('615.9999999999,22\n')  # Epoch floating point
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            
            # Test su lunghezza ed elementi con epoch arrotondato correttamente
            self.assertTrue(len(time_series), 2)
            self.assertEqual(time_series[0], [615, 21])
            self.assertEqual(time_series[1], [616, 22])


            global score; score += 1 # Increase score


    def test_csv_file_epoch_unordered(self):

        with tempfile.NamedTemporaryFile('w+t') as file:
            
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                file.write('{},{}\n'.format(epoch, (i+1)))
                epoch+=86400
            file.write('1000,{}\n'.format(epoch, 42)) # Epoch fuori ordine
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            
            with self.assertRaises(ExamException):
                time_series_file.get_data()
                
            global score; score += 1 # Increase score


    def test_csv_file_epoch_duplicates(self):

        with tempfile.NamedTemporaryFile('w+t') as file:
            
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                file.write('{},{}\n'.format(epoch, (i+1)))
                epoch+=86400
            file.write('86400,{}\n'.format(epoch, 42)) # Epoch duplicato
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            
            with self.assertRaises(ExamException):
                time_series_file.get_data()

            global score; score += 1 # Increase score


    #===================================================
    #  Test su vari contenuti del file CSV sporcati
    #===================================================

    def test_csv_file_dirty_1(self):

        with tempfile.NamedTemporaryFile('w+t') as file:
            
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                file.write('{},{},HELLOOOOOOOWOOORLDDDDDDDDD\n'.format(epoch, (i+1))) # Campo che non c'entra
                epoch+=86400
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            
            # Test su lunghezza e ultimo elemento
            self.assertEqual(len(time_series), 30)
            self.assertEqual(time_series[29], [2592000, 30.0])

            global score; score += 0.5 # Increase score

    def test_csv_file_dirty_2(self):

        with tempfile.NamedTemporaryFile('w+t') as file:
            
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                file.write('{},{}\n'.format(epoch, (i+1)))
                file.write('\n') # Righe vuote in mezzo
                file.write('Nel mezzo del cammin di nostra vita\n')  # Righe di testo senza senso in mezzo
                file.write('mi son imbattuto in un test un po\' fastisioso\n')  # Righe di testo senza senso in mezzo (2)
                epoch+=86400
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            
            # Test su lunghezza e ultimo elemento
            self.assertEqual(len(time_series), 30)
            self.assertEqual(time_series[29], [2592000, 30.0])
        
            global score; score += 0.5 # Increase score


    def test_csv_file_dirty_3(self):

        with tempfile.NamedTemporaryFile('w+t') as file:
            
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                file.write('{},{}\n'.format(epoch, (i+1)))
                file.write('{},SonoUnaTemperaturaNonValidaComeNumero\n') # Una temperature non valida
                epoch+=86400
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()

            # Test su lunghezza e ultimo elemento
            self.assertEqual(len(time_series), 30)
            self.assertEqual(time_series[29], [2592000, 30.0])
        
            global score; score += 0.5 # Increase score


    def test_csv_file_dirty_4(self):

        with tempfile.NamedTemporaryFile('w+t') as file:
            
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                file.write('{},{}\n'.format(epoch, (i+1)))
                file.write('SonoUnaEpochNonValidaComeNumero,34\n') # Un timestamp epoch non valido
                epoch+=86400
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()

            # Test su lunghezza e ultimo elemento
            self.assertEqual(len(time_series), 30)
            self.assertEqual(time_series[29], [2592000, 30.0])
        
            global score; score += 0.5 # Increase score


    def test_csv_file_empty(self):

        with tempfile.NamedTemporaryFile('w+t') as file:
            
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            
            # File vuoto. Mezzo punto per chi ha pensato di gestirla in un modo o
            # nell'altro. Se invece non e' gestito e sale un' eccezione diversa da
            # ExamException o non torna lista vuota, non si prende il mezzo punto.
            
            time_series_file = CSVTimeSeriesFile(file.name)
            try:
                time_series = time_series_file.get_data()
            except ExamException:
                pass
            else:
                self.assertEqual(time_series, [])
            
            global score; score += 0.5 # Increase score



    # Print the score
    @classmethod
    def tearDownClass(cls):
        global score

        print('\n\n-------------')
        print('| Voto: {}  |'.format(score))
        print('-------------\n')


# Run the tests
unittest.main()
