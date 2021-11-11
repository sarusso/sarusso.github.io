#==============================
# Test  
#==============================
 
 
import unittest
import tempfile
import warnings

from esame import CSVTimeSeriesFile, compute_daily_variance, ExamException

 
score = 0
 
class TestAndGrade(unittest.TestCase):

    # Roba per il testing
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)


    #===========================================================
    # Test per il 18: tre giorni di dati, tutti i dati presenti.
    #===========================================================

    def test_correctness(self):
        
        with tempfile.NamedTemporaryFile('w+t') as file:

            file.write('epoch,temperature\n')

            # Inizializzo epoch
            epoch = 3600*23
            
            # Prima giorno
            for i in range(24):
                epoch += 3600
                file.write('{},{}\n'.format(epoch,i))

            # Secondo giorno
            for i in range(24):
                epoch += 3600
                file.write('{},{}\n'.format(epoch,i/2))

            # Terzo giorno
            for i in range(24):
                epoch += 3600
                file.write('{},{}\n'.format(epoch,i*2))
                        
            # Torno all'inizio del file (necessario per i tmpfile) 
            file.seek(0) 

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            results = compute_daily_variance(time_series)
            
            self.assertTrue(len(results) in [2,3])
            self.assertEqual(results[0], 50)
            self.assertEqual(results[1], 12.5)
            
            global score; score += 18 # Increase score
            
            # Controllo anche sull'ultimo giorno
            if len(results) == 3:
                if results[2] == 200:
                    score += 1 # Increase score


    #===================================================
    # Una sola misurazione per giorno (a mezzogiorno)
    #===================================================
 
    def test_correctness_edge_cases_1(self):
 
        with tempfile.NamedTemporaryFile('w+t') as file:
             
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=int(86400+(86400/2))
            for i in range(3):
                file.write('{},{}\n'.format(epoch, (i+1)))
                epoch+=86400
            file.seek(0) # Torno all'inizio del file (necessario per i tmpfile) 
 
            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            results = compute_daily_variance(time_series)
  
            self.assertEqual(results[0], None)
            self.assertEqual(results[1], None)

            global score; score += 1 # Increase score

            # Controllo anche sull'ultimo giorno
            if len(results) == 3:
                if results[2] is None:
                    score += 1 # Increase score


    #===================================================
    # Una sola misurazione per giorno (a mezzanotte)
    #===================================================
 
    def test_correctness_edge_cases_3(self):
 
        with tempfile.NamedTemporaryFile('w+t') as file:
             
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(3):
                file.write('{},{}\n'.format(epoch, (i+1)))
                epoch+=86400
            file.seek(0) # Torno all'inizio del file (necessario per i tmpfile) 
 
            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            results = compute_daily_variance(time_series)
 
            self.assertEqual(results[0], None)
            self.assertEqual(results[1], None)

            global score; score += 1 # Increase score

            # Controllo anche sull'ultimo giorno
            if len(results) == 3:
                if results[2] is None:
                    score += 1 # Increase score

 
    #===================================================
    #  Test che ci sia la variabile "name" nell'init
    #===================================================
    def test_csv_file_interface(self):
 
        with tempfile.NamedTemporaryFile('w+t') as file:
             
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                file.write('{},{}\n'.format(epoch, (i+1))) # Campo che non c'entra
                epoch+=86400
            file.seek(0) # Torno all'inizio del file (necessario per i tmpfile) 
 
            time_series_file = CSVTimeSeriesFile(name = file.name)
            time_series = time_series_file.get_data()
             
            # Test su lunghezze
            self.assertTrue(len(time_series) in [29,30])
 
            global score; score += 1 # Increase score
 


    #===================================================
    #  Vari test CSV file sporcati
    #===================================================
 
    def test_csv_file_dirty_1(self):
 
        with tempfile.NamedTemporaryFile('w+t') as file:
             
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                file.write('{},{},HELLOOOOOOOWOOORLDDDDDDDDD\n'.format(epoch, (i+1))) # Campo che non c'entra
                epoch+=86400
            file.seek(0) # Torno all'inizio del file (necessario per i tmpfile) 
 
            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
             
            # Test su lunghezza e ultimo elemento
            self.assertEqual(len(time_series), 30)
            self.assertEqual(time_series[29], [2592000, 30.0])
 
            global score; score += 1 # Increase score
 
 
    def test_csv_file_dirty_2(self):
 
        with tempfile.NamedTemporaryFile('w+t') as file:
             
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                file.write('{}.6666666666,{}\n'.format(epoch, (i+1))) # Ogni epoch diventa magicamente floating point
                epoch+=86400
            file.seek(0) # Torno all'inizio del file (necessario per i tmpfile) 
 
            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
             
            # Test su lunghezza e ultimo elemento
            self.assertEqual(len(time_series), 30)
            self.assertEqual(time_series[29], [2592000, 30.0])
 
            global score; score += 1 # Increase score
 
 
    def test_csv_file_dirty_3(self):
 
        with tempfile.NamedTemporaryFile('w+t') as file:
             
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                file.write('{}.333333333333333,{}\n'.format(epoch, (i+1)))
                file.write('\n') # Righe vuote in mezzo
                file.write('Nel mezzo del cammin di nostra vita\n')  # Righe di testo senza senso in mezzo
                file.write('mi son imbattuto in un test un po\' fastisioso\n')  # Righe di testo senza senso in mezzo (2)
                epoch+=86400
            file.seek(0) # Torno all'inizio del file (necessario per i tmpfile) 
 
            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
             
            # Test su lunghezza e ultimo elemento
            self.assertEqual(len(time_series), 30)
            self.assertEqual(time_series[29], [2592000, 30.0])
         
            global score; score += 1 # Increase score
 
 
    def test_csv_file_dirty_4(self):
 
        with tempfile.NamedTemporaryFile('w+t') as file:
             
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                file.write('{},{}\n'.format(epoch, (i+1)))
                epoch+=86400
            file.write('1000,{}\n'.format(epoch, 42)) # Epoch fuori ordine
            file.seek(0) # Torno all'inizio del file (necessario per i tmpfile) 
 
            time_series_file = CSVTimeSeriesFile(file.name)
             
            with self.assertRaises(ExamException):
                time_series_file.get_data()
 
            global score; score += 1 # Increase score
 
 
    def test_csv_file_dirty_5(self):
 
        with tempfile.NamedTemporaryFile('w+t') as file:
             
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                file.write('{},{}\n'.format(epoch, (i+1)))
                epoch+=86400
            file.write('86400,{}\n'.format(epoch, 42)) # Epoch duplicato
            file.seek(0) # Torno all'inizio del file (necessario per i tmpfile) 
 
            time_series_file = CSVTimeSeriesFile(file.name)
             
            with self.assertRaises(ExamException):
                time_series_file.get_data()
 
            global score; score += 1 # Increase score
 
 
    def test_csv_file_dirty_6(self):
 
        with tempfile.NamedTemporaryFile('w+t') as file:
             
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                file.write('{},{}\n'.format(epoch, (i+1)))
                file.write('{},SonoUnaTemperaturaNonValidaComeNumero\n') # Una temperature non valida
                epoch+=86400
            file.seek(0) # Torno all'inizio del file (necessario per i tmpfile) 
 
            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
 
            # Test su lunghezza e ultimo elemento
            self.assertEqual(len(time_series), 30)
            self.assertEqual(time_series[29], [2592000, 30.0])
         
            global score; score += 1 # Increase score
 
 
    def test_csv_file_dirty_7(self):
 
        with tempfile.NamedTemporaryFile('w+t') as file:
             
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                file.write('{},{}\n'.format(epoch, (i+1)))
                file.write('SonoUnaEpochNonValidaComeNumero,34\n') # Un timestamp epoch non valido
                epoch+=86400
            file.seek(0) # Torno all'inizio del file (necessario per i tmpfile) 
 
            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
 
            # Test su lunghezza e ultimo elemento
            self.assertEqual(len(time_series), 30)
            self.assertEqual(time_series[29], [2592000, 30.0])
         
            global score; score += 1 # Increase score
 
 
    def test_csv_file_dirty_8(self):
 
        with tempfile.NamedTemporaryFile('w+t') as file:
             
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
             
            # File vuoto. Bonus per chi ha pensato di gestirla in un modo o
            # nell'altro. Se invece non e' gestito e sale un' eccezione diversa
            # da ExamException, allora non si prende il punto.
             
            time_series_file = CSVTimeSeriesFile(file.name)
            try:
                time_series = time_series_file.get_data()
            except ExamException:
                pass
            else:
                self.assertEqual(time_series, [])
             
            global score; score += 1 # Increase score



    # Print the score
    @classmethod
    def tearDownClass(cls):
        global score

        print('\n\n-------------')
        print('| Voto: {}  |'.format(score))
        print('-------------\n')


# Run the tests
unittest.main()