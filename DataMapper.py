import DataModel as model  

class DataMapper:
    def __init__(self, data):
        self.data = data
        self.mapData()

    def mapData(self):
        model.user_id = self.data['Kullanici_id']
        model.gender = self.data['Cinsiyet']
        model.birthday = self.data['Dogum_Tarihi']
        model.nationality = self.data['Uyruk']
        model.city = self.data['Il']
        model.drug_name = self.data['Ilac_Adi']
        model.drug_start_date = self.data['Ilac_Baslangic_Tarihi']
        model.drug_end_date = self.data['Ilac_Bitis_Tarihi']
        model.side_effect = self.data['Yan_Etki']
        model.side_effect_report_date = self.data['Yan_Etki_Bildirim_Tarihi']
        model.allergy = self.data['Alerjilerim']
        model.chronic_disease = self.data['Kronik Hastaliklarim']
        model.father_chronic_disease = self.data['Baba Kronik Hastaliklari']
        model.mother_chronic_disease = self.data['Anne Kronik Hastaliklari']
        model.sister_chronic_disease = self.data['Kiz Kardes Kronik Hastaliklari']
        model.brother_chronic_disease = self.data['Erkek Kardes Kronik Hastaliklari']
        model.blood_type = self.data['Kan Grubu']
        model.weight = self.data['Kilo']
        model.height = self.data['Boy']