from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import (
     Designer, Moderator, Admin
) 
from studio.models import (
    Project, Category, MainCategory
)
from blog.models import Post
from django.conf import settings
from django.http import (
    HttpResponse, JsonResponse
)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point
from django.core.serializers import serialize
from django.contrib.auth import get_user_model
from django.db.models import Q
from firebase_admin.messaging import Message
from fcm_django.models import FCMDevice
from student.models import StudentProject
from firebase_admin import messaging, credentials
import firebase_admin
from .models import AboutImage, AboutNote, Resource
User = get_user_model()
from dashboard.models import PressNote

# firebase_credentials = credentials.Certificate(
#     settings.GOOGLE_APPLICATION_CREDENTIALS)
# firebase_app = firebase_admin.initialize_app(firebase_credentials)


def press(request):
    press = PressNote.objects.all()
    return render(request, 'home/press.html', {
        'press': press,    
        })

def resources(request):
    resources = Resource.objects.all()
    return render(request, 'home/resources.html', {
        'resources': resources
    })

def send_message():
    message_obj = Message(
    data={
        "Nick" : "Mario",
        "body" : "great match!",
        "Room" : "PortugalVSDenmark"
    },
   
    )
    return message_obj

# You can still use .filter() or any methods that return QuerySet (from the chain)
    device = FCMDevice.objects.all().first()
# send_message parameters include: message, dry_run, app
    device.send_message(message_obj)
    


def error_404(request, exception):
    data = {}
    return render(request,'home/404.html', data)


def search(request):
    designers = None
    projects = None
    users = None
    categories = None
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(Q(last_name__icontains=query) | Q(first_name__icontains=query))
        projects = Project.objects.filter(Q(name__icontains=query))
        categories = Category.objects.filter(Q(name__icontains=query))

    return render(request, 'home/search.html', {
        'users': users,
        'projects': projects,
        'query': query,
        'categories': categories
    })
    

def index(request):
    projects = Project.objects.order_by('-created')
    users = User.objects.order_by('first_name')
    latest_projects = Project.objects.select_related().order_by('-created')[0:4]
    blog_posts = Post.objects.select_related().order_by('-created')
    categories = Category.objects.order_by('name')
    return render(request, 'home/index.html', {
              'latest_projects': latest_projects,
              'site_posts': blog_posts,
              'users': users,
              'projects': projects,
              'categories': categories
    })

def about(request):
    notes = AboutNote.objects.order_by('created')
    return render(request, 'home/about.html', {
        'notes': notes
    })

def contact(request):
    return render(request, 'home/contact.html', {

    })

def user_profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    return render(request, 'home/user_profile.html', {
        'user': user
    })


def article_detail(request, article_pk):
    projects = Project.objects.order_by('-created')
    article = get_object_or_404(AdminPost, pk=article_pk)
    other_articles = AdminPost.objects.exclude(pk=article.pk)
    if request.method == 'POST':
        form = ArticleCommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('home:article_detail', article.pk)
    else:
        form = ArticleCommentForm()
    return render(request, 'home/article_detail.html',
                  {
                      'article': article,
                      'comment_form': form,
                      'other_articles': other_articles,
                      'projects': projects,
                      'categories': Category.objects.order_by('-name')
                  }
    )


def directory(request):
    users = User.objects.order_by('first_name').exclude(is_student=True)
    main_categories = MainCategory.objects.order_by('name')
    categories = Category.objects.order_by('name')
    return render(request, 'home/directory.html', {
        'users': users ,
        'main_categories': main_categories,
        'categories': categories,

    })


def directory_category(request, category_pk):
    main_categories = MainCategory.objects.order_by('name')
    category = get_object_or_404(Category, pk=category_pk)
    categories = Category.objects.exclude(pk=category.pk)
    return render(request, 'home/directory.html', {
        'category': category,
        'main_categories': main_categories ,
        'categories': categories,
    })


@csrf_exempt
def dir_filter(request):
    country = None
    main_categories = MainCategory.objects.order_by('name')
    categories = Category.objects.order_by('name')
    if request.method == 'POST' and request.is_ajax():
        term = request.POST.get('term')
        if term == 'country':
            country = term
            return render(request, 'home/directory.html', {
                'country': country,
                'categories': categories,
                'main_categories': main_categories
            })
        elif term == 'name':
            return redirect(request, 'home:directory'
            )


def admcopyright(request):
    return render(request, 'home/copyright.html')

@csrf_exempt
def nearby_view(request):
    f_list= []
    fdata = dict()
    if request.method == 'POST' and request.is_ajax:
        kms = float(request.POST['kms'])
        clat = float(request.POST['clat'])
        clng = float(request.POST['clng'])
        coords = Point((clng, clat))
        nearby = serialize('json', queryset=User.objects.filter(location__distance_lte=(coords, Distance(km=kms))))
        for i in nearby:
            f_list.append(i)
        return HttpResponse(f_list, content_type='application/json')


def ethnicity_filter(request, verb=None):
    black = None
    colored = None
    african = None
    indigenous = None
    african_american = None
    paragon = None
    multiracial = None
    result = ''
    if verb == 'black':
        black = User.objects.filter(ethnicity='Black')
    elif verb == 'colored':
        colored = User.objects.filter(ethnicity='Colored')
    elif verb == 'african':
        african = User.objects.filter(ethnicity='African')
    elif verb == 'indigenous':
        indigenous = User.objects.filter(ethnicity='Indigenous')
    elif verb == 'african-american':
        african_american = User.objects.filter(ethnicity='African-American')
    elif verb == 'paragon':
        paragon = User.objects.filter(is_paragon=True)
    elif verb == 'multiracial':
        african = User.objects.filter(ethnicity='Multiracial')
    else:
        result = '{} Not Found. Please Choose Another Filter'
    return render(request, 'home/filtered.html', {
        'black': black,
        'colored': colored,
        'african': african,
        'african_american': african_american,
        'paragon': paragon, 
        'result': result,
        'verb': verb
    })

def gender_filter(request, verb=None):
    male = None
    female = None
    other_gender = None
    if verb == 'male':
        male = User.objects.filter(gender='Male')
    elif verb == 'female':
        female = User.objects.filter(gender='Female')
    elif verb == 'other-gender':
        other_gender = User.objects.filter(gender='Other')
    return render(request, 'home/filtered.html', {
        'male': male,
        'female': female,
        'other_gender': other_gender,
        'verb': verb
    })


def other_filter(request, verb=None):
    
    paragon = None
    creative_type = None
    if verb == 'paragon':
        paragon = User.objects.filter(is_paragon=True)
    creative_type = Project.objects.filter(category__name=verb)
    return render(request, 'home/filtered.html', {
        'creative_type': creative_type,
        'paragon': paragon,
        'verb': verb
    })

def filter_paragon(request, verb=None):
    paragon = None
    if verb == 'paragon':
        paragon = User.objects.filter(is_paragon=True)
    return render(request, 'home/filtered.html', {
        'paragon': paragon,
        'verb': verb
    })

def student_project_detail(request, project_pk):
    project = get_object_or_404(StudentProject, pk=project_pk)
    return render(request, 'home/student_project_detail.html', {
        'student_project': project
    })
