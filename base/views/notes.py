class Notes:
    def __init__(self):
        self.tutor = None
        self.structure = None
        self.lu_list= []


class NotesDetail:
    def __init__(self):
        self.lu = None
        self.nb_notes_encoded = 0
        self.nb_student = 0
        self.tutor = None

    def completed(self):

        if self.nb_notes_encoded == self.nb_student:
            return True

        return False
