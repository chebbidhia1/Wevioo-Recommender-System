from django.urls import path
from . import views


urlpatterns = [
    path('accounts/login',views.login,name='login'),
    path('adminIndex',views.adminIndex,name='adminIndex'),
    path('userIndex',views.userIndex,name='userIndex'),
    path('penderation',views.pendarationBack,name='penderation'),
    path('logout',views.logout,name='logout'),
    path('allCandidates',views.allCandidates,name='all'),
    path('cosineRecommendation',views.cosine,name='cosine'),
    path('similariteProfile',views.similarity,name='similarity'),
    path('differenceRecommendation',views.difference,name='difference'),
    path('similariteInterne',views.internalSimilarity,name='interne'),
    path('euclideanRecommendation',views.euclidean,name='euclidean'),
    path('decision',views.decision,name='decision'),
    path('scoringRecommendation',views.scoring,name='scoring')
]
