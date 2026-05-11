# Create your views here.
#Django imports
from django.http import JsonResponse
from django.views import View

## A ver si funciona
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
##Si no borramos

#My imports
from core.myLib.geometryTools import WkbConversor, GeometryChecks

from catastrodj import models
from catastrodj.operations.prediodj import insert,delete, selectallAsDicts, update, selectAsDicts
from catastrodj.operations.callesdj import insert as insert_c ,delete as delete_c, selectallAsDicts as selectallAsDicts_c, update as update_c, selectAsDicts as selectAsDicts_c
from catastrodj.operations.iglesiasdj import insert as insert_i ,delete as delete_i, selectallAsDicts as selectallAsDicts_i, update as update_i, selectAsDicts as selectAsDicts_i


class HelloCatastrodj(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "HelloCatastrodj. Hello world", "data":[request.GET.dict()]})
    def post(self, request):
        return JsonResponse({"ok":True,"message": "HelloCatastrodj. Hello world", "data":[request.POST.dict()]})

# Clase Predios. 
class PrediosInsert(View):
    def post(self, request):
        d=request.POST.dict()
        r=insert(d)
        return JsonResponse(r)

class PrediosDelete(View):
    def post(self, request):
        d=request.POST.dict()
        r=delete(d)
        return JsonResponse(r)
    
    ##Con el id desde la URL
class PrediosDelete2(View):
    def post(self, request, id):
        d = {"id": id}
        r = delete(d)
        return JsonResponse(r)

#GET por que solo estamos seleccionando
class PrediosSelectAll(View):
    def get(self, request):
        r = selectallAsDicts()
        return JsonResponse(r)
    
class PrediosUpdate(View):
    def post(self, request):
        d=request.POST.dict()
        r=update(d)
        return JsonResponse(r)

class PrediosSelectAsDicts(View):
    def get(self, request, id):
        d = {"id": id}
        r=selectAsDicts(d)
        return JsonResponse(r)
    
#Clases Calles
class CallesInsert(View):
    def post(self, request):
        d=request.POST.dict()
        r=insert_c(d)
        return JsonResponse(r)

class CallesDelete(View):
    def post(self, request, id):
        d = {"id": id}
        r = delete_c(d)
        return JsonResponse(r)

#GET por que solo estamos seleccionando
class CallesSelectAll(View):
    def get(self, request):
        r = selectallAsDicts_c()
        return JsonResponse(r)
    
class CallesUpdate(View):
    def post(self, request):
        d = request.POST.dict()
        # Si el ID no viene en el body, lo puedes forzar desde la URL:
        if 'id' not in d:
            d['id'] = id
        r = update_c(d)
        return JsonResponse(r)

class CallesSelectAsDicts(View):
    def get(self, request, id):
        d = {"id": id}
        r=selectAsDicts_c(d)
        return JsonResponse(r)
    
#Clases Iglesias
class IglesiasInsert(View):
    def post(self, request):
        d=request.POST.dict()
        r=insert_i(d)
        return JsonResponse(r)

class IglesiasDelete(View):
    def post(self, request, id):
        d = {"id": id}
        r = delete_i(d)
        return JsonResponse(r)

#GET por que solo estamos seleccionando
class IglesiasSelectAll(View):
    def get(self, request):
        r = selectallAsDicts_i()
        return JsonResponse(r)
    
class IglesiasUpdate(View):
    def post(self, request):
        d = request.POST.dict()
        # Si el ID no viene en el body, lo puedes forzar desde la URL:
        if 'id' not in d:
            d['id'] = id
            
        r = update_i(d)
        return JsonResponse(r)

class IglesiasSelectAsDicts(View):
    def get(self, request, id):
        d=request.GET.dict()
        d = {"id": id}
        r=selectAsDicts_i(d)
        return JsonResponse(r)
    