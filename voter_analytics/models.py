from django.db import models
import csv 
import os 
from datetime import datetime

# Create your models here.

class Voter(models.Model):
    ''' Store/represent the data from one registered voter in Newton, Massachusetts.'''

    # identification
    first_name = models.TextField()
    last_name = models.TextField()

    # residential address 
    street_name = models.TextField()
    street_number = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.TextField()

    # registration information
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_registration = models.DateField(null=True, blank=True)
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.TextField()

    # election participation
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    voter_score = models.IntegerField()

    def __str__(self):
        ''' Returns a string representation of the voter.'''
        return f'{self.first_name} {self.last_name}, {self.precinct_number}'
    

def load_data():
    '''Function to load data records from CSV file into the Django database.'''

    Voter.objects.all().delete()

    # Find the CSV file
    filename = os.path.join(os.path.dirname(__file__), 'newton_voters.csv')

    # Open file for reading
    f = open(filename, 'r')
    reader = csv.reader(f)
    # ignore headers 
    next(reader)

    def convert_date(date_string):
            '''Convert date strings into date objects'''
            try:
                return datetime.strptime(date_string, '%Y-%m-%d').date()
            except ValueError:
                return None  

    # Loop to read the file one line at a time
    for fields in reader: 
        
        try:
            dob = convert_date(fields[7])
            registration_date = convert_date(fields[8])

            # Create a new Voter object 
            voter = Voter(
                last_name=fields[1],
                first_name=fields[2],
                street_number=fields[3] if fields[3] else None,
                street_name=fields[4],
                apartment_number=fields[5],
                zip_code=fields[6],
                date_of_birth=dob,
                date_of_registration=registration_date,
                party_affiliation=fields[9],
                precinct_number=fields[10],
                v20state=fields[11].strip().upper() == 'TRUE',
                v21town=fields[12].strip().upper() == 'TRUE',
                v21primary=fields[13].strip().upper() == 'TRUE',
                v22general=fields[14].strip().upper() == 'TRUE',
                v23town=fields[15].strip().upper() == 'TRUE',
                voter_score=int(fields[16]),
            )
            voter.save()

        except Exception as e:
            print("Something went wrong!")
            print(f"fields={fields}")
            print(e)

    f.close()
    print(f"Done. Created {Voter.objects.count()} Voters")


