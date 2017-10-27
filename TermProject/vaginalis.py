from TermProject.genome import Genome


class Vaginalis(Genome):
    def __init__(self, resistance_scale_factor, identifier, datafile):
        self._resistanceScaleFactor = resistance_scale_factor
        super(Vaginalis, self).__init__(identifier, datafile)

    def get_sequence_list_by_resistance(self):
        pass
