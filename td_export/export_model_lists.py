exclude_fields = [
    'created', '_state', 'hostname_created', 'hostname_modified', 'revision',
    'device_created', 'device_modified', 'id', 'site_id', 'created_time',
    'modified_time', 'report_datetime_time', 'registration_datetime_time',
    'screening_datetime_time', 'modified', 'form_as_json', 'consent_model',
    'randomization_datetime', 'registration_datetime', 'is_verified_datetime',
    'first_name', 'last_name', 'initials', 'guardian_name', 'identity',
    'infant_visit_id', 'maternal_visit_id', 'processed', 'processed_datetime',
    'packed', 'packed_datetime', 'shipped', 'shipped_datetime',
    'received_datetime', 'identifier_prefix', 'primary_aliquot_identifier',
    'clinic_verified', 'clinic_verified_datetime', 'drawn_datetime']

maternal_crfs_list = [
    'maternalultrasoundinitial',
    'maternalobstericalhistory',
    'maternaldemographics',
    'maternallifetimearvhistory',
    'maternalclinicalmeasurementsone',
    'maternalrando',
    'maternalinterimidcc',
    'maternalclinicalmeasurementstwo',
    'rapidtestresult',
    'maternaldiagnoses',
    'maternalsubstanceusepriorpreg',
    'maternalpostpartumdep',
    'maternalpostpartumfu',
    'maternalcontraception',
    'maternalsrh',
    'maternalsubstanceuseduringpreg',
    'maternalhivinterimhx',
    'maternalarvpostadh',
    'maternalrecontact']

maternal_inlines_dict = {
    'maternalarvpreg': ['maternalarv', 'maternal_arv_preg_id'],
    'maternalarvpost': ['maternalarvpostmed', 'maternal_arv_post_id']
}

infant_crf_list = [
    'infantbirthdata',
    'infantbirthexam',
    'infantbirthfeedingvaccine',
    'infantbirtharv',
    'infantnvpdispensing',
    'infantfu',
    'infantfuphysical',
    'infantfeeding',
    'infantnvpadjustment',
    'karabooffstudy']

karabo_infant_crf_list = ['karabooffstudy']

infant_inlines_dict = {
    'infantcongenitalanomalies': [[
        'infantcns',
        'infantfacialdefect',
        'infantcleftdisorder',
        'infantmouthupgi',
        'infantcardiodisorder',
        'infantrespiratorydefect',
        'infantlowergi',
        'infantfemalegenital',
        'infantmalegenital',
        'infantrenal',
        'infantmusculoskeletal',
        'infantskin',
        'infanttrisomies',
        'infantotherabnormalityitems'], 'congenital_anomalies_id'],
    'infantbirthfeedingvaccine': [['infantvaccines'], 'infant_birth_feed_vaccine_id'],
    'infantfudx': [['infantfudxitems'], 'infant_fu_dx_id'],
    'infantfuimmunizations': [['vaccinesmissed', 'vaccinesreceived'], 'infant_fu_immunizations_id'],
    'infantfunewmed': [['infantfunewmeditems'], 'infant_fu_med_id'],
    'infantarvproph': [['infantarvprophmod'], 'infant_arv_proph_id']}

infant_many_to_many_crf = [
    ['infantcovidscreening', 'covid_symptoms', 'covidsymptoms'],
    ['solidfoodassessment', 'solid_foods', 'Foods'],
    ['solidfoodassessment', 'rations_receviced', 'Rations'],
    ['karabotuberculosishistory', 'coughing_rel', 'CoughingRelation'],
    ['karabotuberculosishistory', 'fever_rel', 'FeverRelation'],
    ['karabotuberculosishistory', 'weight_loss_rel', 'WeightLossRelation'],
    ['karabotuberculosishistory', 'night_sweats_rel', 'NightSweatsRelation'],
    ['karabotuberculosishistory', 'diagnosis_rel', 'DiagnosisRelation'],
]

maternal_model_list = [
    'registeredsubject', 'specimenconsent', 'maternallocator',
    'maternalcontact', 'subjectconsent', 'antenatalvisitmembership',
    'antenatalenrollment', 'appointment', 'subjectscreening', 'karabosubjectscreening',
    'karabosubjectconsent']

karabo_maternal_model_list = [
    'karabosubjectscreening',
    'karabosubjectconsent']

maternal_many_to_many_crf = [
    ['maternalcovidscreening', 'covid_symptoms', 'covidsymptoms'],
    ['maternalmedicalhistory', 'who', 'wcsdxadult'],
    ['maternalmedicalhistory', 'mother_chronic', 'chronicconditions'],
    ['maternalmedicalhistory', 'father_chronic', 'chronicconditions'],
    ['maternalmedicalhistory', 'mother_medications', 'maternalmedications'],
]

maternal_many_to_many_non_crf = [
    ['maternallabourdel',
     'delivery_complications',
     'deliverycomplications']]

infant_model_list = ['infantbirth', 'appointment']

offstudy_prn_model_list = ['maternaloffstudy', 'infantoffstudy']

death_report_prn_model_list = ['maternaldeathreport', 'infantdeathreport']
