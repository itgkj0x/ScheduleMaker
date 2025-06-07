import calendar
import math
from datetime  import datetime
from icalendar import Calendar, Event

# 今の時刻を取得して定義

now = datetime.now()
y = now.year
m = now.month
print(y,"で",m)

### 質問タイム

## 週いくつか聞く

wcount = int(input("週いくつで働いてますか"))

## 何曜日か聞いてworkdのリストに入れる

def mkwkd():
    workd = []
    for x in range(1,wcount+1):
        ans = int(input(f"週の{x}日目は何曜日ですか"))
        workd.append(ans)
    print(workd)
    return workd

workd = mkwkd()

## 曜日の条件を生成する
def mkcdn(workd):
    cdn = ""
    for day in workd:
        dcdn = 'd[3] == ' + str(day)
        print(dcdn)
        if day == workd[-1]:
            print(day,'ラスト')
            cdn += dcdn
            continue
        else:
            cdn +=  dcdn + " or "
    return cdn

cdn = mkcdn(workd)


## 今の月から何か月分取得するか聞く
def mkmrange(m):
    hlm = int(input("何か月分取得しますか?"))
    if hlm + m > 12:
        hlmlist = list(range(m, 13))
        hlmlist2 = list(range(1,hlm+m-11))
    else:
        hlmlist = list(range(m, m + hlm))
    return hlm,hlmlist

hlmres = mkmrange(m)

### ターゲットを生成する

## 1.空のリストを作りcを定義する



## 2.月の範囲分の曜日をpickupしてリストにまとめる(cdnで作った条件に沿って)

def mkdtlist(y,cdn,hlmres):
    datelist = []
    c = calendar.Calendar()
    for x in hlmres[1]:
        for d in c.itermonthdays4(y, x):
            if eval(cdn) and (m <= d[1] <= m + hlmres[0] - 1 ):
                datelist.append(d)
    return datelist

    # cdnで条件の曜日を指定
    # dはリスト(年,月,日,曜日)
    # -1するのは今月をカウントすることで一月多くなるのを防ぐため

datelist = mkdtlist(y,cdn,hlmres)

### icalの作成
def mkical(datelist):
    cal = Calendar()
    cal.add('prodid', '-//Test//test-product//ja//')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'REQUEST')
    for x in datelist:
        event = Event()
        event.add('summary', u'バイト')
        event.add('dtstart', datetime(x[0],x[1],x[2],6))
        event.add('dtend', datetime(x[0],x[1],x[2],7))
        event.add('description', u'バイト')
        cal.add_component(event)
    icaldt = cal.to_ical()
    return icaldt
    # 6時から7時の前で指定された日時でのEventを作成させる

result = mkical(datelist)
f = open('bite.ics', 'wb')
f.write(result)
f.close()
#  出た結果を icalファイルに書き込む
