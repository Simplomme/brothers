from django.http import HttpResponse
from io import BytesIO
from django.template.loader import get_template,render_to_string
#from xhtml2pdf import pisa
from weasyprint import HTML
import tempfile

def render_to_pdf(template_src,filename,context_dict={}):
    #template =get_template(template_src)
    #html =template.render(context_dict)

    #result = BytesIO()
    #pisa_status = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    #result.seek(0)
    #if not pisa_status.err:
    #    return result
    #else:
    #    return None
    html_string = render_to_string(template_src, context_dict)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename='+filename
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.TemporaryFile(delete=True) as output:
        output.write(result)
        #output.flush()
        #output.close()
        #output = open(output.name, 'r')
        output.seek(0)
        response.write(output.read())

    return response
