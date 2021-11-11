#==============================
# Test  
#==============================
 
 
import unittest
import tempfile
import warnings

from esame import CSVTimeSeriesFile, hourly_trend_changes, ExamException

 
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
            # Torno all'inizio del file (necessario per i tmpfile) 
            file.seek(0)
             
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

            # Torno all'inizio del file (necessario per i tmpfile) 
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
            # Torno all'inizio del file (necessario per i tmpfile) 
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
            # Torno all'inizio del file (necessario per i tmpfile) 
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
            # Torno all'inizio del file (necessario per i tmpfile) 
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
            # Torno all'inizio del file (necessario per i tmpfile) 
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
            # Torno all'inizio del file (necessario per i tmpfile) 
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
            # Torno all'inizio del file (necessario per i tmpfile) 
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
            # Torno all'inizio del file (necessario per i tmpfile) 
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
            # Torno all'inizio del file (necessario per i tmpfile) 
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