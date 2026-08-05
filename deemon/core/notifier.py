import logging
import platform
import smtplib
import ssl
from datetime import datetime, timedelta
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, formatdate

import pkgutil

from deemon import __version__
from deemon.core.config import Config as config
from deemon.utils.repo import get_github_repo_url

logger = logging.getLogger(__name__)

SAMPLE_ALBUMS = [
    {
        'artist': 'Daft Punk',
        'album': 'Discovery',
        'cover': 'https://cdn-images.dzcdn.net/images/cover/5718f7c81c27e0b2417e2a4c45224f8a/250x250-000000-80-0-0.jpg',
        'url': 'https://www.deezer.com/album/302127',
        'track_num': 14,
        'record_type': 'album',
    },
    {
        'artist': 'Starjunk 95',
        'album': 'Industrial Sunset Memories',
        'cover': 'https://cdn-images.dzcdn.net/images/cover/e86b8ad7e35c453d0e30183b1d918dff/250x250-000000-80-0-0.jpg',
        'url': 'https://www.deezer.com/us/album/877883752',
        'track_num': 15,
        'record_type': 'album',
    },
    {
        'artist': 'Levity',
        'album': 'Escapism Vol. 1',
        'cover': 'https://cdn-images.dzcdn.net/images/cover/34242071e568912b435bdba6e9309934/250x250-000000-80-0-0.jpg',
        'url': 'https://www.deezer.com/us/album/644769361',
        'track_num': 7,
        'record_type': 'album',
    },
    {
        'artist': 'S3RL',
        'album': 'Play It Loud',
        'cover': 'https://cdn-images.dzcdn.net/images/cover/4346bb5bd4087401b5ef9a4603fbc987/250x250-000000-80-0-0.jpg',
        'url': 'https://www.deezer.com/us/album/632821661',
        'track_num': 1,
        'record_type': 'single',
    },
    {
        'artist': 'Rick Astley',
        'album': 'The Best of Me',
        'cover': 'https://cdn-images.dzcdn.net/images/cover/1fcfca61ca4e05027612a1af865b2e03/250x250-000000-80-0-0.jpg',
        'url': 'https://link.deezer.com/s/341KFizIQ5HlVnNamEoAu',
        'track_num': 31,
        'record_type': 'album',
    },
    {
        'artist': 'deadmau5',
        'album': 'W:/2016ALBUM/',
        'cover': 'https://cdn-images.dzcdn.net/images/cover/35ac50100a4c47b3bfe7ea9278b7f54a/250x250-000000-80-0-0.jpg',
        'url': 'https://www.deezer.com/album/750162921',
        'track_num': 12,
        'record_type': 'album',
    },
]


