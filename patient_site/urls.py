from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.HomePage.as_view(),name='home_page'),
    path('home/',views.HomePageLogged.as_view(),name='home_page_logged'),
    path('perscription/',views.PerscriptionPage.as_view(),name='perscription_page'),
    path('appointments/',views.AppointmentsPage.as_view(),name='appointments_page'),

    path('register/',views.RegisterPage.as_view(),name='register_page'),
    path('login/',views.LoginPage.as_view(),name='login_page'),
    path('logout/',views.Logout.as_view(),name='logout_req'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)