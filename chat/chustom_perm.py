from datetime import datetime
from .models import Signature
from .serailizer import signature_Serlizer
from dateutil.relativedelta import relativedelta
def check_perm( id , sign):
    print(id , sign)
    sinn = Signature.objects.filter(user= id, sign= sign )
    if sinn.exists():
        sinn_Serlizer= signature_Serlizer(sinn , many=True).data
        timeStr = sinn_Serlizer[0]['expires_at'][:-6]
        objDate = datetime.strptime(timeStr, '%Y-%m-%dT%H:%M:%S.%f')
        if  objDate>datetime.now()-relativedelta(minutes=30):
            print(True,'yyyy')
            return True
        else:
            return False
    else:
        return False