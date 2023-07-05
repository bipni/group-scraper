import pandas as pd
import datetime
import facebook_scraper as fs
import os
from os.path import exists
import csv
import getpass


class FacebookGroupScraper:
    def get_facebook_group_details(self, group_id: str, name_of_cookies_file: str, cookies_file, page_count: int = 1):
        os_name = os.name
        os_user = getpass.getuser()

        # for ubuntu
        if os_name == 'posix':
            base_path = f'/home/{os_user}/Documents/scraper-files'
        # for windows
        elif os_name == 'nt':
            base_path = f'C:/Users/{os_user}/Documents/scraper-files'
        else:
            pass

        if not exists(base_path):
            os.makedirs(base_path)

        if cookies_file:
            cookies_file.save(base_path + '/' + name_of_cookies_file)

        details = []

        # initialize name of csv file
        name_of_posts_csv = base_path + '/' + group_id + '.csv'

        # Get Posts

        # Get date filter from CSV file

        # check if csv file exists and deduce the earliest time checkpoint for posts to be scraped
        if exists(name_of_posts_csv):
            # ingest saved data
            df = pd.read_csv(name_of_posts_csv,
                             header=0)
            if len(df) > 0:
                # change data type of time column to datetime from string
                df['time'] = pd.to_datetime(
                    df['time'], format='%Y-%m-%d %H:%M:%S')

                # sort rows by time
                df.sort_values(by='time', ascending=False, inplace=True)
                # create time checkpoint based on the latest date time
                time_checkpoint = df.tail(1)['time'].values[0]
                # convert time checkpoint to int timestamp (1e9 second) from numpy datetime64 format
                time_checkpoint = time_checkpoint.astype(datetime.datetime)
                # convert time checkpoint to datetime (not numpy datetime64) timestamp from integer
                time_checkpoint = datetime.datetime.fromtimestamp(
                    time_checkpoint / 1e9)
            # if for some reason, the csv has headers but no rows, the most current timestamp would be the earliest time checkpoint
            else:
                time_checkpoint = datetime.datetime.now()
        else:
            # if the csv file doesn't exist, the most current timestamp would be the earliest time checkpoint
            time_checkpoint = datetime.datetime.now()

        # Filter for rows you will keep, Scrape posts from groups, append rows to csv

        # Filter for rows you will keep, Scrape posts from groups, append rows to csv
        # create empty list where every post will be appended
        posts = []
        MAX_COMMENTS = True

        # initialize list of headers which we shall be checking the post row for
        post_level_headers = ['original_request_url', 'post_url', 'post_id', 'text', 'post_text', 'shared_text',
                              'original_text', 'time', 'timestamp', 'image', 'image_lowquality', 'images',
                              'images_description', 'images_lowquality', 'images_lowquality_description',
                              'video', 'video_duration_seconds', 'video_height', 'video_id', 'video_quality',
                              'video_size_MB', 'video_thumbnail', 'video_watches', 'video_width', 'likes',
                              'comments', 'shares', 'link', 'links', 'user_id', 'username', 'user_url',
                              'is_live', 'factcheck', 'shared_post_id', 'shared_time', 'shared_user_id',
                              'shared_username', 'shared_post_url', 'available', 'comments_full', 'reactors',
                              'w3_fb_url', 'reactions', 'reaction_count', 'with', 'page_id', 'sharers', 'image_id',
                              'image_ids', 'was_live', 'header', 'share_post_id', 'post_with']

        # set up a counter to show the person operating this notebook, how many posts have been scraped so far
        counter = 0

        # # initialize empty list of all posts
        # all_posts = []
        # run a for loop where the we loop through every post and append it to the empty list
        for post in fs.get_posts(group=group_id,
                                 #  credentials=(f'{email}' ,f'{password}'),
                                 cookies=base_path + '/' + name_of_cookies_file,
                                 pages=page_count):

            # ignore the posts that were before the earliest post saved
            if post['time'] < time_checkpoint:

                # # append post_urls to all_posts (for debugging purposes)
                # all_posts.append(post['post_url'])

                # # initialize empty list where all reply level data will be appended
                # all_comments_and_replies = [] # for debugging purposes
                # loop through all replies, comments and posts and append reply level data to empty list
                for row in fs.get_posts(
                    post_urls=[post['post_url']],
                    # credentials=(f'{email}' ,f'{password}'),
                    cookies=base_path + '/' + name_of_cookies_file,
                    options={"comments": MAX_COMMENTS,
                             "reactors": True, "progress": True}
                ):
                    # initialize an empty placeholder for a  copy dictionary for the post
                    # so you don't have to handle exceptions
                    # when keys change from one post to another
                    copy_dict = {}

                    # make sure all posts, comments and replies have the same number of headers by loopingthrough all
                    for post_header in post_level_headers:
                        if post_header in list(row.keys()):
                            # pass
                            # make a copy dictionary so that you don't have to handle exceptions
                            # when they keys don't match from one post to another
                            copy_dict[post_header] = row[post_header]
                        else:
                            # post[post_header] = None
                            copy_dict[post_header] = None

                    # # append post to all_comments_and_replies to check for debug purposes
                    # all_comments_and_replies.append(copy_dict)

                    # if CSV file exists, ignore headers and only add rows
                    if exists(name_of_posts_csv):
                        with open(name_of_posts_csv, 'a', newline='', encoding="utf-8") as f:
                            writer = csv.DictWriter(
                                f, fieldnames=copy_dict.keys())
                            writer.writerow(copy_dict)
                    else:
                        with open(name_of_posts_csv, 'a', newline='', encoding="utf-8") as f:
                            writer = csv.DictWriter(
                                f, fieldnames=copy_dict.keys())
                            writer.writeheader()
                            writer.writerow(copy_dict)

                    # show the person operating this notebook how many rows we have written into the csv file
                    counter = counter + 1
                    print("Count of new rows added to file: ", counter)
                    details.append(copy_dict)

            # if the post was published after the earliest time checkpoint,
            # we shall ignore it and move on because it has already been recorded in the csv file
            else:
                pass

        return details
