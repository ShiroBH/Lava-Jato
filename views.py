from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from .models import Dados
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet



# Create your views here.
def login(request):
    if request.method == "GET":     
        return render(request, 'lavajato/login.html')
    else:
        
        username = request.POST.get('cpf') 
        senha = request.POST.get('DataN')

        user = authenticate(username=username, password=senha)
        if user:
            login_django(request, user)

            return redirect('index/')
        else:
            return HttpResponse('usuario não encontrado')
        
def register(request):
    # No formulario foi definido que ele teria o metodo post
    # aqui eu coloco um if se ele for get a pagina entra normal se nao ele faz o cadastro
    # se ele for post ele vai pegar todos os dados
    # ele pega utilizando o "request.POST.get("nome do elemento")" e o coloca em uma variavel

    if request.method == "GET":     
        return render(request, 'lavajato/register.html')
    else:
        username = request.POST.get('cpf')
        DataN = request.POST.get('DataN')
        email = request.POST.get('email')
        nome = request.POST.get('nome')
        cargo = request.POST.get('cargo')
        foto = request.POST.get('foto')
        
        # verifica se o cpf ja esta em uso 
        user = User.objects.filter(username=username).first()

        if user:
            # caso ele exista esse codigo o informará
            return HttpResponse('ja existe um usuario com esse cpf')
        # caso nao ele ira criar um novo, com o cpf sendo o username e a senha a data de nascimento
        user = User.objects.create_user(username=username, password=DataN)
        user.save()
        dado = Dados.objects.create(cpf=username, email=email, DataN=DataN, nome=nome, cargo=cargo, foto=foto)
        return redirect('http://127.0.0.1:8000/index/')
    
# tela principal apos ser autenticado ele sera mandado para ca
@login_required(login_url='/')
def index(request):
    return render(request, 'pages/index.html')

# Tela de dados - Aqui para baixo irei buscar os dados do django-admin e jogar na tela

@login_required(login_url='/')
def perfil(request):
    dados = Dados.objects.filter(cpf=str(request.user.username))
    return render(request, "pages/perfil.html", {"perfil":dados})

@login_required(login_url='/')
def carteirinha(request):
    dados = Dados.objects.filter(cpf=str(request.user.username))
    return render(request, "pages/carteirinha.html", {"carteirinha":dados})

@login_required(login_url='/')

def generate_pdf(request):
    if request.method == 'POST':
        # Vai capturar o que foi digitado

        my_list = request.POST.getlist('my_list')
        nome_pdf = request.POST.get('nome_pdf')
        cpf_pdf = request.POST.get('cpf_pdf')
        data_nascimento_pdf = request.POST.get('data_nascimento_pdf')
        cargo_pdf = request.POST.get('cargo_pdf')


        buffer = io.BytesIO()

        # Crie um objeto PDF, usando o buffer como o "arquivo"
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        # Definir o conteúdo do PDF
        styles = getSampleStyleSheet()
        content = []
        content.append(Paragraph(nome_pdf, styles['Heading1']))
        content.append(Paragraph(cpf_pdf, styles['Normal']))
        content.append(Paragraph(data_nascimento_pdf, styles['Normal']))
        content.append(Paragraph(cargo_pdf, styles['Normal']))
        for item in my_list:
            content.append(Paragraph(my_list, styles['Normal']))

        # Cria o PDF
        doc.build(content)

        # Obter o valor do buffer e gravar na resposta
        pdf = buffer.getvalue()
        buffer.close()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=lava_jato.pdf'
        return response
    else:
        # Render the form template
        return render(request, 'my_form.html')
