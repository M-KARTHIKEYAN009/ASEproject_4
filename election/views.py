from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import ElectionUser,ElectionVote,ElectionEvent
from .forms import ElectionUserCreationForm,ElectionVoterCandidateCreationForm
from django.contrib.auth import login


class AdminSignUpView(generic.CreateView):
    model = ElectionUser
    form_class = ElectionUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('admin_home')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Log the user in
        print("coming to this screen")
        print("user pk", str(user.pk))
        print(user.is_active)
        print(user.is_superuser)
        print(user.username)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return redirect(self.success_url)

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView


from django.contrib.auth import logout
from django.views import View

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('landing_page')
class AdminLoginView(LoginView):
    template_name = 'admin_user_login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('admin_home')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            return render(self.request, self.template_name, {
                'form': form,
                'error_message': 'Invalid credentials or not an admin user.'
            })

class CandidateLoginView(LoginView):
    template_name = 'candidate_user_login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('candidate_member_home')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'candidate'
        return super().get_context_data(**kwargs)
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            return render(self.request, self.template_name, {
                'form': form,
                'error_message': 'Invalid credentials or not an admin user.'
            })

class VoterLoginView(LoginView):
    template_name = 'voter_user_login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('voter_member_home')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'voter'
        return super().get_context_data(**kwargs)
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            return render(self.request, self.template_name, {
                'form': form,
                'error_message': 'Invalid credentials or not an admin user.'
            })
def admin_home(request):
    if request.user.is_active:
        return render(request,'admin_member_home.html')

def voter_dashboard(request):
    voter = UserProfile.objects.filter(account=request.user).first()
    if not voter:
        return redirect('voter_signup')
    return render(request, 'voter_member_home.html', {'voter': voter})

def candidate_dashboard(request):
    candidate = UserProfile.objects.filter(account=request.user).first()
    if not candidate:
        return redirect('candidate_signup')
    return render(request, 'candidate_member_home.html',{'candidate':candidate})
class CandidateSignUpView(generic.CreateView):
    model = ElectionUser
    form_class = ElectionVoterCandidateCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('candidate_member_home')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'candidate'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_candidate = True
        user.save()
        try:
            UserProfile.objects.get_or_create(account=user)
        except:
            pass
        login(self.request, user)  # Log the user in
        return redirect(self.success_url)

class VoterSignUpView(generic.CreateView):
    model = ElectionUser
    form_class = ElectionVoterCandidateCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('voter_member_home')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'voter'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_voter = True
        user.save()
        try:
            UserProfile.objects.get_or_create(account=user)
        except:
            pass
        login(self.request, user)  # Log the user in
        return redirect(self.success_url)

from .models import UserProfile
def get_all_candidates_info(request):
    candidates = UserProfile.objects.filter(account__is_candidate=True)
    return render(request,'candidates_info.html',{'candidates':candidates})

def election_landing_page(request):
    return render(request,'election_landing_page.html')
def verify_candidate(request, id):
    candidate = UserProfile.objects.filter(pk=id).first()
    # Check if a candidate was updated, which implies it existed and was not verified before
    if candidate:
        candidate.is_validated = True
        candidate.candidate_unique_id = "CANDIDATE"+str(candidate.pk)
        candidate.save()
    return redirect('all_candidates')



def verify_voter(request, id):
    voter = UserProfile.objects.filter(pk=id).first()
    # Check if a candidate was updated, which implies it existed and was not verified before
    if voter:
        voter.is_validated = True
        voter.voter_unique_id = "VOTER" + str(voter.pk)
        voter.save()
    return redirect('all_voters')

def get_all_voters_info(request):
    voters = UserProfile.objects.filter(account__is_voter=True)
    return render(request,'voters_info.html',{'voters':voters})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ElectionEvent, UserProfile, ElectionVote


