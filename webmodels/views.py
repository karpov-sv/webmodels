from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.db.models import Avg, Min, Max, StdDev
from django.db import connections, transaction

from models import Models, Species, ObsFin, ObsCont

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

#from utils import permission_required_or_403

@transaction.commit_on_success
def db_query(string, params=None, db='default', debug=False):
    connection = connections[db]

    cursor = connection.cursor()
    result = None

    if debug:
        print cursor.mogrify(string, params)

    try:
        cursor.execute(string, params)
        result = cursor.fetchall()
    except:
        import traceback
        traceback.print_exc()
        pass
    finally:
        cursor.close()

    return result

def index(request):
    context = {}

    return TemplateResponse(request, 'index.html', context=context)

def models_list(request, sort='name'):
    context = {}

    models = Models.objects.all()

    if request.method == 'GET':
        sort = request.GET.get('sort', sort)
        ion = request.GET.get('ion')

    if sort:
        models = models.order_by(sort)

    if ion:
        models = models.extra(where=["%s = any(ions)"], params=[ion])

    context['models'] = models
    context['sort'] = sort
    context['ions'] = db_query("SELECT DISTINCT unnest(ions) as ion FROM models ORDER BY ion")

    return TemplateResponse(request, 'models_list.html', context=context)

def model_details(request, id=0):
    context = {}

    model = Models.objects.get(id=id)
    species = model.species_set.order_by('-rel_frac').filter(rel_frac__gt=0)
    ions = model.ions
    ions.sort()

    context['model'] = model
    context['species'] = species
    context['ions'] = ions

    return TemplateResponse(request, 'model_details.html', context=context)

def model_plot_select(request, lmin=3800, lmax=8000, id=0):
    context = {}

    model = Models.objects.get(id=id)

    if request.method == 'POST':
        lmin = float(request.POST.get('lmin', 3800))
        lmax = float(request.POST.get('lmax', 8000))

    context['model'] = model
    context['lmin'] = lmin
    context['lmax'] = lmax

    return TemplateResponse(request, 'model_plot.html', context=context)

def model_plot(request, id=0, lmin=3800, lmax=8000, mode='fin', size=800):
    model = Models.objects.get(id=id)

    if mode == 'fin':
        data = model.obsfin_set.order_by('lamb')
    else:
        data = model.obscont_set.order_by('lamb')

    if lmin:
        data = data.filter(lamb__gt=lmin)
    if lmax:
        data = data.filter(lamb__lt=lmax)

    lamb = [_.lamb for _ in data]
    flamb = [_.flambda for _ in data]

    fig = Figure(facecolor='white', figsize=(size/72, 400/72), tight_layout=True)
    ax = fig.add_subplot(111)
    ax.autoscale()

    ax.plot(lamb, flamb, '-')

    ax.set_xlabel("Wavelength, Angstroms")
    ax.set_ylabel("Specific Intensity")

    # 10% margins on both axes
    ax.margins(0.0, 0.1)

    if mode == 'fin':
        ax.set_title('%s' % model.name)
    else:
        ax.set_title('Continuum for %s' % model.name)

    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)

    return response
