from PIL import Image, ImageFont, ImageDraw
from datetime import datetime, timedelta
import calendar
from math import ceil
import csv
import os

# ini
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0
import codecs

# instagram
import io
import getpass

# facebook
import requests
import json

# naver
import xmlrpc.client

# dropbox
import dropbox

###############

pil_bg = Image.open('res/empty.png')
width, height = pil_bg.size

# fonts, coordinate and other definitions#{{{
titlebox_height = 405
bodybox_height = height-titlebox_height

max_body_line = 14

title_day_y = 39
title_date_y = 248

body_time_x = 50
body_content_x = 225

font_title_day = ImageFont.truetype('res/NanumBarunpenR.ttf', 180)
font_title_date = ImageFont.truetype('res/NanumBarunpenR.ttf', 100)
font_title_date_page = ImageFont.truetype('res/NanumBarunpenR.ttf', 70)
fill_title_day = (255,255,255,255)
fill_title_date = (0,0,0,255)
font_body = ImageFont.truetype('res/NanumBarunGothicLight.ttf', 55)
font_body_bold = ImageFont.truetype('res/NanumBarunGothicBold.ttf', 55)
font_body_discount = ImageFont.truetype('res/NanumBarunpenR.ttf', 37)
fill_body = (0,0,0,255)
fill_body_name = (0,0,255,255)    # name of musical or play
fill_body_discount_rect = (234,104,162,255)
fill_body_discount = (255,255,255,255)

textheight_body = font_body.getsize("한국어")[1]
text_space = 10            # space between lines
line_height = textheight_body + text_space


cover_week_y = 880
font_cover = ImageFont.truetype('res/NanumBarunGothicUltraLight.ttf', 100)
fill_cover = (0,0,0,255)
korean_counter = ["첫", "둘", "셋", "넷", "다섯"]
### #}}}

def week_of_month(dt):#{{{
    """ Returns the week of the month for the specified date.
    """

    first_day = dt.replace(day=1)

    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom/7.0))#}}}
def write_center(draw, y, text, font, fill, width_of_img = width):#{{{
    """ Draws center-aligned text.
    """
    text_width = font.getsize(text)[0]
    draw.text(((width_of_img-text_width)/2,y), text, font=font, fill=fill)#}}}

# read csv file
csv_content = []
with open('input.csv', 'r', encoding='ANSI') as input_csv:
    rdr = csv.reader(input_csv)
    for line in rdr:
        csv_content.append(line)
first_date = csv_content[0][0]
del csv_content[0]
print("Starting date: " + str(first_date))

# separate the list by days.
start_idx = 0
day_by_day = []
for i, line in enumerate(csv_content):
    if line[0].upper() == 'N':
        day_by_day.append(csv_content[start_idx:i])
        start_idx = i+1
day_by_day.append(csv_content[start_idx:])

# format first day
first_datetime = datetime.strptime(first_date, '%Y%m%d')

###
# make content pages
print("Generating content pages..")

