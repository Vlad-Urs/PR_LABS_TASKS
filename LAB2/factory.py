from player import Player
from datetime import datetime
from player import Player
import re

import player_pb2

class PlayerFactory:
    def to_json(self, players):
        dict_list = []
        for player in players:
           new_dict = {
               "nickname" : player.nickname,
               "email" : player.email,
               "date_of_birth" : player.date_of_birth.strftime("%Y-%m-%d"),
               "xp" : player.xp,
               "class" : player.cls

           }

           dict_list.append(new_dict)

        return dict_list

    def from_json(self, list_of_dict):
        player_list = []

        for dict in list_of_dict:
            new_player = Player(dict["nickname"], dict["email"], dict["date_of_birth"], dict["xp"], dict["class"])
            player_list.append(new_player)

        return player_list

    def from_xml(self, xml_string):
        players = []
        number_of_players = xml_string.count("<player>")
        params = ['nickname', 'email', 'date_of_birth', 'xp', 'class']

        for i in range(number_of_players):
            # get the nickname
            start_nickname = xml_string.find("<nickname>") + 10
            end_nickname = xml_string.find("</nickname>")
            name = xml_string[start_nickname:end_nickname]
            xml_string = xml_string.replace("<nickname>","",1)
            xml_string = xml_string.replace("</nickname>","",1)

            # get the email
            start_email = xml_string.find("<email>") + 7
            end_email = xml_string.find("</email>")
            e_mail = xml_string[start_email:end_email]
            xml_string = xml_string.replace("<email>","",1)
            xml_string = xml_string.replace("</email>","",1)

            # get the date of birth
            start_date = xml_string.find("<date_of_birth>") + 15
            end_date = xml_string.find("</date_of_birth>")
            date_ob = xml_string[start_date:end_date]
            xml_string = xml_string.replace("<date_of_birth>","",1)
            xml_string = xml_string.replace("</date_of_birth>","",1)

            # get the xp
            start_xp = xml_string.find("<xp>") + 4
            end_xp = xml_string.find("</xp>")
            x_p = int(xml_string[start_xp:end_xp])
            xml_string = xml_string.replace("<xp>","",1)
            xml_string = xml_string.replace("</xp>","",1)

            # get the class
            start_class = xml_string.find("<class>") + 7
            end_class = xml_string.find("</class>")
            clss = xml_string[start_class:end_class]
            xml_string = xml_string.replace("<class>","",1)
            xml_string = xml_string.replace("</class>","",1)

            players.append(Player(name, e_mail, date_ob, x_p, clss))
        
        return players
    def to_xml(self, list_of_players):
        xml_file = '''<?xml version="1.0"?>
            <data>'''
        for player in list_of_players:
            xml_file += "        <player>"
            xml_file += f"            <nickname>{player.nickname}</nickname>"
            xml_file += f"            <email>{player.email}</email>"
            xml_file += f'''            <date_of_birth>{player.date_of_birth.strftime('%Y-%m-%d')}</date_of_birth>'''
            xml_file += f"            <xp>{str(player.xp)}</xp>"
            xml_file += f"            <class>{player.cls}</class>"
            xml_file += "        </player>"

        xml_file += "    </data>"

        return xml_file

    def from_protobuf(self, binary):
        plrs = player_pb2.PlayersList()
        plrs.ParseFromString(binary)
        player_list = []
        class_dict = {
            0 : "Berserk",
            1 : "Tank",
            3 : "Paladin",
            4 : "Mage"
        }


        for p in plrs.player:
            player_list.append(Player(p.nickname, p.email, p.date_of_birth, p.xp, class_dict[p.cls]))
            
        return player_list

    def to_protobuf(self, list_of_players):
        plrs = player_pb2.PlayersList()

        for plr in list_of_players:
            player = plrs.Player()
            player.nickname = plr.nickname 
            player.email = plr.email 
            player.date_of_birth = plr.date_of_birth.strftime("%Y-%m-%d")
            player.xp = plr.xp 
            player.cls = plr.cls
            plrs.player.append(player)

        return plrs.SerializeToString()