def build_sample_releases(album_count: int = 1) -> list:
    """Build grouped sample release data for HTML email tests."""
    if album_count < 1:
        album_count = 1

    albums = []
    for i in range(album_count):
        album = SAMPLE_ALBUMS[i % len(SAMPLE_ALBUMS)].copy()
        if album_count > 1:
            album['album'] = f"{album['album']} #{i + 1}"
        albums.append(album)

    today = datetime.now()
    grouped = {}
    for i, album in enumerate(albums):
        # Spread albums across a few dates to exercise date headers.
        offset_days = (i // 2) * 7
        release_date = (today.replace(hour=0, minute=0, second=0, microsecond=0)
                        - timedelta(days=offset_days))
        date_key = release_date.strftime('%Y-%m-%d')
        grouped.setdefault(date_key, []).append(album)

    return [
        {'release_date': release_date, 'releases': release_list}
        for release_date, release_list in sorted(grouped.items(), reverse=True)
    ]


SAMPLE_RELEASES = build_sample_releases(1)


class Notify:

    def __init__(self, new_releases: list = None):
        logger.debug(f"Sending notification for {new_releases} release(s)")
        self.subject = "deemon Notification"
        self.releases = new_releases

    def send(self, body=None, test=False):
        """
        Send email notification message
        """
        if not all([config.smtp_server(), config.smtp_port(), config.smtp_user(),
                    config.smtp_pass(), config.smtp_sender(), config.smtp_recipient()]):
            if test:
                logger.info("   [!] Unable to send test notification. Please configure "
                            "email server settings and provide recipient address.")
            logger.debug("Email not configured, no notifications will be sent")
            return False

        if not body:
            body = self.html_message()

        context = ssl.create_default_context()

        logger.debug("Sending notification email")
        logger.debug(f"Using server: {config.smtp_server()}:{config.smtp_port()}")

        try:
            if config.smtp_starttls():
                with smtplib.SMTP(config.smtp_server(), config.smtp_port()) as server:
                    server.starttls()
                    server.login(config.smtp_user(), config.smtp_pass())
                    server.sendmail(config.smtp_sender(), config.smtp_recipient(), body.as_string())
            else:
                with smtplib.SMTP_SSL(config.smtp_server(), config.smtp_port(), context=context) as server:
                    server.login(config.smtp_user(), config.smtp_pass())
                    server.sendmail(config.smtp_sender(), config.smtp_recipient(), body.as_string())
        except Exception as e:
            if test:
                logger.error(f"   [!] Failed to send test notification: {e}")
            else:
                logger.error(f"Failed to send email notification: {e}")
            return False

        logger.debug("Email notification has been sent")
        if test:
            logger.info(f"   Test notification sent to {config.smtp_recipient()}")
        return True

    def construct_header(self, is_plain_text=True, subject=None):
        subject = subject or self.subject

        if is_plain_text:
            message = EmailMessage()
        else:
            message = MIMEMultipart('mixed')

        message['To'] = config.smtp_recipient()
        message['From'] = formataddr(('deemon', config.smtp_sender()))
        message['Subject'] = subject
        message['Date'] = formatdate(localtime=True)

        return message

    def html_message(self):
        """
        Builds HTML messages
        """
        html_body = MIMEText(self.html_new_releases(), 'html')
        msg = self.construct_header(is_plain_text=False)
        msg.attach(html_body)
        return msg

    def test(self):
        """
        Verify SMTP settings by sending test email
        """
        msg = self.construct_header(subject="deemon Test Notification")
        msg.set_content("Congrats! You'll now receive new release notifications.")
        self.send(msg, test=True)

    def test_html(self, album_count: int = 1):
        """
        Send a test email using the HTML new-release notification template.
        """
        self.releases = build_sample_releases(album_count)
        if album_count > 1:
            self.subject = f"deemon Test Notification (HTML, {album_count} albums)"
        else:
            self.subject = "deemon Test Notification (HTML)"
        self.send(test=True)

    def expired_arl(self):
        """
        Notify user of expired ARL
        """
        msg = self.construct_header(subject="deemon - ARL expired")
        msg.set_content("Your ARL has expired. Please update your ARL to receive new releases.")
        self.send(msg)

    def expired_sub(self):
        """
        Notify user of expired subscription
        """
        msg = self.construct_header(subject="deemon - Subscription expired")
        msg.set_content("Your Deezer subscription appears to have expired.")
        self.send(msg)

    def plaintext_message(self) -> str:
        """
        Plaintext version of email to send
        """
        message = "The following new releases were detected:\n\n"
        for release in self.releases:
            release_date_ts = datetime.strptime(release["release_date"], "%Y-%m-%d")
            release_date_str = datetime.strftime(release_date_ts, "%A, %B %-d")
            message += f"\n{release_date_str}\n"
            for album in release["releases"]:
                message += f"+ {album['artist']} - {album['album']}\n"
        return message

    def html_new_releases(self):

        app_version = f"deemon {__version__}"
        py_version = f"python {platform.python_version()}"
        sys_version = f"{platform.system()} {platform.release()}"

        new_release_list_spacer = f"""
            </ul>
            <p style="font-size: 14px; line-height: 140%;">&nbsp;</p>
        """

        all_new_releases = ""

        self.releases = sorted(self.releases, key=lambda x: x['release_date'], reverse=True)

        new_release_count = 0
        
        for release in self.releases:

            if all_new_releases != "":
                all_new_releases += new_release_list_spacer

            release_date_ts = datetime.strptime(release["release_date"], "%Y-%m-%d")
            release_date_str = datetime.strftime(release_date_ts, "%A, %B %d").replace(" 0", " ")

            new_release_list_header = f"""
			<div class="album date" style="background-color:#f0f0f0; color:#6106e5; flex:0 0 100%; width:100%;">
				<span class="album date badge" style="color:#6106e5; border:1px solid #6106e5;">
					{release_date_str}
				</span>
			</div>
            """

            new_release_list_item = ""

            for album in release["releases"]:
                new_release_count += 1
                if album['record_type'].lower() == "ep":
                    record_type = "EP"
                else:
                    record_type = album['record_type'].title()
            
                if not album['track_num']:
                    album_info = record_type
                else:
                    album_info = f"{record_type} | {album['track_num']} track(s)"
            
                new_release_list_item += f"""
            <div class="album body" style="background-color:#f0f0f0; color:#404040; overflow:hidden; min-width:350px; margin:0 0 30px 0; box-sizing:border-box;">
				<table class="album-row" role="presentation" cellpadding="0" cellspacing="0" border="0" style="width:100%; border-collapse:collapse; table-layout:fixed;">
					<tr>
						<td class="albumart" width="150" style="width:150px; max-width:150px; height:150px; max-height:150px; vertical-align:top; padding:0 20px 0 0; overflow:hidden;">
							<a href="{album['url']}" style="display:block; width:150px; height:150px; overflow:hidden; line-height:0; text-decoration:none;">
								<img src="{album['cover']}" alt="" width="150" height="150" style="width:150px !important; height:150px !important; max-width:150px !important; max-height:150px !important; display:block; border:0; border-radius:7px; object-fit:cover;">
							</a>
						</td>
						<td class="albuminfo" style="vertical-align:top; color:#404040; word-wrap:break-word; overflow-wrap:anywhere;">
							<div class="albumtitle" style="color:#404040; font-weight:bold; margin-top:5px;">
								<a href="{album['url']}" style="color:#2f7a40; text-decoration:none;">{album['album']}</a>
							</div>
							<div class="artistname" style="color:#404040; font-style:italic; padding-bottom:10px;">{album['artist']}</div>
							<span style="color:#404040;">{album_info}</span>
						</td>
					</tr>
				</table>
			</div>
                """

            all_new_releases += new_release_list_header + new_release_list_item

        if new_release_count > 1:
            self.subject = f"{str(new_release_count)} new releases found!"
        else:
            self.subject = f"1 new release found!"
        
        html_output = pkgutil.get_data('deemon', 'assets/index.html').decode('ascii')
        
        if config.update_available():
            html_output = html_output.replace("{UPDATE_MESSAGE}", f"Update to v{config.update_available()} is now available!")
        else:
            html_output = html_output.replace("{UPDATE_MESSAGE}", "")
            html_output = html_output.replace("{VIEW_UPDATE_MESSAGE}", "display:none;")

        html_output = html_output.replace("{NEW_RELEASE_COUNT}", str(new_release_count))
        html_output = html_output.replace("{NEW_RELEASE_LIST}", all_new_releases)
        html_output = html_output.replace("{DEEMON_VER}", app_version)
        html_output = html_output.replace("{PY_VER}", py_version)
        html_output = html_output.replace("{SYS_VER}", sys_version)
        html_output = html_output.replace("{GITHUB_REPO_URL}", get_github_repo_url())

        return html_output
