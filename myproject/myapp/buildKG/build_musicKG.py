import os
import re
import json
import jieba.posseg as pseg
from py2neo import Graph, Node

# 判断是不是人名
def isname(single_word_string):
    pair_word_list = pseg.lcut(single_word_string)
    for eve_word, cixing in pair_word_list:
        if cixing == "nr":
            return True
        return False    

class MusicGraph:
    def ___init___(self):
        # 路径
        cur_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])
        self.data_path = os.path.join(cur_dir, 'data\\data.json')
        self.g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="52151")
    def test(self):
        print("----->>/////???")


    
    # 读取文件
    def read_nodes(self):
        print(self)
        # 节点 7
        artists = [] # 艺术家     有属性
        musicColleges = [] # 艺术高校   有属性（只爬了一个）
        musicWorks = []  # 音乐作品    无属性
        musicology = [] # 音乐学       有属性
        musicInstruments = [] # 乐器   有属性
        musicTheroies = [] # 乐理      有属性
        musicTypes = [] # 音乐类型      有属性


        # 关系 11
        rels_representativeWork = [] # 艺术家-音乐作品：代表作品
        rels_graduatedCollege = [] # 艺术家-艺术高校：毕业高校
        rels_musicstyle = [] # 艺术家-音乐类型：音乐风格
        rels_groupMember = [] #  艺术家-艺术家：组合成员
        rels_play = [] # 艺术家-乐器：演奏 
        rels_representativeFigure = [] # 乐器-艺术家：代表人物
        rels_appliedScience = [] # 乐器-音乐学：应用学科 
        rels_applicableMusicType = []  # 乐器-音乐类型：适用类型
        rels_classfication = [] # 乐器-乐器：分类
        rels_representativeMusicInstrument = [] # 音乐型-乐器：代表乐器
        rels_subjectSetting = []  # 音乐学-音乐学科：学科设置
        
        # 思路： 先把节点分类出来，然后遍历充实其信息和关系
        count = 0
        with open(self.data_path, encoding='utf-8') as f:
            lis = json.load(f)   # all datas 列表形式
            '''抽出节点'''
            for data in lis:
                count += 1
                print("count:", count)

                key_list = list(data.keys())
                name = data[key_list[0]]

                '''musicColleges 艺术高校'''     
                # 注意 毕业院校不一定是艺术高校，所以我只爬取了代表院校——中国传媒大学的信息
                if '毕业院校' in data:
                    musicColleges.append(data['毕业院校'])
                
                ''' musicology 音乐学'''
                if name.startswith('音') and name.endswith('学'):
                    musicology.append(name);

                ''' artists 艺术家 '''
                if isname(name):
                    artists.append(name)
                # infor = {}  # 每条data 所包含的信息
                if re.findall('[a-zA-Z]+', name):
                    artists.append(name)

                if '国籍' in data:
                    artists.append(name)
                # 筛选人和组合最好的方法是看其是否有代表作品和其国籍
                if '代表作品' not in data:
                    if name in artists:
                        if '国籍' not in data:
                            artists.remove(name)
                
                 
                
                '''musicWorks音乐作品'''
                works = ""
                if '作品' in data:
                    works = data['作品']
                if '代表作品' in data:
                    works = data['代表作品']

                work_list = re.split('、|,', works)
                if '、' not in works and ',' not in works:
                    work_list = re.split(' ', works)
                for item in work_list:
                    item = item.replace('《', '')
                    item = item.replace('》', '')
                    musicWorks.append(item)
            
            musicColleges.append("中国传媒大学")
            musicColleges = set(musicColleges)
            artists = set(artists)
            musicWorks = [i for i in musicWorks if i != '']   # 去除 空字符串



            '''musicTypes 音乐类型'''
            musicTypes = ['古典音乐','民间音乐','流行音乐','摇滚','爵士乐','乡村音乐','民族音乐','华尔兹','新古典主义音乐','浪漫主义音乐','表现主义音乐','现代音乐','R&B','朋克'
            ,'说唱','拉丁','节奏蓝调', '民歌','民谣','蓝调','歌剧','电子音乐', '艺术歌曲','清唱剧','英伦摇滚', '秧歌剧', '音乐剧', '印象主义音乐', '群众歌曲','Pop','hip-hop']
                            
                            
            '''musicInstruments 乐器'''
            musicInstruments = ['吉他','小提琴','钢琴','贝斯','古筝','古琴','口琴','三角铁','琵琶','胡琴','弦乐器','二胡','电吉他',
            '英国管','定音鼓','钢管乐器', '钢片琴','铜管乐器','小镲', '大镲', '竖琴', '管风琴','吊镲', '木琴', '铁琴','锣','鼓','双簧管','尤克里里','键盘乐器','长笛','大军鼓', '小军鼓', '乐器',
            '木管乐器', '打击乐器','班卓琴']



            '''musicTheroies 乐理'''
            musicTheroies = []
            for data in lis:
                key_list = list(data.keys())
                name = data[key_list[0]]

                if name not in musicWorks and name not in musicColleges and name not in musicology and name not in artists and name not in musicTypes and name not in musicInstruments:
                    musicTheroies.append(name)
        
        artists.remove('古琴')    # 特殊：这个被认为了人名   
        artists.remove('小提琴')    # 特殊：这个被认为了人名   

        ''' 建立关系咯 '''   
        for data in lis:
            key_list = list(data.keys())
            name = data[key_list[0]]


            ''' rels_subjectSetting 音乐学-音乐学科 学科设置 ''' 
            if name != '音乐学' and name in musicology:
                rels_subjectSetting.append(['音乐学', name])
        
            
            ''' rels_classfication 乐器-乐器  分类'''
            if name != '乐器' and name in musicInstruments:
                rels_classfication.append(['乐器', name])
            
            ''' rels_representativeWork 艺术家-音乐作品  代表作品'''
            if name in artists:
                works = ""
                style = ""
                groupMember = ""
                play = ""
                if '作品' in data:
                    works = data['作品']
                if '代表作品' in data:
                    works = data['代表作品']

                work_list = re.split('、|,', works)
                if '、' not in works and ',' not in works:
                    work_list = re.split(' ', works)

                for item in work_list:
                    item = item.replace('《', '')
                    item = item.replace('》', '')
                    if item != '':
                        rels_representativeWork.append([name, item])

                ''' rels_graduatedCollege 艺术家-艺术高校  毕业高校'''
                if '毕业院校' in data:
                    rels_graduatedCollege.append([name, data['毕业院校']])

                ''' rels_musicstyle 艺术家-音乐类型  音乐风格'''
                if '音乐类型' in data:
                    style = data['音乐类型']
                if '音乐风格' in data:
                    style = data['音乐风格']
                style_list = re.split('、', style)
                for item in style_list:
                    if item != '':
                        rels_musicstyle.append([name, item])

                '''rels_groupMember 艺术家-艺术家：组合成员'''
                if '组合成员' in data:
                    groupMember = data['组合成员']
                member_list = re.split("、", groupMember)
                for item in member_list:
                    if item != '':
                        rels_groupMember.append([name, item])
                
                '''rels_play  艺术家-乐器 演奏'''
                if '演奏乐器' in data:
                    play = data['演奏乐器']
                play_list = re.split("、", play)
                for item in play_list:
                    if item != '':
                        rels_play.append([name, item])


            '''rels_representativeFigure 乐器-艺术家 代表人物'''  
            if name in musicInstruments:
                figures = ""
                subjects = ""
                types = ""
                works = ""
                instruments = ""
                if '代表人物' in data:
                    figures = data['代表人物']
                figure_list = re.split("、", figures)
                for item in figure_list:
                    if item != '':
                        rels_representativeFigure.append([name, item]) 
            
                '''rels_appliedScience 乐器-音乐学  应用学科'''
                if '应用学科' in data:
                    subjects = data['应用学科']
                subject_list = re.split("、", subjects)
                for item in subject_list:
                    if item != '':
                        rels_appliedScience.append([name, item])

                '''rels_applicableMusicType  乐器-音乐类型  适用类型'''
                if '适用领域' in data:
                    types = data['适用领域']
                type_list = re.split("、", types)
                for item in type_list:
                    if item != '':
                        rels_applicableMusicType.append([name, item])

                '''rels_representativeWork 乐器 - 音乐作品 代表作品'''
                if '代表作品' in data:
                    works = data['代表作品']
                work_list = re.split("、", works)
                for item in work_list:
                    item = item.replace('《', '')
                    item = item.replace('》', '')
                    if item != '':
                        rels_representativeWork.append([name, item])

                '''rels_classfication 乐器 - 子乐器 分类'''
                if '分类' in data:
                    instruments = data['分类']
                instrument_list = re.split("、", instruments)
                for item in instrument_list:
                    if item != '':
                        rels_classfication.append([name, item])


            '''rels_representativeMusicInstrument 音乐类型- 乐器  代表乐器'''
            if name in musicTypes:
                # print(data)
                instruments = ""
                figures = ""
                works = ""
                if '代表乐器' in data:
                    instruments = data['代表乐器']
                instrument_list = re.split("、", instruments)
                for item in instrument_list:
                    if item != '':
                        rels_representativeMusicInstrument.append([name, item])

                '''rels_representativeFigure 音乐类型- 艺术家  代表人物'''
                if '代表人物' in data:
                    figures = data['代表人物']
                figure_list = re.split("、", figures)
                for item in figure_list:
                    if item != '':
                        rels_representativeFigure.append([name, item])

                '''rels_representativeWork 音乐类型- 艺术作品  代表作品'''
                if '代表作品' in data:
                    works = data['代表作品']
                work_list = re.split("、", works)
                for item in work_list:
                    item = item.replace('《', '')
                    item = item.replace('》', '')
                    if item != '':
                        rels_representativeWork.append([name, item])

        return artists, musicInstruments, musicColleges, musicology, musicTypes, musicWorks, musicTheroies,rels_applicableMusicType, rels_appliedScience, rels_classfication, rels_graduatedCollege, rels_groupMember,rels_musicstyle, rels_play, rels_representativeFigure, rels_representativeWork, rels_subjectSetting, rels_representativeMusicInstrument


    # 得到节点属性信息
    def get_infor(self):
        artists, musicInstruments, musicColleges, musicology, musicTypes, musicWorks, musicTheroies,rels_applicableMusicType, rels_appliedScience, rels_classfication, rels_graduatedCollege, rels_groupMember,rels_musicstyle, rels_play, rels_representativeFigure, rels_representativeWork, rels_subjectSetting, rels_representativeMusicInstrument = self.read_nodes()

        
        # 节点属性     建立关系的时候丰富信息
        artists_infor = []  # 艺术家 属性信息
        colleges_infor = []   # 艺术高校信息
        musicology_infor = []  # 音乐学信息
        instrument_infor = []  # 乐器信息
        theroy_infor = []  # 乐理信息
        types_infor = []  # 音乐类型信息
        with open(self.data_path, encoding='utf-8') as f:
            lis = json.load(f)   # all datas 列表形式
            data_infor = {}
            ''' 建立关系咯 '''   
            for data in lis:
                data_infor = data   # 字典类型
                key_list = list(data.keys())
                name = data[key_list[0]]

                # 音乐学 单独被列出来
                if name == '音乐学':
                    musicology_infor.append(data_infor)
                
                # 中国传媒大学
                if name == '中国传媒大学':
                    colleges_infor.append(data_infor)   # colleges_infor
                
                # 乐理信息
                if name in musicTheroies:
                    theroy_infor.append(data_infor)

                # musicology_infor 有关音乐学
                if name != '音乐学' and name in musicology:
                    musicology_infor.append(data_infor) 
                
                ''' 有关艺术家'''
                if name in artists:

                    if '作品' in data:
                        del data_infor['作品']
                    if '代表作品' in data:
                        del data_infor['代表作品']

                    '''毕业高校'''
                    if '毕业院校' in data:
                        del data_infor['毕业院校']

                    '''音乐风格'''
                    if '音乐类型' in data:
                        del data_infor['音乐类型']
                    if '音乐风格' in data:
                        del data_infor['音乐风格']

                    '''组合成员'''
                    if '组合成员' in data:
                        del data_infor['组合成员']
                    
                    '''乐器 演奏'''
                    if '演奏乐器' in data:
                        del data_infor['演奏乐器']

                    artists_infor.append(data_infor)  # artist


                '''有关乐器'''  
                if name in musicInstruments:
            
                    if '代表人物' in data:
                        del data_infor['代表人物']
                
                    '''音乐学  应用学科'''
                    if '应用学科' in data:
                        del data_infor['应用学科']
        
                    '''音乐类型  适用类型'''
                    if '适用领域' in data:
                        del data_infor['适用领域']

                    '''音乐作品 代表作品'''
                    if '代表作品' in data:
                        del data_infor['代表作品']
            
                    '''rels_classfication 乐器 - 子乐器 分类'''
                    if '分类' in data:
                        del data_infor['分类']
                    
                    instrument_infor.append(data_infor)  # instrument

                '''有关音乐类型'''
                if name in musicTypes:
                
                    if '代表乐器' in data:
                        del data_infor['代表乐器']

                    '''艺术家  代表人物'''
                    if '代表人物' in data:
                        del data_infor['代表人物']

                    '''艺术作品  代表作品'''
                    if '代表作品' in data:
                        del data_infor['代表作品']
        
                    types_infor.append(data_infor)

        print("--->", artists_infor, colleges_infor, musicology_infor, instrument_infor, theroy_infor, types_infor)
        return artists_infor, colleges_infor, musicology_infor, instrument_infor, theroy_infor, types_infor

    # 建立节点
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name = node_name)
            print("--->", node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return 

    # 建立艺术家节点
    def create_artist_node(self, artists_infor):
        count = 0
        for infor in artists_infor:
            temp = infor
            print(infor)
            node = Node("艺术家", name = infor['姓名'])
            del temp['姓名']

            node.update(temp)
            self.g.create(node)
            count += 1
            print(count)
        return 

    # 建立有信息的艺术高校节点
    def create_colleges_node(self, colleges_infor):
        count = 0
        for infor in colleges_infor:
            temp = infor
            print(infor)
            node = Node("艺术高校", name = infor['姓名'])
            del temp['姓名']

            node.update(temp)
            self.g.create(node)
            count += 1
            print(count)
        return 

     # 建立音乐学节点
    def create_musicology_node(self, musicology_infor):
        count = 0
        for infor in musicology_infor:
            temp = infor
            print(infor)
            node = Node("音乐学", name = infor['姓名'])
            del temp['姓名']

            node.update(temp)
            self.g.create(node)
            count += 1
            print(count)
        return 

    # 建立乐器信息节点
    def create_instrument_node(self, instrument_infor):
        count = 0
        for infor in instrument_infor:
            print("infor: ", infor)
            temp = infor
            
            node = Node("乐器", name = infor['姓名'])
            del temp['姓名']
            print("temp: ", temp)
            node.update(temp)
            self.g.create(node)
            count += 1
            print(count)
        return

    # 建立乐理信息节点
    def create_theroy_node(self, theroy_infor):
        count = 0
        for infor in theroy_infor:
            temp = infor
            print(infor)
            node = Node("乐理", name = infor['姓名'])
            del temp['姓名']

            node.update(temp)
            self.g.create(node)
            count += 1
            print(count)
        return   
    # 建立音乐类型信息节点
    def create_type_node(self, types_infor):
        count = 0
        for infor in types_infor:
            temp = infor
            print(infor)
            node = Node("音乐类型", name = infor['姓名'])
            del temp['姓名']

            node.update(temp)
            self.g.create(node)
            count += 1
            print(count)
        return       
    # 创建知识图谱实体节点类型
    def create_graphnodes(self):
        artists, musicInstruments, musicColleges, musicology, musicTypes, musicWorks, musicTheroies,rels_applicableMusicType, rels_appliedScience, rels_classfication, rels_graduatedCollege, rels_groupMember,rels_musicstyle, rels_play, rels_representativeFigure, rels_representativeWork, rels_subjectSetting, rels_representativeMusicInstrument = self.read_nodes()
        artists_infor, colleges_infor, musicology_infor, instrument_infor, theroy_infor, types_infor = self.get_infor()
        
        print(instrument_infor)
       
        self.create_node('音乐作品', musicWorks)
        self.create_node('艺术高校', musicColleges)
        self.create_instrument_node(instrument_infor)
        self.create_artist_node(artists_infor)
        self.create_colleges_node(colleges_infor)
        self.create_type_node(types_infor)
        self.create_musicology_node(musicology_infor)
        self.create_theroy_node(theroy_infor)
        
        return 
    
    # 创建实体关系边
    def create_graphrels(self):
        artists, musicInstruments, musicColleges, musicology, musicTypes, musicWorks, musicTheroies,rels_applicableMusicType, rels_appliedScience, rels_classfication, rels_graduatedCollege, rels_groupMember,rels_musicstyle, rels_play, rels_representativeFigure, rels_representativeWork, rels_subjectSetting, rels_representativeMusicInstrument = self.read_nodes()
        artists_infor, colleges_infor, musicology_infor, instrument_infor, theroy_infor, types_infor = self.get_infor()
        self.create_relationship('乐器', '音乐类型', rels_applicableMusicType, 'applicableMusicType', '适用类型')
        self.create_relationship('乐器', '音乐学', rels_appliedScience, 'appliedScience', '应用学科')
        self.create_relationship('乐器', '乐器', rels_classfication, 'classfication', '分类')
        self.create_relationship('艺术家', '艺术高校', rels_graduatedCollege, 'graduatedCollege', '毕业高校')
        self.create_relationship('艺术家', '艺术家', rels_groupMember, 'groupMember', '组合成员')
        self.create_relationship('艺术家', '音乐类型', rels_musicstyle, 'musicstyle', '音乐风格')
        self.create_relationship('艺术家', '乐器', rels_play, 'play', '演奏')
        self.create_relationship('乐器', '艺术家', rels_representativeFigure, 'representativeFigure', '代表人物')
        self.create_relationship('音乐类型', '艺术家', rels_representativeFigure, 'representativeFigure', '代表人物')
        self.create_relationship('乐器', '音乐作品', rels_representativeWork, 'representativeWork', '代表作品')
        self.create_relationship('音乐类型', '音乐作品', rels_representativeWork, 'representativeWork', '代表作品')
        self.create_relationship('艺术家', '音乐作品', rels_representativeWork, 'representativeWork', '代表作品')
        self.create_relationship('音乐学', '音乐学', rels_subjectSetting, 'subjectSetting', '学科设置')
        self.create_relationship('音乐类型', '音乐作品', rels_representativeMusicInstrument, 'representativeMusicInstrumen', '代表乐器')


    # 创建实体关联边
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return


    '''导出数据'''
    def export_data(self):
        artists, musicInstruments, musicColleges, musicology, musicTypes, musicWorks, musicTheroies,rels_applicableMusicType, rels_appliedScience, rels_classfication, rels_graduatedCollege, rels_groupMember,rels_musicstyle, rels_play, rels_representativeFigure, rels_representativeWork, rels_subjectSetting, rels_representativeMusicInstrument = self.read_nodes()

        f_artist = open('artists.txt', 'w+', encoding="utf-8")
        f_musicInstrument = open('musicInstruments.txt', 'w+', encoding="utf-8")
        f_musicCollege = open('musicColleges.txt', 'w+', encoding="utf-8")
        f_musicology = open('musicology.txt', 'w+', encoding="utf-8")
        f_musicType = open('musicTypes.txt', 'w+', encoding="utf-8")
        f_musicWork = open('musicWorks.txt', 'w+', encoding="utf-8")
        f_musicTheroy = open('musicTheroies.txt', 'w+', encoding="utf-8")

        f_artist.write('\n'.join(list(artists)))
        f_musicInstrument.write('\n'.join(list(musicInstruments)))
        f_musicCollege.write('\n'.join(list(musicColleges)))
        f_musicology.write('\n'.join(list(musicology)))
        f_musicType.write('\n'.join(list(musicTypes)))
        f_musicWork.write('\n'.join(list(musicWorks)))
        f_musicTheroy.write('\n'.join(list(musicTheroies)))

        f_artist.close()
        f_musicInstrument.close()
        f_musicCollege.close()
        f_musicology.close()
        f_musicType.close()
        f_musicWork.close()
        f_musicTheroy.close()

        return 

if __name__ == '__main__':
    
    # print(cur_dir)
    


    headler = MusicGraph()
    headler.___init___()
    headler.test()
    # headler.read_nodes(data_path)
    headler.export_data()
    # headler.get_infor(data_path)
    #headler.create_graphnodes()
    
    #headler.create_graphrels()
