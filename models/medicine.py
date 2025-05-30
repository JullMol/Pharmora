class Medicine:
    def __init__(self, med_id, name, composition, uses, side_effect, manufacturer, excellent_review, average_review, poor_review):
        self.med_id = med_id
        self.name = name
        self.composition = composition
        self.uses = uses
        self.side_effect = side_effect
        self.manufacturer = manufacturer
        self.excellent_review = float(excellent_review) if excellent_review else 0
        self.average_review = float(average_review) if average_review else 0
        self.poor_review = float(poor_review) if poor_review else 0

    def __str__(self):
        return f"{self.name} (ID: {self.med_id}) - Uses: {self.uses}, Composition: {self.composition}"
    