from django.shortcuts import render
from ProgInt.models import Kalorie
import sqlite3
from bokeh.io import output_file, show
from bokeh.palettes import Spectral6
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from django.http import HttpResponse
from django.utils.translation import ugettext as _

def glowna(request):
    from django.utils import translation
    #user_language='en'
    #translation.activate(user_language)
    #request.session[translation.LANGUAGE_SESSION_KEY]=user_language
    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]
    contex={}
    return render(request, "ProgInt/index.html")
def tempob(request2):
    context2 = {}
    if request2.method == "POST":
        kilometry = int(request2.POST.get("dyst_km"))
        metry = int(request2.POST.get("dyst_m"))
        godziny = int(request2.POST.get("time_h"))
        minuty = int(request2.POST.get("time_m"))
        sekundy = int(request2.POST.get("time_s"))
        czas = godziny*3600+minuty*60+sekundy
        dytans = kilometry*1000+metry
        tempod = ((czas/dytans)*1000)/60
        dziesietna = tempod-int(tempod)
        if dziesietna*0.6<0.1:

            tempo=(str(int(tempod))+":0"+str(round((dziesietna*0.6)*100)))
        else:
            tempo=(str(int(tempod))+":"+str(round((dziesietna*0.6)*100)))
        speed=round((dytans/czas)*3.6,3)
        context2["speed"]=speed
        context2["tempo"] = tempo
        return render(request2, "ProgInt/index.html", context2)
    else:
        return render(request2, "ProgInt/index.html", context2)
def licz(request):
    context = {}
    if request.method == "POST":
        waga = float(request.POST.get("waga"))
        wzrost = float(request.POST.get("wzrost"))
        wiek = int(request.POST.get("wiek"))
        plec = str(request.POST.get("plec"))
        bmi = (waga/((wzrost/100)**2))
        context["bmi"] = round(bmi, 2)
        if bmi < 16:
            state = _("WYGŁODZENIE!!")
        elif bmi > 16 and bmi < 17:
            state = _("wychudzenie")
        elif bmi > 17 and bmi < 18:
            state = _("niedowaga")
        elif bmi > 18 and bmi < 25:
            state = _("świetnie, tak trzymaj")
        elif bmi > 25 and bmi < 30:
            state = _("nadwaga, uważaj")
        elif bmi > 30 and bmi < 35:
            state = _("I sotpień otyłości!")
        elif bmi > 35 and bmi < 40:
            state = _("II stopień otyłości!!")
        elif bmi > 40:
            state = _("SKRAJNA OTYŁOŚĆ!!!")
        context["state"] = state
        if plec == "K":
            need = 665.1+9.567*waga+1.85*wzrost-4.68*wiek
            chory = 1.2*need
            blekka = 1.3*need
            lekka = 1.5*need
            srednia = 1.6*need
            duza = 1.9*need
            bduza = 2.1*need
        elif plec == "M":
            need = 66.47+13.7*waga+5*wzrost-6.76*wiek
            chory = 1.2*need
            blekka = 1.3*need
            lekka = 1.6*need
            srednia = 1.7*need
            duza = 2.1*need
            bduza = 2.4*need
        if Kalorie.objects.count != 0:
            Kalorie.objects.all().delete()
        Kalorie.objects.create(chory=round(chory), blekka=round(blekka), lekka=round(
            lekka), srednia=round(srednia), duza=round(duza), bduza=round(bduza))

        opis = [_('o.chora'), _('bardzo lekka '), _('lekka'),_('średnia'), _('duża'), _('bardzo duża')]
        wartosci = Kalorie.objects.values()
        for i in wartosci:
            counts = [i['chory'], i['blekka'], i['lekka'],
                      i['srednia'], i['duza'], i['bduza']]
        source = ColumnDataSource(
            data=dict(opis=opis, counts=counts, color=Spectral6))
        p = figure(
            x_range=opis,
            plot_height=380,
            plot_width=360,
            tools=""
        )

        p.vbar(
            x='opis',
            top='counts',
            width=0.9,
            color='color',
            source=source,

        )
        p.xaxis.axis_label = _("Aktywność")
        p.yaxis.axis_label = _("Kalorie")
        p.xgrid.grid_line_color = None
        script, div = components(p)
        context["script"] = script
        context["div"] = div
        return render(request, "ProgInt/index.html", context)

    else:
        if Kalorie.objects.count != 0:
            Kalorie.objects.all().delete()
        return render(request, "ProgInt/index.html", context)



