import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import unidecode

url = "https://www.ufc.com/rankings"
req = requests.get(url)
soup = BeautifulSoup(req.content,"html.parser")

champ_list = []
for i in soup.find_all("caption"):
    if ("weight" in i.text) and (i.next_sibling.next_sibling) and (len(i.next_sibling.next_sibling.contents) > 1):
        champ_list.append(i.a.text)
    else:
        pass

weight_classes = []
for i in soup.find_all("caption"):
    if ("weight" in i.text) and (len(i.next_sibling.next_sibling.contents) > 1):
        weight_classes.append(i.h4.text)

top15list = []
q2 = []
for i in soup.find_all("caption"):
    # if [i for in list4] in i.text:
    if ("weight" in i.text) and (len(i.next_sibling.next_sibling.contents) > 1):
        for y in (i.next_sibling.next_sibling.find_all("div",{"class":"views-row"})):
            q2.append(y.text)
        top15list.append(q2)
        q2 = []


no_wins = []
l_new_2 = []

for i in range(len(champ_list)):
    name1 = champ_list[i]
    wiki = "https://en.wikipedia.org/wiki/"
    url1 = (wiki + name1)
    page = requests.get(url1).text

    soup = BeautifulSoup(page, "html.parser")
    t1 = soup.find_all("table",attrs={"class":"wikitable","style":"font-size: 85%;"})

    df = pd.read_html(str(t1))[0]

    for y in range(len(df["Opponent"])):
        if (unidecode.unidecode(df["Opponent"][y]) in top15list[i]) and (df["Res."][y] == "Win"):
            (l_new_2.append(df["Opponent"][y]))
        else:
            pass
    l_new_2 = list(dict.fromkeys(l_new_2))
    no_wins.append(str(len(l_new_2)))
    l_new_2 = []


df = pd.DataFrame({"Name":champ_list,"Weight":weight_classes,"No. of Wins":no_wins,"Top 15 Opponents":top15list})

data = df[["Name","No. of Wins"]]
data = data.astype({"No. of Wins": int})

data_sorted = data.sort_values(by='No. of Wins', ascending=True)

fig, ax = plt.subplots(figsize=(12,5))
hbars = ax.barh(width=data_sorted["No. of Wins"],y=data_sorted["Name"],color="lightseagreen")

font = {'family': 'arial',
        'color':  'gray',
        'weight': 'bold',
        'size': 20,
        }
ax.set_title("Wins Against Current Top 15 in their Division",fontdict=font,loc="left")
ax.bar_label(hbars,label_type="edge",padding=10)
ax.set_yticks(ticks=data_sorted["Name"])

font2 = {'family': 'calibri',
        'color':  'dimgray',
        'weight': 'normal',
        'size': 11,
        }
ax.set_yticklabels(labels=data_sorted["Name"],fontdict=font2)
ax.get_xaxis().set_visible(False)
ax.tick_params(axis=u'both', which=u'both',length=0)

ax.set_facecolor("whitesmoke")
fig.patch.set_facecolor('whitesmoke')
plt.box(False)
plt.show()