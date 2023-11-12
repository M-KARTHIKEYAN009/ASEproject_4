
from django.contrib import admin
from django.urls import path
from election import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.election_landing_page,name='landing_page'),
    path('signup/admin/', views.AdminSignUpView.as_view(), name='admin_signup'),

    path('login/admin/', views.AdminLoginView.as_view(), name='admin_signup'),

    path('login/candidate/', views.CandidateLoginView.as_view(), name='candidate_signup'),

    path('login/voter/', views.VoterLoginView.as_view(), name='voter_signup'),
    # Candidate signup URL
    path('signup/candidate/', views.CandidateSignUpView.as_view(), name='candidate_signup'),


    # Voter signup URL
    path('signup/voter/', views.VoterSignUpView.as_view(), name='voter_signup'),

    path('member/admin/home/',views.admin_home,name='admin_home'),
    path('member/candidate/home/',views.candidate_dashboard,name='candidate_member_home'),
    path('member/voter/home/',views.voter_dashboard,name='voter_member_home'),
    path('all/candidates/',views.get_all_candidates_info,name='all_candidates'),
    path('all/voters/',views.get_all_voters_info,name='all_voters'),
    path('elections/new/', views.CreateElectionEventView.as_view(), name='create_election_event'),

    path('show/elections/', views.show_elections_info, name='elections_list'),
    path('cast/vote/<int:id>/', views.use_vote, name='cast_vote'),
    path('election/results/<int:id>/', views.show_election_results, name='election_results'),

    path('profile/update/', views.update_user_profile, name='update_user_profile'),

    path('verify/voter/<int:id>/',views. verify_voter, name='verify_voter'),
    path('verify/candidate/<int:id>/',views. verify_candidate, name='verify_candidate'),

    path('logout/', views.LogoutView.as_view(), name='logout'),
]