page = 1
date = first_datetime
for day_content in day_by_day:
    # one day can contain several pages. split the content by pages.
    day_pages = []
    nb_page = int(ceil(float(len(day_content)) / max_body_line))
    idx = 0
    for i in range(nb_page):
        if all(not e for e in day_content[idx]):    # if all strings are empty
            idx += 1    # do not include the first element

        if not day_content[idx][0]:            # if no time information at first line
            j = 1
            while not day_content[idx-j][0]:    # backward time search
                j += 1
            day_content[idx][0] = day_content[idx-j][0]

        if i == nb_page-1:    # if last page
            day_pages.append(day_content[idx:])
        else:
            day_pages.append(day_content[idx:idx+max_body_line])
            idx += max_body_line
    
    # format day and date string
    str_day = calendar.day_name[date.weekday()].upper()
    str_date = '{d.month}/{d.day}'.format(d=date)

    # make page and save.
    for page_num, day_page in enumerate(day_pages):
        pil_day = pil_bg.copy()
        draw = ImageDraw.Draw(pil_day)

        # draw header
        write_center(draw, title_day_y, str_day, font=font_title_day, fill=fill_title_day)
        if len(day_pages) > 1:    # if more than 1 page
            str_page = "-(%d)" % (page_num+1)
            date_width = font_title_date.getsize(str_date)[0]
            date_page_width = date_width + font_title_date_page.getsize(str_page)[0]
            title_date_x = (width - date_page_width)/2
            draw.text((title_date_x, title_date_y), str_date, font=font_title_date, fill=fill_title_date)
            draw.text((title_date_x + date_width, title_date_y+27), str_page, font=font_title_date_page, fill=fill_title_date)
        else:
            write_center(draw, title_date_y, str_date, font=font_title_date, fill=fill_title_date)

        # calculate position coordinate
        multiline_text_height = line_height * len(day_page) - text_space
        body_y = titlebox_height + (bodybox_height - multiline_text_height) / 2

        # draw body
        for i, line in enumerate(day_page):
            cursor_y = body_y + i*line_height
            if line[0]:
                draw.text((body_time_x, cursor_y), line[0], font=font_body_bold, fill=fill_body)
            cursor_x = body_content_x
            if line[1]:
                draw.text((cursor_x, cursor_y), line[1], font=font_body, fill=fill_body)
                cursor_x += font_body.getsize(line[1] + " ")[0]
            if line[2]:
                str_draw = "<" + line[2] + ">"
                draw.text((cursor_x, cursor_y), str_draw, font=font_body_bold, fill=fill_body_name)
                cursor_x += font_body_bold.getsize(str_draw + " ")[0]
            if line[3]:
                draw.text((cursor_x, cursor_y), line[3], font=font_body, fill=fill_body)
                cursor_x += font_body.getsize(line[3] + " ")[0]
            if line[4]:
                text_width = font_body_discount.getsize(line[4])[0]
                draw.rectangle([cursor_x, cursor_y, cursor_x + text_width + 18, cursor_y + textheight_body + 1], fill = fill_body_discount_rect)
                draw.text((cursor_x+10, cursor_y+4), line[4], font=font_body_discount, fill=fill_body_discount)

        # save a page
        pil_day.convert('RGB').save('%d.jpg' % page, quality=100)
        pil_day.close()
        page += 1

    # increase day
    date += timedelta(days=1)

#pil_first.save('output1.png')
pil_bg.close()

###
# make first cover page
print("Generating cover page..")

pil_cover = Image.open('res/cover.png')
draw = ImageDraw.Draw(pil_cover)

monthrange = calendar.monthrange(first_datetime.year,first_datetime.month)[1]
if monthrange - first_datetime.day < 2:        # if less than or equal to 2 days are in the month
    cover_month = first_datetime.month + 1
    cover_week = 1
else:
    cover_month = first_datetime.month
    cover_week = week_of_month(first_datetime)

str_week_of_month = korean_counter[cover_week - 1]
str_month_week = "%d월 %s째 주" % (cover_month, str_week_of_month)
write_center(draw, cover_week_y, str_month_week, font=font_cover, fill=fill_cover)

pil_cover.convert('RGB').save('0.jpg', quality=100)
pil_cover.close()

print("Processing done!")
print()

###############################################################
print("Getting ready to upload to SNS..")
print()

last_datetime = date - timedelta(days=1)
str_date_range = ' ({first.month}/{first.day}~{last.month}/{last.day})'.format(first=first_datetime, last=last_datetime)

config = ConfigParser()
config.readfp(codecs.open('config.ini', 'r', 'utf-8-sig'))    # UTF-8 with BOM
sns_caption = config.get('sns', 'icon') + str_month_week + str_date_range + "\n"
sns_caption += config.get('sns', 'caption') + "\n\n"
sns_caption += config.get('sns', 'hashtags') + " "
print('\t'.join(("\t" + sns_caption).splitlines(True)))
print()

sns_hashtags = input("Enter additional hashtags: ")
sns_caption += sns_hashtags

print()
print('\t'.join(("\t" + sns_caption).splitlines(True)))
print()

token_config = ConfigParser()
token_config.read('access_token.ini')    # ANSI


###
# Instagram
print('Uploading to Instagram..')
from InstagramAPI import InstagramAPI
media = []  # Albums can contain between 2 and 10 photos/videos.

for p in range(page):
    # find jpg files and add to album
    file_to_add = '%d.jpg' % p
    media.append({'type':'photo', 'file': file_to_add})

insta_userid = token_config.get('id', 'instagram')
print()
print("User ID: " + insta_userid)
insta_password = getpass.getpass()
ig = InstagramAPI(insta_userid, insta_password)
ig.login()
ig.uploadAlbum(media, caption=sns_caption)

