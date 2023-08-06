from django.core.mail import EmailMultiAlternatives
from django.conf import settings


class ChangelogEmail:
    pass


class EmailManager:
    from_email = settings.CHANGELOG_FROM_EMAIL

    def send(self, commits, humans):
        if commits.exclude(body__isnull=True):
            html_content = self.get_html(commits)
            msg = EmailMultiAlternatives(
                'Updates auf dem {} Server'.format(commits[0].branch.name),
                self.get_text(commits),
                self.from_email,
                bcc=self.bcc_from_humans(humans)
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        self.mark_commits_as_sent(commits)

    def bcc_from_humans(self, humans):
        return [human.email for human in humans]

    def get_text(self, commits):
        text_content = '''
        Guten Tag,
        Auf dem {} Server gab es folgende Updates:
        '''.format(commits[0].branch.name)

        for commit in commits:
            text_content += '''
            * {} - {} - {} - {}
            '''.format(
                commit.hash,
                commit.head,
                commit.body,
                commit.tag_name,
            )
        return text_content

    def get_html(self, commits):
        commit_rows = ''
        for commit in commits:
            if not commit.body:
                continue
            commit_rows += '''
            <tr>
                <th style="border-top:1px solid grey;text-align:left;">Titel:</th>
                <td style="border-top:1px solid grey;text-align:left;">{}</td>
                <th style="border-top:1px solid grey;text-align:left;">Id:</th>
                <td style="border-top:1px solid grey;text-align:left;">{}</td>
            </tr>
            <tr>
                <td colspan=4 style="border-top:1px dotted lightgrey;text-align:left;padding-bottom:10px;">{}</td>
            </tr>
            '''.format(
                commit.head,
                commit.hash,
                commit.body if commit.body else '',
            )

        return '''
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                <title></title>
                <style></style>
            </head>
            <body>
                <table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">
                    <tr>
                        <td align="center" valign="top">
                            <table border="0" cellpadding="20" cellspacing="0" width="100%" id="emailContainer">
                                <tr>
                                    <td align="left" valign="top" style="padding-bottom: 0;">
                                        <p>Guten Tag,</p>
                                        <p>Auf dem {} Server gab es folgende Updates:</p>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center" valign="top">
                                        <table align="left" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%">
                                            {}
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </body>
        </html>
        '''.format(
            commits[0].branch.name,
            commit_rows,
        )

    def mark_commits_as_sent(self, commits):
        commits.update(executed=True)
