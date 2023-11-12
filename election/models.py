from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

# Choices constants for the application
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

USA_STATE_CHOICES = (
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
)

POLITICAL_PARTY_CHOICES = (
    ('CON', 'Congress'),
    ('REP', 'Republican Party'),
    ('DEM', 'Democratic Party'),
    ('LIB', 'Libertarian Party'),
    ('GRE', 'Green Party'),
    ('IND', 'Independent'),
    ('SOC', 'Socialist Party'),
    ('UNA', 'Unaffiliated'),
    ('OTH', 'Other'),
)

# Custom user model extending AbstractUser to include election system specific fields
from django.contrib.auth.models import AbstractUser
from django.db import models

class ElectionUser(AbstractUser):
    is_candidate = models.BooleanField(default=False)
    is_voter = models.BooleanField(default=False)
    phone = models.CharField(max_length=10, blank=True, null=True, help_text='Contact phone number of the user.')
    registration_date = models.DateTimeField(auto_now_add=True, help_text='Timestamp when the user was registered.')
    updated_date = models.DateTimeField(auto_now=True, help_text='Timestamp when the user profile was last updated.')
    dob = models.DateField(null=True, blank=True, help_text='Date of birth.')
    # Add related_name for groups and user_permissions to avoid clashing with the User model
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="electionuser_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="electionuser_user_permissions",
        related_query_name="user",
    )

    def __str__(self):
        role = 'Candidate' if self.is_candidate else 'Voter'
        return f"{self.username} ({role})"


# Profile model for additional details for both candidates and voters
class UserProfile(models.Model):
    account = models.OneToOneField(ElectionUser, on_delete=models.CASCADE, related_name='profile')
    dob = models.DateField(null=True, blank=True, help_text='Date of birth.')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, help_text='Gender of the person.')
    residence = models.TextField(null=True, blank=True, help_text='Residential address.')
    party = models.CharField(max_length=50, choices=POLITICAL_PARTY_CHOICES, null=True, blank=True, help_text='Political party affiliation.')
    id_document = models.ImageField(
        upload_to='user_docs',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        null=True,
        blank=True,
        help_text='Identity document image.'
    )
    biography = models.TextField(null=True, blank=True, help_text='Biographical information for the candidate.')
    is_validated = models.BooleanField(default=False, help_text='Flag to indicate if the profile has been verified.')
    faulty_account = models.BooleanField(default=False, help_text='Flag to indicate if the account has inconsistencies.')
    candidate_unique_id = models.CharField(max_length=30,null=True)
    voter_unique_id = models.CharField(max_length=30,null=True)
    def __str__(self):
        return f"{self.account.get_full_name()} - {'Candidate' if self.account.is_candidate else 'Voter'} Profile"

# Model to manage election details
class ElectionEvent(models.Model):
    name = models.CharField(max_length=200, help_text='Title of the election event.')
    date_of_election = models.DateField(help_text='Scheduled date for the election.')
    voting_start_time = models.TimeField(help_text='Time when voting starts.')
    voting_end_time = models.TimeField(help_text='Time when voting ends.')
    result_announcement_date = models.DateField(help_text='Scheduled date for announcing results.')
    additional_notes = models.TextField(null=True, blank=True, help_text='Any additional notes related to the election.')
    has_concluded = models.BooleanField(default=False, help_text='Status to indicate if the election has concluded.')
    victor = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_elections', help_text='The winning candidate of the election.')

    def __str__(self):
        return f"{self.name} (Date: {self.date_of_election})"

# Model to record votes cast in an election
class ElectionVote(models.Model):
    candidate = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='votes_received', help_text='Candidate who received the vote.')
    voter = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='votes_cast', help_text='Voter who cast the vote.')
    election = models.ForeignKey(ElectionEvent, on_delete=models.CASCADE, related_name='votes', help_text='Election in which the vote was cast.')
    timestamp = models.DateTimeField(auto_now_add=True, help_text='Timestamp when the vote was recorded.')

    def __str__(self):
        return f"Vote by {self.voter.account.username} for {self.candidate.account.username} in {self.election.name}"
