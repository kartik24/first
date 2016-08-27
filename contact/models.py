from django.db import models
from django.utils import timezone


class pathlab(models.Model):

    Path_Lab_Id = models.IntegerField(primary_key=True, default="")
    Path_Lab_Password = models.CharField(max_length=20, default="")
    Path_Lab_Name = models.CharField(max_length=200 , default="")
    Basic_Contact_number = models.CharField(max_length=20, default="")
    Alternate_Contact_number = models.CharField(max_length=20, default="")
    Home_Pick_up = models.BooleanField()
    Account_Number = models.CharField(max_length=200 , default="")
    IFSC_Code = models.CharField(max_length=200 , default="")
    Email_Id = models.EmailField()
    Country = models.CharField(max_length=200,default="")

    class Meta:
        db_table = u'pathlab'


    def apply_filter(self, **kwargs):
        lab = pathlab.objects.all()
        if 'Path_Lab_Name' in kwargs and kwargs.get('Path_Lab_Name') != '':
            lab = lab.filter(Path_Lab_Name=kwargs['Path_Lab_Name'])
       # """if 'clinic_name' in kwargs and kwargs.get('clinic_name')!= '':
        #    doctor= doctor.filter(clinic_name = kwargs['clinic_name'])"""
        return lab


class pathlabinfo(models.Model):

    Path_Lab_Id = models.ForeignKey(pathlab, on_delete=models.CASCADE)
    City = models.CharField(max_length=30)
    Pincode = models.CharField(max_length=30)
    Nearby_Pincode = models.CharField(max_length=30)
    Basic_Contact_number = models.CharField(max_length=20, default="")
    Alternate_Contact_number = models.CharField(max_length=20, default="")
    Address_No1_Plot_Number = models.CharField(max_length=30)
    Address_No2_Sub_Locality = models.CharField(max_length=100)
    Address_No3_Area = models.CharField(max_length=100)
    Is_Package = models.BooleanField()
    Package_Name = models.CharField(max_length=100)
    Test_Day = models.CharField(max_length=300, default="")
    Test_Name = models.CharField(max_length=30)
    Test_Start_at = models.DateTimeField()  # ManyToManyField(Days)
    # clinic_timing = models.CharField(max_length=50)
    Test_End_at = models.DateTimeField()
    Price = models.CharField(max_length=255)
    Details = models.TextField()

    class Meta:
        db_table = u'pathlabinfo'