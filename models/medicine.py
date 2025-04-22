class Medicine:
    def __init__(self, med_id, name, composition, uses, side_effect, image_url, manufacturer, excellent_review, average_review, poor_review):
        self.med_id = med_id
        self.name = name
        self.composition = composition
        self.uses = uses
        self.side_effect = side_effect
        self.image_url = image_url
        self.manufacturer = manufacturer
        self.excellent_review = int(excellent_review) if excellent_review else 0
        self.average_review = int(average_review) if average_review else 0
        self.poor_review = int(poor_review) if poor_review else 0

    def __str__(self):
        return f"{self.name} (ID: {self.med_id}) - Uses: {self.uses}, Composition: {self.composition}"
    