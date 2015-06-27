from collections import defaultdict
import os
import pprint
import re
from models import Tag_Similarity

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django import db

conn = db.connections['default']
cursor = conn.cursor()

def chunks(l, size):
    """ Yield successve n-sized chunks from l"""
    for i in xrange(0, len(l), size):
        yield l[i:i+size]

def calculate_app_weights():
    pass


def _do_calculate_tag(base_tag_apps, tag_apps):
    same_app_ids = list(set(base_tag_apps.keys()) & set(tag_apps.keys()))
    same_app_count = len(same_app_ids)
    base_tag_apps_count = len(base_tag_apps)
    tag_apps_count = len(tag_apps)

    base_tag_rate = float(same_app_count) / base_tag_apps_count
    tag_rate = float(same_app_count) / tag_apps_count
    similarity = (base_tag_rate + tag_rate) / 2
    return round(similarity, 5)


def get_similar_tags_advance(tag):
    cursor.execute("SELECT app_id, times FROM cm_tag_15w WHERE tag = '%s' ORDER BY times DESC LIMIT 50;" % tag)
    top_app_times = {r[0] : r[1] for r in cursor}
    top_app_ids = top_app_times.keys()

    similar_matrix = defaultdict(list)
    cursor.execute('SELECT app_id, tag, times FROM cm_tag_15w WHERE app_id IN (%s) AND times > 1' % ','.join(map(str, top_app_ids)))
    for r in cursor:
        app_id, tag, times = r
        similarity = top_app_times[app_id] + times * 0.75
        similar_matrix[tag].append((app_id, similarity))

    final_similar_matrix = []
    for tag, similarities in similar_matrix.iteritems():
        final_similar_matrix.append([tag, sum([(1/i) * s[1] for i, s in enumerate(similarities, start=1)])])

    return sorted(final_similar_matrix, key=lambda e: e[1], reverse=True)


def calculate_tag_similarity():
    cursor.execute('Truncate table tag_similarity_15w;')
    db.transaction.commit_unless_managed(using='default')
    # Get all tags
    cursor.execute('SELECT DISTINCT(tag) FROM cm_tag_15w;')
    tags = [re.sub(r"[^a-zA-Z0-9]+","",r[0]) for r in cursor]

    all_tag_data = defaultdict(dict)
    for tag_batch in chunks(tags, 1000):
        cursor.execute(
            cursor.mogrify(
                'SELECT tag, app_id, times FROM cm_tag_15w WHERE tag IN %s;', (tuple(tag_batch), )
            )
        )
        for r in cursor:
            all_tag_data[r[0]][r[1]] = r[2]
    all_tags = all_tag_data.keys()
    all_tags_length = len(all_tags)

    # Calculate similarity for each two tags
    similarity_data = []
    for i, base_tag in enumerate(all_tags):
        similarity_data = []
        for j, tag in enumerate(all_tags[i+1:]):
            base_tag_data = all_tag_data[base_tag]
            tag_data = all_tag_data[tag]
            similarity = _do_calculate_tag(base_tag_data, tag_data)
            if similarity > 0.0:
                similarity_data.append([base_tag, tag, similarity])
        print '**%s/%s, %s, similarity_data length is %s' % (i, all_tags_length, base_tag, len(similarity_data))
        if i % 1000 == 0:
            insert_sql = 'INSERT INTO tag_similarity_15w (base_tag, tag, similarity) VALUES (%s, %s, %s);'
            for base, tag, similarity in similarity_data:
                cursor.execute(insert_sql, (base, tag, similarity))
            db.transaction.commit_unless_managed(using='default')
            del similarity_data

    if similarity_data:
        insert_sql = 'INSERT INTO tag_similarity_15w (base_tag, tag, similarity) VALUES (%s, %s, %s);'
        for base, tag, similarity in similarity_data:
            cursor.execute(insert_sql, (base, tag, similarity))
        db.transaction.commit_unless_managed(using='default')


def get_similar_tags_django(tag, top=30):
    tags = Tag_Similarity.objects.filter(tag=tag).order_by('-similarity')[:top]
    tags_data = [(tag.base_tag, tag.similarity) for tag in tags]
    reverse_tags = Tag_Similarity.objects.filter(base_tag=tag).order_by('-similarity')[:top]
    reverse_tags_data = [(tag.tag, tag.similarity) for tag in reverse_tags]
    similar_list = sorted(tag_similar_list + base_tag_similar_list, key=lambda e: e[1], reverse=True)
    return similar_list[:top]


def get_similar_tags(tag, top=30):
    cursor = conn.cursor()
    sql = "SELECT base_tag, similarity FROM cm_tag_similarity WHERE tag = '%s' ORDER BY similarity DESC LIMIT %s;" % (tag, top)
    cursor.execute(sql)
    tag_similar_list = [(r[0], r[1]) for r in cursor]
    cursor.execute("SELECT tag, similarity FROM cm_tag_similarity WHERE base_tag = '%s' ORDER BY similarity DESC LIMIT %s;" % (tag, top))
    base_tag_similar_list = [(r[0], r[1]) for r in cursor]
    similar_list = sorted(tag_similar_list + base_tag_similar_list, key=lambda e: e[1], reverse=True)
    cursor.close()
    return similar_list[:top]


def get_apps_by_tag(tag, top=60):
    cursor = conn.cursor()
    cursor.execute("SELECT app_id FROM cm_tag WHERE tag = '%s' ORDER BY times DESC LIMIT %s" % (tag[0], top))
    app_ids = [r[0] for r in cursor]

    if not app_ids:
        return []
    app_id_str = ','.join(map(str, app_ids))
    cursor.execute('SELECT id, name, icon FROM cm_app WHERE id IN (%s)' % (app_id_str, ))
    apps = []
    for r in cursor:
        apps.append({
            'src': r[2],
            'title': r[1],
            'link': 'https://www.appannie.com/apps/ios/app/%s/' % r[0]
        })
    cursor.close()
    return apps

