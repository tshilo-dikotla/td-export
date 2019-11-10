import datetime
from pytz import timezone
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError

from django_crypto_fields.fields import (
    EncryptedCharField, EncryptedDecimalField, EncryptedIntegerField,
    EncryptedTextField, FirstnameField, IdentityField, LastnameField)
encrypted_fields = [
    EncryptedCharField, EncryptedDecimalField, EncryptedIntegerField,
    EncryptedTextField, FirstnameField, IdentityField, LastnameField]


class ExportMethods:
    """Export Tshilo Dikotla data.
    """
    
    def __init__(self):
        self.antenatal_enrollment_cls = django_apps.get_model('td_maternal.antenatalenrollment')
        self.rs_cls = django_apps.get_model('edc_registration.registeredsubject')
        self.maternal_rando_cls = django_apps.get_model('td_maternal.maternalrando')
        self.subject_consent_csl = django_apps.get_model('td_maternal.subjectconsent')
        self.subject_screening_csl = django_apps.get_model('td_maternal.subjectscreening')

    def encrypt_values(self, obj_dict=None, obj_cls=None):
        """Ecrypt values for fields that are encypted.
        """
        result_dict_obj = {**obj_dict}
        for key, value in obj_dict.items():
            for f in obj_cls._meta.get_fields():
                if key == f.name and type(f) in encrypted_fields:
                    new_value = f.field_cryptor.encrypt(value)
                    result_dict_obj[key] = new_value
        return result_dict_obj
    

    def fix_date_format(self, obj_dict=None):
        """Change all dates into a format for the export
        and split the time into a separate value.
        
        Format: m/d/y
        """

        result_dict_obj = {**obj_dict}
        for key, value in obj_dict.items():
            if isinstance(value, datetime.datetime):
                value = value.astimezone(timezone('Africa/Gaborone'))
                time_value = value.time().strftime('%H:%M:%S.%f')
                time_variable = key + '_time'
                value = value.strftime('%m/%d/%Y')
                result_dict_obj[key] = value
                result_dict_obj[time_variable] = time_value
            elif isinstance(value, datetime.date):
                value = value.strftime('%m/%d/%Y')
                result_dict_obj[key] = value
        return result_dict_obj

    def maternal_crf_data_dict(self, crf_obj=None):
        """Return a crf obj dict adding extra required fields.
        """

        data = crf_obj.__dict__
        data = self.encrypt_values(obj_dict=data, obj_cls=crf_obj.__class__)
        data.update(
            subject_identifier=crf_obj.maternal_visit.subject_identifier,
            visit_datetime=crf_obj.maternal_visit.report_datetime,
            last_alive_date=crf_obj.maternal_visit.last_alive_date,
            reason=crf_obj.maternal_visit.reason,
            survival_status=crf_obj.maternal_visit.survival_status,
            visit_code=crf_obj.maternal_visit.visit_code,
            visit_code_sequence=crf_obj.maternal_visit.visit_code_sequence,
            study_status=crf_obj.maternal_visit.study_status,
            appt_status=crf_obj.maternal_visit.appointment.appt_status,
            appt_datetime=crf_obj.maternal_visit.appointment.appt_datetime,
        )
        try:
            ae = self.antenatal_enrollment_cls.objects.get(subject_identifier=crf_obj.maternal_visit.subject_identifier)
        except self.antenatal_enrollment_cls.DoesNotExist:
            raise ValidationError('AntenatalEnrollment can not be missing')
        else:
            data.update(enrollment_hiv_status=ae.current_hiv_status)
        try:
            rs = self.rs_cls.objects.get(subject_identifier=crf_obj.maternal_visit.subject_identifier)
        except self.rs_cls.DoesNotExist:
            raise ValidationError('RegisteredSubject can not be missing')
        else:
            data.update(
                screening_age_in_years=rs.screening_age_in_years,
                registration_status=rs.registration_status,
                dob=rs.dob,
                gender=rs.gender,
                subject_type=rs.subject_type,
                registration_datetime=rs.registration_datetime,
            )
            try:
                maternal_rando = self.maternal_rando_cls.objects.get(
                    maternal_visit__subject_identifier=crf_obj.maternal_visit.subject_identifier)
            except self.maternal_rando_cls.DoesNotExist:
                data.update(
                    rx=None,
                    registration_datetime=None,
                    randomization_datetime=None
                )
            else:
                data.update(
                    rx=maternal_rando.rx,
                    randomization_datetime=maternal_rando.randomization_datetime
                )
        return data


    def infant_crf_data(self, crf_obj=None):
        """Return a dictionary for a crf object with additional participant information.
        """

        data = crf_obj.__dict__
        data = self.encrypt_values(obj_dict=data, obj_cls=crf_obj.__class__)
        data.update(
            subject_identifier=crf_obj.infant_visit.subject_identifier,
            visit_datetime=crf_obj.infant_visit.report_datetime,
            last_alive_date=crf_obj.infant_visit.last_alive_date,
            reason=crf_obj.infant_visit.reason,
            survival_status=crf_obj.infant_visit.survival_status,
            visit_code=crf_obj.infant_visit.visit_code,
            visit_code_sequence=crf_obj.infant_visit.visit_code_sequence,
            study_status=crf_obj.infant_visit.study_status,
            appt_status=crf_obj.infant_visit.appointment.appt_status,
            appt_datetime=crf_obj.infant_visit.appointment.appt_datetime,
        )
        try:
            rs = self.rs_cls.objects.get(subject_identifier=crf_obj.infant_visit.subject_identifier)
        except self.rs_cls.DoesNotExist:
            raise ValidationError('RegisteredSubject can not be missing')
        else:
            data.update(
                screening_age_in_years=rs.screening_age_in_years,
                registration_status=rs.registration_status,
                dob=rs.dob,
                gender=rs.gender,
                subject_type=rs.subject_type,
                registration_datetime=rs.registration_datetime,
                maternal_identifier=rs.relative_identifier
            )
        return data

    def non_crf_obj_dict(self, obj=None):
        """Return a dictionary of non crf object.
        """

        data = obj.__dict__
        data = self.encrypt_values(obj_dict=data, obj_cls=obj.__class__)
        subject_consent = self.subject_consent_csl.objects.filter(subject_identifier=obj.subject_identifier).last()
        if subject_consent:
            if not 'dob' in data:
                data.update(dob=subject_consent.dob)
            if not 'gender' in data:
                data.update(gender=subject_consent.gender)
            if not 'screening_identifier' in data:
                data.update(screening_identifier=subject_consent.screening_identifier)
            try:
                subject_screening = self.subject_screening_csl.objects.get(
                    screening_identifier=subject_consent.screening_identifier)
            except self.subject_screening_csl.DoesNotExist:
                raise ValidationError('Subject Screening can not be missing')
            else:
                data.update(
                    screening_age_in_years=subject_screening.age_in_years
                )
        else:
            if not 'screening_identifier' in data:
                data.update(screening_identifier=None)
            data.update(
                screening_age_in_years=None,
                dob=None,
                gender=None,
                
            )
        if not 'registration_datetime' in data:
            try:
                rs = self.rs_cls.objects.get(subject_identifier=obj.subject_identifier)
            except self.rs_cls.DoesNotExist:
                data.update(
                    registration_datetime=None,
                    screening_datetime=None
                )
            else:
                data.update(
                    registration_datetime=rs.registration_datetime,
                    screening_datetime=rs.screening_datetime
                )
        return data