print('Successfully uploaded to Instagram!')
print()

###
# Facebook

print('Uploading to Facebook page..')


fb_token = token_config.get('token', 'facebook')
data = {
    #'caption': 'test upload 한글',
    'access_token': fb_token,
    'published': 'false'
}

data_upload = {
    'message': sns_caption,
    'access_token': fb_token,
}

# upload to facebook without publishing
for p in range(page):
    files = {
        'file': open('%d.jpg' % p, 'rb')
    }
    resp = requests.post(
        'https://graph.facebook.com/v2.11/me/photos',
         data=data, files=files)
    json_resp = json.loads(resp.text)
    if 'error' in json_resp:
        raise Exception(str(json_resp['error']))
    data_upload['attached_media[%d]' % p] = '{"media_fbid":"%s"}' % json_resp['id'] 

# post
resp = requests.post(
    'https://graph.facebook.com/v2.11/me/feed',
     data=data_upload)

json_resp = json.loads(resp.text)
if 'error' in json_resp:
    raise Exception(str(json_resp['error']))

print('Successfully uploaded to Facebook page!')
print()

###
# Naver
print('Uploading images to Dropbox.. (for Naver blog hotlinking)')
dropbox_token = token_config.get('token', 'dropbox')
dbx = dropbox.Dropbox(dropbox_token)

image_links = []
for p in range(page):
    with open("%d.jpg" % p, 'rb') as f:
        data = f.read()
    result = dbx.files_upload(data, '/ticketing/%s/%d.jpg' % (first_date, p), mode = dropbox.files.WriteMode.add, autorename = True)
    upload_path = result.path_display

    result = dbx.sharing_create_shared_link(upload_path, short_url=False)
    url = result.url.replace('www.dropbox.com', 'dl.dropboxusercontent.com')    # for obtaining actual image link
    image_links.append(url)

print('Successfully uploaded to Dropbox!')
print()

print('Uploading a post to Naver blog..')
naver_id = token_config.get('id', 'naver')
naver_token = token_config.get('token', 'naver')


###########
API_URL = 'https://api.blog.naver.com/xmlrpc'
class NaverBlog(object):
    def __init__(self, user_id, api_key):
        self.__server = None
        self.__user_id = user_id
        self.__api_key = api_key
        self.__categories = []
 
        try:
            self.__set_categories()
        except Exception as e:
            raise e
 
    def __client(self):
        if self.__server is None:
            self.__server = xmlrpc.client.ServerProxy(API_URL)
 
        return self.__server
 
    def __set_categories(self):
        categories = self.__client().metaWeblog.getCategories(self.__user_id,
                                                              self.__user_id,
                                                              self.__api_key)
 
        for category in categories:
            self.__categories.append(category['title'])
 
    def new_post(self, title, description, category, publish=True):
        struct = {}
        struct['title'] = title
        struct['description'] = description
        if category in self.__categories:
            struct['categories'] = [category]
 
        try:
            return self.__client().metaWeblog.newPost(self.__user_id,
                                                      self.__user_id,
                                                      self.__api_key,
                                                      struct,
                                                      publish)
        except Exception as e:
            raise e

    def new_post_struct(self, struct, publish=True):
        try:
            return self.__client().metaWeblog.newPost(self.__user_id,
                                                      self.__user_id,
                                                      self.__api_key,
                                                      struct,
                                                      publish)
        except Exception as e:
            raise e

    def get_post(self, postid):
        try:
            return self.__client().metaWeblog.getPost(postid,
                                                      self.__user_id,
                                                      self.__api_key
                                                      )
        except Exception as e:
            raise e

#####
naver = NaverBlog(naver_id, naver_token)

blog_title = str_month_week + " " + config.get('blog','title')

blog_desc = str_month_week + str_date_range + "<br>"
blog_desc += config.get('blog', 'caption')
blog_desc = config.get('blog','pre_caption_html') + blog_desc + config.get('blog','post_caption_html') + "\n\n"

for link in image_links:
    blog_desc += '<br><br><img src="%s">\n' % link

blog_section = config.get('blog','section')


postid = naver.new_post(blog_title, blog_desc, blog_section)
print('Successfully uploaded to Naver blog!')
