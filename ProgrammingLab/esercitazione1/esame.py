class ExamException(Exception):
    pass

class MovingAverage():
    
    def __init__(self, window):
        
        # Controllo che la lunghezza della finestra si di tipo intero
        if not isinstance(window, int):
            raise ExamException('Invalid type for window, only int supported. Got "{}"'.format(type(window)))

        # Controllo che la lunghezza della finestra non sia uguale a zero o negativa.
        # nota bene che una finestra di lunghezza uno e' accettata!
        if window < 1:
            raise ExamException('Negative or zero window value provided')
        
        # Salvo la lunghezza della finestra internamente
        self.window = window
    
    def compute(self, data):

        # Controllo che i valori siano in una lista
        if not isinstance(data, list):
            raise ExamException('Invalid type for data, only list supported. Got "{}"'.format(type(data)))

        # Controllo che la lista sia abbastanza lunga
        if len(data) < self.window:
            raise ExamException('Not enough data to compute a moving average of "{}" steps'.format(self.window))
        
        # Controllo che i valori della lista siano di tipo floato o numerico.
        # Questo controllo non era veramente richiesto, e puo' alle volte
        # risultare lento perchè aggiungo un ciclo su tutti gli elementi della lista.
        # Tuttavia dava punti extra nella valutazione, per premiare chi ci ha pensato
        # e si e' posto il problema a prescindere dalle performance (che non sono
        # argomento di quetso corso).
        
        for item in data:
            if not (isinstance(item, int) or  isinstance(item, float)):
                raise ExamException('Got non-numeric item in the list data: "{}"'.format(item))
        
        # Ok, ora calcolo la media mobile ciclando su tutti gli elmenti della lista. Per la natura
        # del problema, non posso essere del tutto pythonico ed usar eper esempio il costrutto 
        # "for item in list", ma devo usare un' indice di supporto.
        
        averages = []
        for i in range(len(data)+1):
            
            # Se non ho ho abbastanza valori su cui applicarla, 
            # continuo andando al prossimo giro
            if i < self.window:
                continue
            else:
                # Forma contratta che usa la "sum" built-in. Si poteva implementare
                # questa parte in molti altri modi, piu' o meno contratti.
                averages.append(sum(data[i-self.window:i])/self.window)
                
        return averages