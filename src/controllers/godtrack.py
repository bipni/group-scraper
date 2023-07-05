from flask import request, jsonify
from services.FacebookGroupScraper import FacebookGroupScraper


class GodTrack:
    def facebook_group_scraper(self):
        group_id = request.form.get('group_id')
        cookies_file = request.files.get('name_of_cookies_file')
        name_of_cookies_file = cookies_file.filename

        facebookGroupScraper = FacebookGroupScraper()

        details = facebookGroupScraper.get_facebook_group_details(
            group_id, name_of_cookies_file, cookies_file)

        return (jsonify(dict(
            status=200,
            message="Group Details Scraped",
            details=details
        )), 200)
