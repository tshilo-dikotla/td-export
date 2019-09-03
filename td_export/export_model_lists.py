
maternal_crfs_list = [
#     'maternalultrasoundinitial',
#     'maternalobstericalhistory',
#     'maternalmedicalhistory',
#     'maternaldemographics',
#     'maternallifetimearvhistory',
#     'maternalclinicalmeasurementsone',
#     'maternalrando',
#     'maternalinterimidcc',
#     'maternalclinicalmeasurementstwo',
#     'rapidtestresult',
#     'maternaldiagnoses',
#     'maternalsubstanceusepriorpreg',
#     'maternalpostpartumdep',
#     'maternalpostpartumfu',
#     'maternalcontraception',
#     'maternalsrh',
#     'maternalsubstanceuseduringpreg',
#     'maternalhivinterimhx',
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
            ['SolidFoodAssessment', 'solid_foods', 'Foods'],
            ['SolidFoodAssessment', 'rations_receviced', 'Rations']
        ]

maternal_model_list = [
            'registeredsubject', 'specimenconsent', 'maternallocator',
            'maternalcontact', 'subjectconsent', 'antenatalvisitmembership', 
            'antenatalenrollment']

maternal_many_to_many_crf = [
            ['maternallabourdel', 'delivery_complications', 'deliverycomplications'],
        ]

infant_model_list = ['infantbirth']

offstudy_prn_model_list = ['MaternalOffStudy', 'InfantOffStudy']

death_report_prn_model_list = ['MaternalDeathReport', 'InfantDeathReport']
