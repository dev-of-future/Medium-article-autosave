import requests
import re, os

google_cache = "http://webcache.googleusercontent.com/search?q=cache:"


def clean_string(text):
    # This pattern matches any character that is not a letter or whitespace
    pattern = r'[^a-zA-Z\s]'
    return re.sub(pattern, '', text)


def get_title(text):
    # article_title = re.sub('<title .*? /title>', '', response.text)
    article_title = text.split("</title>")[0].split("<title")[1].split(">")[1]
    title = clean_string(article_title)
    title = " ".join([i for i in title.split(" ") if i != ''])

    return title


def get_content(siteUrl):
    new_url = google_cache + siteUrl
    try:
        original_ret = requests.get(new_url)
        try:
            print(original_ret.text.split("<!doctype html"))
            ret = original_ret.text.split("<!doctype html")[2]
            return "<!doctype html" + ret
        except:
            return "FError"
    except requests.exceptions.RequestException as e:
        return "NError"


def remove_script(content):
    cleaned_content = content.split("<script>window.main();</script>")
    return "".join(cleaned_content)


def main():
    with open("urls.txt", 'r') as f:
        original_urls = [i.strip() for i in f.read().split("\n")]
        urls = list(filter(lambda x: x != '', original_urls))

    if len(urls) != 0:
        try:
            os.mkdir("sites")
        except:
            pass

    for url in urls:
        html_content = get_content(url)
        if html_content == "NError":
            print("Failed get content, Network Error!!!!!!!")
        elif html_content == "FError":
            print("Failed get content, File Error!!!!!!!")
        else:
            html_title = "sites/" + get_title(html_content) + ".html"
            html_content = remove_script(html_content)
            try:
                with open(html_title, 'w') as f:
                    f.write(html_content)
                    print("Successfully saved " + html_title)
            except:
                print("Warning : Failed to save " + html_title)


main()
# print(get_content(
#     "https://medium.com/@impure/async-await-is-the-worst-thing-to-happen-to-programming-9b8f5150ba74?source=email-a56cf5023dbd-1721355161279-digest.welcome--9b8f5150ba74----4-109------------------f418048f_7673_4f18_bad1_6dabb0059079-1"))
