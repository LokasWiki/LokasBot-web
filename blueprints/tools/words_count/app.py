import re

import pywikibot
import wikitextparser as wtp
from flask import Blueprint, render_template, request

words_count_page = Blueprint('words_count_page', __name__, template_folder='templates')

site = pywikibot.Site("ar", "wikipedia")


@words_count_page.route("/", methods=('GET', 'POST'))
def words_count_tool():
    messages = []
    if request.method == 'POST':
        title = request.form['title']
        if len(title.strip()) == 0:
            messages.append({'content': "يجب ادخال اسم المقال"})
        else:
            page = pywikibot.Page(site, title)
            if not page.exists():
                messages.append({'content': "المقال غير موجودة"})
            else:
                if not page.namespace() == 0:
                    messages.append({'content': "يجب ان تكون المقال ضمن نطاق المقالات"})
                else:
                    status = True

                    tem_text = page.text

                    parsed = wtp.parse(tem_text)

                    # remove cat links
                    for link in parsed.wikilinks:
                        if ":" in link.title:
                            tem_text = tem_text.replace(str(link), "")
                    parsed = wtp.parse(tem_text)
                    # remove tables
                    # remove template
                    # remove html tag include ref tags
                    # remove all comments
                    # remove all external links
                    tem_text = parsed.plain_text(
                        replace_wikilinks=False,
                        replace_bolds_and_italics=False
                    )
                    parsed = wtp.parse(tem_text)
                    # replace all wikilinks to be like  [from|some text ] to from
                    for wikilink in parsed.wikilinks:
                        tem_text = tem_text.replace(str(wikilink), str(wikilink.title))

                    # remove tables like this "{| |}"
                    tem_text = re.sub(r"{|\|[.|\w|\W]*?\|}", "", tem_text)

                    # remove numbers in string"
                    tem_text = re.sub(r"\d+", "", tem_text)

                    # get counts of words
                    result = len(re.findall(r'\w+', tem_text))

                    if result >= 500:
                        # start remove template
                        status = False

                    return render_template(f"words_count_show.html", new_text=tem_text, status=status, result=result)

    return render_template(f"words_count_form.html", messages=messages)
