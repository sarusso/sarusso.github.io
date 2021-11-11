#==============================
# Test  
#==============================
 
 
import unittest
import tempfile
import warnings

from esame import CSVTimeSeriesFile, daily_stats, ExamException
 
score = 0
 
class TestAndGrade(unittest.TestCase):

    # Ignoro alcuni warning per pulire l'output del testing
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)


    #==============================================================
    # Test per il 18: 30 giorni puliti con tutti i dati presenti.
    #==============================================================

    def test_correctness(self):
        
        with tempfile.NamedTemporaryFile('w+t') as file:
            
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                for j in range(24):
                    file.write('{},{}\n'.format(epoch, (j+1)/(i+1)))
                    # Valori del primo giorno: 1,2,3,4...24
                    # Valori del secondo giorno: 0.5,1,1.5,2...12
                    # ..e cosi' via
                    epoch+=3600
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            results = daily_stats(time_series)

            # Primo giorno
            self.assertTrue(len(results) in [29,30])
            self.assertEqual(results[0][0], 1)
            self.assertEqual(results[0][1], 24)
            self.assertAlmostEqual(results[0][2], 12.5, 3)
    
            # Secondo giorno
            self.assertEqual(results[1][0], 0.5)
            self.assertEqual(results[1][1], 12)
            self.assertAlmostEqual(results[1][2], 6.25, 3)
    
            # Ventinovesimo giorno
            self.assertEqual(results[28][0], 1/29)
            self.assertEqual(results[28][1], 24/29)
            self.assertAlmostEqual(results[28][2], 0.431, 2)
            
            global score; score += 18 # Increase score      


    #=====================================================
    # Controllo sul'ultimo giorno calcolato correttamente
    #=====================================================

    def test_correctness_last_day(self):

        with tempfile.NamedTemporaryFile('w+t') as file:
            
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                for j in range(24):
                    file.write('{},{}\n'.format(epoch, (j+1)/(i+1)))
                    # Valori del primo giorno: 1,2,3,4...24
                    # Valori del secondo giorno: 0.5,1,1.5,2...12
                    # ..e cosi' via
                    epoch+=3600
            file.seek(0) 

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            results = daily_stats(time_series)
 
            self.assertEqual(len(results), 30)
            self.assertEqual(results[29][0], 1/30)
            self.assertEqual(results[29][1], 24/30)
            self.assertAlmostEqual(results[29][2], 0.417, 2)
     
            global score; score += 2 # Increase score


    #=====================================================
    # Controllo su un mese da 28 giorni
    #=====================================================

    def test_correctness_28_days_month(self):

        with tempfile.NamedTemporaryFile('w+t') as file:
            
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(28):
                for j in range(24):
                    file.write('{},{}\n'.format(epoch, (j+1)/(i+1)))
                    # Valori del primo giorno: 1,2,3,4...24
                    # Valori del secondo giorno: 0.5,1,1.5,2...12
                    # ..e cosi' via
                    epoch+=3600
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            results = daily_stats(time_series)
 
            self.assertEqual(len(results), 28)
            self.assertEqual(results[27][0], 1/28)
            self.assertEqual(results[27][1], 24/28)
            self.assertAlmostEqual(results[27][2], 0.446, 2)
     
            global score; score += 1 # Increase score


    #===================================================
    # Una sola misurazione per giorno (a mezzogiorno)
    #===================================================

    def test_correctness_edge_cases_1(self):

        with tempfile.NamedTemporaryFile('w+t') as file:
            
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=int(86400+(86400/2))
            for i in range(30):
                file.write('{},{}\n'.format(epoch, (i+1)))
                epoch+=86400
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            results = daily_stats(time_series)

            self.assertEqual(results[0][0], 1)
            self.assertEqual(results[0][1], 1)
            self.assertEqual(results[0][2], 1)
    
            self.assertEqual(results[28][0], 29)
            self.assertEqual(results[28][1], 29)
            self.assertEqual(results[28][2], 29)
     
            global score; score += 0.5 # Increase score


    #===================================================
    # Una sola misurazione per giorno (a mezzogiorno)
    # ..con controllo sull'ultimo giorno
    #===================================================

    def test_correctness_edge_cases_2(self):

        with tempfile.NamedTemporaryFile('w+t') as file:
            
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=int(86400+(86400/2))
            for i in range(30):
                file.write('{},{}\n'.format(epoch, (i+1)))
                epoch+=86400
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            results = daily_stats(time_series)

            self.assertEqual(results[29][0], 30)
            self.assertEqual(results[29][1], 30)
            self.assertEqual(results[29][2], 30)
     
            global score; score += 0.5 # Increase score


    #===================================================
    # Una sola misurazione per giorno (a mezzanotte)
    #===================================================

    def test_correctness_edge_cases_3(self):

        with tempfile.NamedTemporaryFile('w+t') as file:
            
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                file.write('{},{}\n'.format(epoch, (i+1)))
                epoch+=86400
            file.seek(0) 

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            results = daily_stats(time_series)

            self.assertEqual(results[0][0], 1)
            self.assertEqual(results[0][1], 1)
            self.assertEqual(results[0][2], 1)

            self.assertEqual(results[28][0], 29)
            self.assertEqual(results[28][1], 29)
            self.assertEqual(results[28][2], 29)
 
            global score; score += 0.5 # Increase score


    #===================================================
    # Una sola misurazione per giorno (a mezzanotte)
    # ..con controllo sull'ultimo giorno
    #===================================================

    def test_correctness_edge_cases_4(self):

        with tempfile.NamedTemporaryFile('w+t') as file:
            
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                file.write('{},{}\n'.format(epoch, (i+1)))
                epoch+=86400
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            results = daily_stats(time_series)

            self.assertEqual(results[29][0], 30)
            self.assertEqual(results[29][1], 30)
            self.assertEqual(results[29][2], 30)
 
            global score; score += 0.5 # Increase score


    #===================================================
    #  Test che ci sia la variabile "name" nell'init
    #===================================================
    def test_csv_file_interface(self):

        with tempfile.NamedTemporaryFile('w+t') as file:
            
            # Scrivo i contenuti nel file di test
            file.write('epoch,temperature\n')
            epoch=86400
            for i in range(30):
                file.write('{},{}\n'.format(epoch, (i+1)))
                epoch+=86400
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(name = file.name)
            time_series = time_series_file.get_data()
            self.assertTrue(len(time_series)>0)

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
            epoch=86400
            for i in range(30):
                file.write('{}.333333333333333,{}\n'.format(epoch, (i+1))) # Ogni epoch diventa magicamente floating point
                epoch+=86400
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            
            # Test su lunghezza e ultimo elemento
            self.assertTrue(len(time_series), 30)
            self.assertEqual(time_series[29], [2592000, 30.0])

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
                # Va bene alzare l'eccezione sia in get_data che il daily_stats, la specifica era debole
                time_series = time_series_file.get_data()
                daily_stats(time_series)
                
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
                # Va bene alzare l'eccezione sia in get_data che il daily_stats, la specifica era debole
                time_series = time_series_file.get_data()
                daily_stats(time_series)

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
            
            # File vuoto. Punto per chi ha pensato di gestirla in un modo o
            # nell'altro. Se invece non e' gestito e sale un' eccezione diversa
            # da ExamException o non torna lista vuota, non si prende il punto.
            
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