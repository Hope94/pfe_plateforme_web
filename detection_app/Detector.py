import os
import traceback
from training_app.module_apprentissage.apk import APK
from training_app.module_apprentissage.feature_extractor_dex import extract_dex_features
from training_app.module_apprentissage.feature_extractor_manifest import extract_manifest_features
from detection_app.droidsec_manager import  get_features_weight,get_all_paramatere
from pfe_plateforme_web.settings import MEDIA_DIR
from datetime import datetime

def calcul_score_apk(apk_path: str)->dict:
    svm_result = {'scan_datetime': datetime.now()}
    apk = APK(apk_path,"")
    apk.score =0
    paramater = get_all_paramatere()

    svm_result ['threshold']=  paramater['threshold']
    try:
        # Extraction des caractéristiques
        # extract_dex_features(apk)
        extract_manifest_features(apk)
        svm_result['permissions'] = apk.get_manifest_features().get_permissions()
        svm_result['activities'] = apk.get_manifest_features().get_activities()
        svm_result['services'] = apk.get_manifest_features().get_services()
        svm_result['receivers'] = apk.get_manifest_features().get_receivers()
        svm_result['providers'] = apk.get_manifest_features().get_providers()
        # Formatter les caractéristiques : type::name dans une liste apk_feature
        features = apk.get_dex_features().get_features()
        features.extend(apk.get_manifest_features().get_features())
        apk_feature = [ feature['feature_type'] + "::" + feature['feature_name'] for feature in features ]
        weights = get_features_weight(apk_feature)
        svm_result['feature_weight'] =  weights
        # additionner weights
        for value in weights.values():
            apk.score += value
        # Add intercept

        apk.score += paramater['intercept']
        apk.malignity= apk.score>paramater['threshold']
        svm_result['app_score'] = apk.score
        svm_result['malignity'] = apk.malignity
        if apk.malignity:
            svm_result['relatif_score'] = (apk.score / paramater['sumMalignantFeatures']) * 100
        else:
            svm_result['relatif_score'] = (apk.score / paramater['sumBenignFeatures']) * 100
        return svm_result
    except Exception as exception:
        print('Error for APK ' + apk.get_name())
        traceback.print_exc()

# apk_path = os.path.join(MEDIA_DIR,'Mobile-antiMalware.apk')
# print(apk_path)
# calcul_score_apk(apk_path)
