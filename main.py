import calendar
from datetime  import datetime
from icalendar import Calendar, Event # type: ignore

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

## 開始時間を聞く
def mksetime():
    stime = int(input("何時からですか?"))
    etime = int(input("何時までですか?"))
    return stime,etime

setime = mksetime()
wtime = setime[1]-setime[0]


## 時給を聞く

def mktmoney():
    mktm = int(input("時給はいくらですか"))
    return mktm

mktm = mktmoney()

### ターゲットを生成する

## 1.空のリストを作りcを定義する
## 2.月の範囲分の曜日をpickupしてリストにまとめる(cdnで作った条件に沿って)

def mkdtlist(y,workd,hlmres):
    datelist = []
    c = calendar.Calendar()
    for x in hlmres[1]:
        for d in c.itermonthdays4(y, x):
            if (d[3] in workd) and (m <= d[1] <= m + hlmres[0] - 1 ):
                datelist.append(d)
    return datelist

    # cdnで条件の曜日を指定
    # dはリスト(年,月,日,曜日)
    # -1するのは今月をカウントすることで一月多くなるのを防ぐため

datelist = mkdtlist(y,workd,hlmres)

### 給料のカウント

def countm(mktm,datelist,wtime):
    money = mktm*len(datelist)*wtime
    return money

money = countm(mktm,datelist,wtime)
print(money)

### icalの作成
def mkical(datelist,stime,etime):
    cal = Calendar()
    cal.add('prodid', '-//Test//test-product//ja//')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'REQUEST')
    for x in datelist:
        event = Event()
        event.add('summary', u'バイト')
        event.add('dtstart', datetime(x[0],x[1],x[2],stime))
        event.add('dtend', datetime(x[0],x[1],x[2],etime))
        event.add('description', u'バイト')
        cal.add_component(event)
    icaldt = cal.to_ical()
    return icaldt
    # 6時から7時の前で指定された日時でのEventを作成させる

result = mkical(datelist,setime[0],setime[1])
f = open('result/bite.ics', 'wb')
f.write(result)
f.close()

#  出た結果を icalファイルに書き込む