def tidy_tags():

    stop_words = "a's,able,about,above,according,accordingly,across,actually,after,afterwards,again,against,ain't,all,allow,allows,almost,alone,along,already,also,although,always,am,among,amongst,an,and,another,any,anybody,anyhow,anyone,anything,anyway,anyways,anywhere,apart,appear,appreciate,appropriate,are,aren't,around,as,aside,ask,asking,associated,at,available,away,awfully,be,became,because,become,becomes,becoming,been,before,beforehand,behind,being,believe,below,beside,besides,best,better,between,beyond,both,brief,but,by,c'mon,c's,came,can,can't,cannot,cant,cause,causes,certain,certainly,changes,clearly,co,com,come,comes,concerning,consequently,consider,considering,contain,containing,contains,corresponding,could,couldn't,course,currently,definitely,described,despite,did,didn't,different,do,does,doesn't,doing,don't,done,down,downwards,during,each,edu,eg,eight,either,else,elsewhere,enough,entirely,especially,et,etc,even,ever,every,everybody,everyone,everything,everywhere,ex,exactly,example,except,far,few,fifth,first,five,followed,following,follows,for,former,formerly,forth,four,from,further,furthermore,get,gets,getting,given,gives,go,goes,going,gone,got,gotten,greetings,had,hadn't,happens,hardly,has,hasn't,have,haven't,having,he,he's,hello,help,hence,her,here,here's,hereafter,hereby,herein,hereupon,hers,herself,hi,him,himself,his,hither,hopefully,how,howbeit,however,i'd,i'll,i'm,i've,ie,if,ignored,immediate,in,inasmuch,inc,indeed,indicate,indicated,indicates,inner,insofar,instead,into,inward,is,isn't,it,it'd,it'll,it's,its,itself,just,keep,keeps,kept,know,known,knows,last,lately,later,latter,latterly,least,less,lest,let,let's,like,liked,likely,little,look,looking,looks,ltd,mainly,many,may,maybe,me,mean,meanwhile,merely,might,more,moreover,most,mostly,much,must,my,myself,name,namely,nd,near,nearly,necessary,need,needs,neither,never,nevertheless,new,next,nine,no,nobody,non,none,noone,nor,normally,not,nothing,novel,now,nowhere,obviously,of,off,often,oh,ok,okay,old,on,once,one,ones,only,onto,or,other,others,otherwise,ought,our,ours,ourselves,out,outside,over,overall,own,particular,particularly,per,perhaps,placed,please,plus,possible,presumably,probably,provides,que,quite,qv,rather,rd,re,really,reasonably,regarding,regardless,regards,relatively,respectively,right,said,same,saw,say,saying,says,second,secondly,see,seeing,seem,seemed,seeming,seems,seen,self,selves,sensible,sent,serious,seriously,seven,several,shall,she,should,shouldn't,since,six,so,some,somebody,somehow,someone,something,sometime,sometimes,somewhat,somewhere,soon,sorry,specified,specify,specifying,still,sub,such,sup,sure,t's,take,taken,tell,tends,th,than,thank,thanks,thanx,that,that's,thats,the,their,theirs,them,themselves,then,thence,there,there's,thereafter,thereby,therefore,therein,theres,thereupon,these,they,they'd,they'll,they're,they've,think,third,this,thorough,thoroughly,those,though,three,through,throughout,thru,thus,to,together,too,took,toward,towards,tried,tries,truly,try,trying,twice,two,un,under,unfortunately,unless,unlikely,until,unto,up,upon,us,use,used,useful,uses,using,usually,value,various,very,via,viz,vs,want,wants,was,wasn't,way,we,we'd,we'll,we're,we've,welcome,well,went,were,weren't,what,what's,whatever,when,whence,whenever,where,where's,whereafter,whereas,whereby,wherein,whereupon,wherever,whether,which,while,whither,who,who's,whoever,whole,whom,whose,why,will,willing,wish,with,within,without,won't,wonder,would,wouldn't,yes,yet,you,you'd,you'll,you're,you've,your,yours,yourself,yourselves,zero"
    stop_words +="app,lot,please,great,apps,awesome,day,thing,use,get,play,something,everything,playing,thanks,issue,anything,nothing,thank,good,data,excellent,updates,access,user,dyas,list,help,others,fine"

    stop_words_list = stop_words.split(',')
    print '**%s' % len(stop_words_list)
    cursor.execute(
        cursor.mogrify('DELETE FROM cm_tag_15w WHERE tag IN %s', (tuple(stop_words_list), ))
    )

def normalize_tags():
    cursor.execute('SELECT app_id, tag, times FROM tag_app_rel;')
    all_tag_data = defaultdict(dict)
    for r in cursor:
        all_tag_data[r[0]][r[1]] = r[2]
    from nltk.stem.snowball import EnglishStemmer
    stemmer = EnglishStemmer()
    for app_id, tag_to_times in all_tag_data.iteritems():
        normalized_app_tag_dict = defaultdict(int)
        for tag, times in tag_to_times.iteritems():
            normalized_app_tag_dict[stemmer.stem(tag)] += times
        for tag, times in normalized_app_tag_dict.iteritems():
            cursor.execute('INSERT INTO tag_app_relation (app_id, tag, times) VALUES (%s, %s, %s)', (app_id, tag, times))


if __name__ == "__main__":
    # calculate_tag_similarity()
    # tidy_tags()
    tags = get_similar_tags_advance('gambling')
    print 'dice' in dict(tags)
    print dict(tags)['dice']
    pprint.pprint(tags[:80])