from django.db import models
from django.conf import settings
from git import Repo
from changelog.email import EmailManager


class Branch(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'


class Human(models.Model):
    name = models.CharField('Name', max_length=150)
    email = models.EmailField('E-Mail', max_length=150)
    # subscription = models.OneToOneField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    master = models.BooleanField(default=False)
    beta = models.BooleanField(default=False)

    def __str__(self):
        return '{} <{}>'.format(self.name, self.email)

    class Meta:
        verbose_name = 'Mensch'
        verbose_name_plural = 'Menschen'


class Commit(models.Model):
    hash = models.CharField('Id', max_length=40)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    head = models.CharField('Titel', max_length=150)
    body = models.TextField('Beschreibung', null=True, blank=True)
    created_by = models.ForeignKey(Human, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Übermittlungsdatum', null=True, blank=True)
    tag_name = models.CharField('Tag-Name', max_length=150, null=True, blank=True)
    executed = models.BooleanField('Übermittelt', help_text='Wurde dieser Comit bereits in einer E-Mail versendet?', default=False)

    @classmethod
    def get_unexecuted(cls, branch):
        return cls.objects.filter(executed=False, branch__name=branch)

    @classmethod
    def get_unexecuted_tags(cls, branch):
        return cls.get_unexecuted(branch).exclude(tag_name__isnull=True)

    def __str__(self):
        return '{}'.format(self.hash)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('hash', 'branch')


class Git(Repo):
    """ object = Git(path=repository_dir) """
    repository_dir = settings.BASE_DIR

    def __init__(self, *args, **kwargs):
        kwargs['path'] = self.repository_dir
        super().__init__(*args, **kwargs)

    def refresh(self):
        """ hash branch head body created_by created_at tag_name """
        for branch in self.get_branches_names():
            result = list(self.get_commit_objects(branch))

    def get_commit_objects(self, branch='master'):
        """ hash branch head body created_by created_at tag_name """
        commits = self.get_commits(branch)
        tagged_commits = self.get_tagged_commits(branch)
        branch_obj = Branch.objects.get_or_create(name=branch)[0]
        for commit in commits:
            human = Human.objects.update_or_create(
                email=commit.committer.email,
                defaults={
                    'name': commit.committer.name,
                }
            )[0]
            if '\n' in commit.message:
                head, body = commit.message.split('\n', 1)
            else:
                head, body = commit.message, None
            commit_kwargs = {
                #'hash': commit.hexsha,
                #'branch': branch_obj,
                'head': head[:150].strip('\n'),
                'body': body.strip('\n') if body else None,
                'created_by': human,
                'created_at': commit.authored_datetime,
                'tag_name': tagged_commits.get(commit.hexsha),
            }

            yield Commit.objects.update_or_create(
                hash=commit.hexsha,
                branch=branch_obj,
                defaults=commit_kwargs
            )[0]

    def get_commits(self, branch='master'):
        """ return [commit_id] """
        return self.iter_commits(branch)

    def get_tagged_commits(self, branch='master'):
        """ return [commit_id] """
        return {tag.commit.hexsha: tag for tag in self.tags}

    def get_branches_names(self):
        return [branch.name for branch in self.get_branches()]

    def get_branches(self):
        return self.branches


class ActionBase:
    def action(self, commits_to_send):
        humans = self.get_humans()
        self.send_email(commits=commits_to_send, humans=humans)

    def send_email(self, commits, humans):
        if humans and commits:
            EmailManager().send(commits, humans)


class MasterAction(ActionBase):
    def get_humans(self):
        return Human.objects.filter(master=True)


class BetaAction(ActionBase):
    def get_humans(self):
        return Human.objects.filter(beta=True)


class Changelog:
    """ Interface for Git and Actions"""
    git = Git()
    try:
        active_branch = git.active_branch
        active_branch_name = active_branch.name
    except TypeError:
        pass

    @classmethod
    def run_actions(cls):
        """ execute actions """
        cls.git.refresh()
        cls.dispatch()

    @classmethod
    def dispatch(cls):
        if cls.active_branch_name == 'master' and cls.get_unexecuted_tags('master'):
            MasterAction().action(cls.get_unexecuted_commits('master'))
        elif cls.active_branch_name == 'beta':
            BetaAction().action(cls.get_unexecuted_commits('beta'))

    @classmethod
    def get_unexecuted_tags(cls, branch):
        """ returns CommitQuerySet with executed=False and tag_name==True """
        return Commit.get_unexecuted_tags(branch)

    @classmethod
    def get_unexecuted_commits(cls, branch):
        """ returns Commit QuerySet with executed=False """
        return Commit.get_unexecuted(branch)
