from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.pk}번 의사 {self.name}'


# 우리가 하고싶은 것.
# patient.doctors.all()  ->  내가 가지고 있는 모든 의사들의 정보를 가지고오는 것.
# doctor.patioents.all()
class Patient(models.Model):
    name = models.CharField(max_length=200)
    # doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    # doctor을 만든 후에 사용할 수 있기 때문에 Patient 모델부터 사용할 수 있음
    doctors = models.ManyToManyField(Doctor, related_name='patients')
    # patient.doctors.all() -> 가능
    # patients = doctor.patients_set.all() -> doctor.patients.all() 사용 가능  /  related 했기때문에

    '''
    1번의사 -> 1번환자 추가 :  doctor1.patients.add(patient1) 

    In [5]: patient1.doctors.all()
    Out[5]: <QuerySet [<Doctor: 1번 의사 혜련>]>

    In [6]: doctor1.patients.all()
    Out[6]: <QuerySet [<Patient: 1번 환자 쑤>]>

    # 예약취소
    In [7]: patient1.doctors.remove(doctor1)

    In [8]: patient1.doctors.all()
    Out[8]: <QuerySet []>
    '''

    def __str__(self):
        return f'{self.pk}번 환자 {self.name}'



# class Reservation(models.Model):
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'의사{self.doctor.id} - 환자{self.patient.id}'
