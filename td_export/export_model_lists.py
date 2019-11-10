
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
    'maternalarvpostadh']

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
            'infantnvpadjustment']

infant_crf_list = [
            'infantbirthdata',
            'infantbirthexam',
            'infantbirthfeedingvaccine',
            'infantbirtharv',
            'infantnvpdispensing',
            'infantfu',
            'infantfuphysical',
            'infantfeeding',
            'infantnvpadjustment']

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
            ['solidfoodassessment', 'solid_foods', 'Foods'],
            ['solidfoodassessment', 'rations_receviced', 'Rations']
        ]

maternal_model_list = [
            'registeredsubject', 'specimenconsent', 'maternallocator',
            'maternalcontact', 'subjectconsent', 'antenatalvisitmembership', 
            'antenatalenrollment', 'appointment', 'subjectscreening']

maternal_many_to_many_crf = [
            ['maternalmedicalhistory', 'who', 'wcsdxadult'],
            ['maternalmedicalhistory', 'mother_chronic', 'chronicconditions'],
            ['maternalmedicalhistory', 'father_chronic', 'chronicconditions'],
            ['maternalmedicalhistory', 'mother_medications', 'maternalmedications'],
        ]
maternal_many_to_many_non_crf = [
    ['maternallabourdel', 'delivery_complications', 'deliverycomplications']]

infant_model_list = ['infantbirth', 'appointment']

offstudy_prn_model_list = ['maternaloffstudy', 'infantoffstudy']

death_report_prn_model_list = ['maternaldeathreport', 'infantdeathreport']