@login_required  # Ensure that only logged-in users can access this view
def show_elections_info(request):
    # Retrieve all upcoming or current elections
    elections = ElectionEvent.objects.all()

    # Get the current user's profile
    # It is assumed that each user has only one profile.
    current_user_profile = UserProfile.objects.filter(account=request.user).first()

    # Iterate over each election to check if the user has already voted
    for election in elections:
        # Check if a vote exists for the current user in the current election
        user_has_voted = ElectionVote.objects.filter(voter=current_user_profile, election=election).exists()

        # Set an attribute on the election object to indicate if the vote has been utilized
        election.vote_cast = user_has_voted  # Renamed 'is_vote_utilized' to 'vote_cast' for clarity

    # Render the elections page with the context containing elections
    # The template can use 'election.vote_cast' to display if the vote is utilized or not
    return render(request, 'elections.html', {'elections': elections})


from django.shortcuts import render, redirect
from django.views import View
from .forms import ElectionEventForm

class CreateElectionEventView(View):
    form_class = ElectionEventForm
    template_name = 'create_election_event.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a new URL, for example to the list of elections
            return redirect('elections_list')
        return render(request, self.template_name, {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm,VoterUserProfileForm

@login_required
def update_user_profile(request):
    # Ensure that only candidates can access this view
    print(request.user.is_voter)
    if not request.user.is_candidate and not request.user.is_voter:
        return redirect('home')

    # Get the UserProfile associated with the current user
    user_profile, created = UserProfile.objects.get_or_create(account=request.user)

    if request.method == 'POST':
        if request.user.is_voter:
            form = VoterUserProfileForm(request.POST, request.FILES, instance=user_profile)
        else:
            form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            if request.user.is_candidate:
                return redirect('candidate_member_home')
            return redirect('voter_member_home')
    else:
        if request.user.is_voter:
            form = VoterUserProfileForm(instance=user_profile)
        else:
            form = UserProfileForm(instance=user_profile)

    return render(request, 'user_profile_form.html', {
        'form': form
    })


def use_vote(request, id):
    election = ElectionEvent.objects.filter(pk=id).first()
    candidates = UserProfile.objects.filter(account__is_candidate=True,is_validated=True)

    voter = UserProfile.objects.filter(account=request.user).first()
    if not voter:
        return redirect('elections_list')
    if ElectionVote.objects.filter(election=election, voter=voter):

        return redirect('elections_list')
    if request.method == "POST":
        candidate_id = request.POST["candidate"]
        candidate = UserProfile.objects.filter(pk=candidate_id).first()
        voting, voting_flag = ElectionVote.objects.get_or_create(candidate=candidate, voter=voter,
                                                         election=election)
        return redirect('elections_list')
    return render(request, 'submit_vote.html',
                  {'election': election, 'candidates': candidates, 'voter': voter})


from django.db.models import Count, Sum


def show_election_results(request, id):
    election = ElectionEvent.objects.filter(pk=id).first()
    total_votes = ElectionVote.objects.filter(election=election).count()
    results = ElectionVote.objects.filter(election=election).order_by(
        "candidate").values("candidate__account__first_name",
                            "candidate__pk",
                            'candidate__gender',
                            'candidate__residence',
                            'candidate__candidate_unique_id',
                            'candidate__dob',
                            "election__name", "election__date_of_election",
                            "candidate__account__last_name").annotate(
        the_count=Count("candidate"))
    if not results:
        return redirect('admin_home')
    maximum_votes = max(r["the_count"] for r in results)
    winner_candidate_id = ''
    for result in results:
        result["voting_perc"] = float(result["the_count"]) / float(total_votes) * 100
        if maximum_votes == float(result["the_count"]):
            winner_candidate_id = result["candidate__pk"]
    election.is_completed = True
    if winner_candidate_id:
        winner = UserProfile.objects.filter(pk=winner_candidate_id).first()
        election.victor = winner
        msg = str(winner.account.first_name) + " " + str(winner.account.last_name) + " won the election " + str(
            election.name)
        election.additional_notes = msg
        election.has_concluded = True
    election.save()
    return render(request, 'show_final_election_results.html',
                  {'results': results, 'total_votes': total_votes, 'maximum_votes': maximum_votes})