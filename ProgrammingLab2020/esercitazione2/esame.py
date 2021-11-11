
class ExamException(Exception):
    pass

class Diff():
    
    def __init__(self, ratio=1):
        
        # Controllo che la ratio sia di tipo numerico
        if not isinstance(ratio, int) and not isinstance(ratio, float):
            raise ExamException('Invalid type for ratio, only int or float supported. Got "{}"'.format(type(ratio)))

        # Controllo che il rapporto sia positivo e non uguale a zero
        if ratio <= 0:
            raise ExamException('Negative or zero ratio value provided')
        
        # Salvo la ratio internamente
        self.ratio = ratio
    
    def compute(self, data):

        # Controllo che i valori siano in una lista
        if not isinstance(data, list):
            raise ExamException('Invalid type for data, only list supported. Got "{}"'.format(type(data)))

        # Controllo che la lista sia abbastanza lunga per fare la differenza tra almeno due elementi
        if len(data) < 2:
            raise ExamException('Not enough data to compute a diff! Got only one element in the data.')

        # Controllo che i valori della lista siano di tipo floato o numerico.
        # Questo controllo non era veramente richiesto, e puo' alle volte
        # risultare lento perche' aggiungo un ciclo su tutti gli elementi della lista.
        # Tuttavia dava punti extra nella valutazione, per premiare chi ci ha pensato
        # e si e' posto il problema a prescindere dalle performance (che non sono
        # argomento di quetso corso).
        for item in data:
            if not (isinstance(item, int) or  isinstance(item, float)):
                raise ExamException('Got non-numeric item in the list data: "{}"'.format(item))
        
        # Ok, ora calcolo la differenza ciclando su tutti gli elmenti della lista.
        # Posso essere abbastanza pythinico e non usare neanche un indice!
        
        # Qui salvero' la lista delle differenze
        diff_list = []
        
        # Variabile di supporto per l'elemento precedente con cui far' la differenza
        prev_item = None
        
        # Ciclo sugli elementi
        for item in data:

            if not prev_item:
                # Salto il primo elemento (non faccio nulla, pass e' l'istruzione vuota).
                # Capisco che e' il primo perche' non c'e' nessun elemento precedente settato 
                pass
            
            else:
                # Calcolo la differenza con l'elemento precedente
                item_diff = item-prev_item
                
                # Se devo dividere per u fattore di scala, lo faccio
                if self.ratio is not None:
                    item_diff = item_diff / self.ratio
                
                # Ora appendo alla lista delle differenze
                diff_list.append(item_diff)

            # Infine assegno la variabile di supporto per l'elemento precednete
            prev_item = item

        return diff_list




