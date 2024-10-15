from tortoise import fields, Tortoise
from tortoise.models import Model


class Identity(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    father_name = fields.CharField(max_length=255)
    grand_father_name = fields.CharField(max_length=255)
    request_no = fields.CharField(max_length=255)
    receiving_date = fields.CharField(max_length=255)
    location = fields.CharField(max_length=255)

    class Meta: 
        table = 'identity'

    def __str__(self):
        return f'<Identity(id={self.id}, name={self.name}, father_name={self.father_name}, grand_father_name={self.grand_father_name}, request_no={self.request_no}, receiving_date={self.receiving_date}, location={self.location})>'
