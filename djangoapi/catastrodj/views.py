# Create your views here.
#Django imports
from django.http import JsonResponse
from django.views import View


#My imports
from core.myLib.geometryTools import WkbConversor, GeometryChecks

from catastrodj import models
from catastrodj.operations.prediodj import insert,delete, selectallAsDicts, update, selectAsDicts
from catastrodj.operations.callesdj import insert as insert_calles ,delete, selectallAsDicts, update, selectAsDicts

class HelloCatastrodj(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "HelloCatastrodj. Hello world", "data":[request.GET.dict()]})
    def post(self, request):
        return JsonResponse({"ok":True,"message": "HelloCatastrodj. Hello world", "data":[request.POST.dict()]})

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
        d=request.GET.dict()
        d = {"id": id}
        r=selectAsDicts(d)
        return JsonResponse(r)