from django.shortcuts import render
from django import shortcuts
from django.core.files.storage import FileSystemStorage
from  django.contrib import messages
from detection_app.Detector import calcul_score_apk
from detection_app.virus_total_scan import virus_total_scan
from os import path
from pfe_plateforme_web.settings import MEDIA_DIR



# Create your views here.

def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        if myfile.name.split('.')[-1]=='apk':
            filename = fs.save(myfile.name, myfile)
            # url de l'apk chargée
            uploaded_apk_url = fs.url(filename)
            # Lancer la detection
            svm_scan_result= calcul_score_apk(path.join(MEDIA_DIR,myfile.name))
            svm_scan_result['file_name'] = myfile.name
            # VirusTotal scan
            # virus_total_dict= virus_total_scan(myfile.name, path.join(MEDIA_DIR,myfile.name))
            # svm_scan_result.update(virus_total_dict)
            # Résultat dans la page result.html , svm_scan_result is a dictionary
            return render(request, 'result.html', svm_scan_result)
        else:
            messages.error(request, "Veuillez charger un fichier .apk !")
           # return render(request, "detection_app/index.html",{'message':'Veuillez charger un fichier .apk !'})

    return render(request, "index.html")
