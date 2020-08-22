#               Импорт не служебных модулей
import configparser as cp
import logging
#
log=logging.getLogger("main")
extra={"moduleName":"Config"}
#

class ConfigParser():
    def __init__(self):
        self.config=cp.ConfigParser()
        self.path="config.ini"
    def parser(self):
        self.config.read(self.path,encoding='utf-8')
        #   Main
        self.main_token                         =       self.config.get("Main","token")
        self.main_commandPrefix                 =       self.config.get("Main","command_prefix")
        self.main_broudcastChannel              =   int(self.config.get("Main","broudcast_channel"))
        self.antispam_spamCooldown              =   int(self.config.get("AntiSpam","cooldown"))
        self.antispam_spamBypass                =       self.config.get("AntiSpam","bypass").split(",")
        self.antispam_keywords                  =       self.config.get("AntiSpam","keywords").split(",")
        self.serverstatus_statusInVoice         =   int(self.config.get("ServerStatus","in_voice"))
        self.serverstatus_statusInServer        =   int(self.config.get("ServerStatus","in_server"))
        self.serverstatus_statusUpdate          =   int(self.config.get("ServerStatus","time_update"))
        self.giveroles_giveRolesDict            =       self.config.get("GiveRoles","roles")
        self.giveroles_messageID                =   int(self.config.get("GiveRoles","message_id"))
        self.admcheck_admRoles                  =       self.config.get("AdmCheck","adm_roles")
        self.admcheck_admMembers                =       self.config.get("AdmCheck","adm_members")
        self.duels_rejectionAliases             =   set(self.config.get("Duels","rejection_aliases").split(","))
        self.duels_consentAliases               =   set(self.config.get("Duels","consent_aliases").split(","))
        self.duels_topAliases                   =   set(self.config.get("Duels","top_aliases").split(","))
        self.duels_personalInfoAliases          =   set(self.config.get("Duels","personal_info_aliases").split(","))
        self.duels_shotAliases                  =   set(self.config.get("Duels","shot_aliases").split(","))
        self.duels_timeConsent                  =   int(self.config.get("Duels","time_consent"))
        self.duels_timeShot                     =   int(self.config.get("Duels","time_shot"))
        self.duels_shotChance                   =   int(self.config.get("Duels","shot_chance"))
        self.duels_draw                         =   int(self.config.get("Duels","draw"))
        self.duels_channel                      =   int(self.config.get("Duels","channel"))
        self.duels_topLines                     =   int(self.config.get("Duels","top_lines"))
        self.duels_topPositions                 =       self.config.get("Duels","top_positions")
        self.duels_moneyWin                     = float(self.config.get("Duels","money_win"))
        self.duels_moneyLose                    = float(self.config.get("Duels","money_lose"))
        self.nullcheck_time                     =   int(self.config.get("bdNullCheck","time"))
        self.levels_weekLimit                   =   int(self.config.get("Levels","week_limit"))
        self.levels_expMsg                      =   int(self.config.get("Levels","exp_msg"))
        self.levels_lenMsg                      =   int(self.config.get("Levels","len_msg"))
        self.levels_newLvl                      =   int(self.config.get("Levels","new_lvl"))
        self.levels_todayBonus                  =   int(self.config.get("Levels","today_bonus"))
        self.levels_lengthWeek                  =   int(self.config.get("Levels","length_week"))
        self.levels_topAliases                  =   set(self.config.get("Levels","top_aliases").split(","))
        self.levels_personalInfoAliases         =   set(self.config.get("Levels","personal_info_aliases").split(","))
        self.levels_topLines                    =   int(self.config.get("Levels","top_lines"))
        self.levels_topPositions                =       self.config.get("Levels","top_positions")
        self.levels_moneyLevelUp                = float(self.config.get("Levels","money_level_up"))
        self.timevoice_moneyRewards             =       self.config.get("TimeVoice","money_rewards")
        self.timevoice_rolesRewards               =       self.config.get("TimeVoice","roles_rewards")
        self.economy_balanceAliases             =   set(self.config.get("Economy","balance_aliases").split(","))
        self.economy_topAliases                 =   set(self.config.get("Economy","top_aliases").split(","))
        self.economy_topLines                   =       self.config.get("Economy","top_lines").split(",")
        self.economy_topPositions               =       self.config.get("Economy","top_positions").split(",")
        self.buyrole_roles                      =       self.config.get("BuyRole","roles")
        self.pvc_category                       =   int(self.config.get("PVC","category"))
        self.pvc_runChannel                     =   int(self.config.get("PVC","run_channel"))
        self.pvc_slots                          =   int(self.config.get("PVC","slots"))
        self.pvc_days                           =   int(self.config.get("PVC","days"))
        self.timeroles_time                     =   int(self.config.get("TimeRoles","time"))
        self.timeroles_roles                    =       self.config.get("TimeRoles","roles")
        self.lav_roles                          =       self.config.get("LaV_rewards","roles")
        self.admmsg_custom                      =       self.config.get("admMSG","custom").replace("\\n","\n")
        self.admmsg_cmdBuyRoleImage             =       self.config.get("admMSG","cmd_buyrole_image")
        self.music_playAliases                  =   set(self.config.get("Music","play_aliases").split(","))
        self.dev_devolopers                     =   set(int(i) for i in self.config.get("Dev","devolopers").split(","))
        #   Replics
        self._replics                           ={
            "serverstatusInVoiceChannelName"    :       self.config.get("Replics","serverstatus_in_voice_channel_name").replace("\\n","\n"),
            "serverstatusInServerChannelName"   :       self.config.get("Replics","serverstatus_in_server_channel_name").replace("\\n","\n"),
            "admmsgRolesMSG"                    :       self.config.get("Replics","admmsg_roles_msg").replace("\\n","\n"),
            "admmsgRulesDuelMSG"                :       self.config.get("Replics","admmsg_rules_duel_msg").replace("\\n","\n"),
            "admmsgRulesChatMSG"                :       self.config.get("Replics","admmsg_rules_chat_msg").replace("\\n","\n"),
            "admmsgRulesVoiceMSG"               :       self.config.get("Replics","admmsg_rules_voice_msg").replace("\\n","\n"),
            "admmsgWelcomeMSG"                  :       self.config.get("Replics","admmsg_welcome_msg").replace("\\n","\n"),
            "admmsgCmdGlobalMSG"                :       self.config.get("Replics","admmsg_cmd_global_msg").replace("\\n","\n"),
            "admmsgCmdMusicMSG"                 :       self.config.get("Replics","admmsg_cmd_music_msg").replace("\\n","\n"),
            "admmsgCmdHelpMSG"                  :       self.config.get("Replics","admmsg_cmd_help_msg").replace("\\n","\n"),
            "admmsgCmdBuyRoleMSG"               :       self.config.get("Replics","admmsg_cmd_buyrole_msg").replace("\\n","\n"),
            "duelsUserNotFound"                 :       self.config.get("Replics","duels_user_not_found").replace("\\n","\n"),
            "duelsSendMyself"                   :       self.config.get("Replics","duels_send_myself").replace("\\n","\n"),
            "duelsSendBot"                      :       self.config.get("Replics","duels_send_bot").replace("\\n","\n"),
            "duels2PAlreadyIn"                  :       self.config.get("Replics","duels_2p_already_in").replace("\\n","\n"),
            "duels1PAlreadyIn"                  :       self.config.get("Replics","duels_1p_already_in").replace("\\n","\n"),
            "duels1PAlreadyRequest"             :       self.config.get("Replics","duels_1p_already_request").replace("\\n","\n"),
            "duels1PAlreadySendRequest"         :       self.config.get("Replics","duels_1p_already_send_request").replace("\\n","\n"),
            "duelsInvite"                       :       self.config.get("Replics","duels_invite").replace("\\n","\n"),
            "duelsNoShot"                       :       self.config.get("Replics","duels_no_shot").replace("\\n","\n"),
            "duelsNoAnswer"                     :       self.config.get("Replics","duels_no_answer").replace("\\n","\n"),
            "duelsConsent"                      :       self.config.get("Replics","duels_consent").replace("\\n","\n"),
            "duelsQueue"                        :       self.config.get("Replics","duels_queue").replace("\\n","\n"),
            "duelsDraw"                         :       self.config.get("Replics","duels_draw").replace("\\n","\n"),
            "duelsShotLose"                     :       self.config.get("Replics","duels_shot_lose").replace("\\n","\n"),
            "duelsShotWin"                      :       self.config.get("Replics","duels_shot_win").replace("\\n","\n"),
            "duelsNullRejection"                :       self.config.get("Replics","duels_null_rejection").replace("\\n","\n"),
            "duelsRejection"                    :       self.config.get("Replics","duels_rejection").replace("\\n","\n"),
            "duelsEscape"                       :       self.config.get("Replics","duels_escape").replace("\\n","\n"),
            "duelsNullConsent"                  :       self.config.get("Replics","duels_null_consent").replace("\\n","\n"),
            "duels2PAlreadySendRequest"         :       self.config.get("Replics","duels_2p_already_send_request").replace("\\n","\n"),
            "duels2PAlreadyRequest"             :       self.config.get("Replics","duels_2p_already_request").replace("\\n","\n"),
            "duelsNoConsent"                    :       self.config.get("Replics","duels_no_consent").replace("\\n","\n"),
            "duelsNoDuel"                       :       self.config.get("Replics","duels_no_duel").replace("\\n","\n"),
            "duelsTopTitle"                     :       self.config.get("Replics","duels_top_title").replace("\\n","\n"),
            "duelsTopLine"                      :       self.config.get("Replics","duels_top_line").replace("\\n","\n"),
            "duelsTopNoneUser"                  :       self.config.get("Replics","duels_top_none_user").replace("\\n","\n"),
            "duelsStatistics"                   :       self.config.get("Replics","duels_statistics").replace("\\n","\n"),
            "levelsLevelUp"                     :       self.config.get("Replics","levels_level_up").replace("\\n","\n"),
            "levelsTopTitle"                    :       self.config.get("Replics","levels_top_title").replace("\\n","\n"),
            "levelsTopLine"                     :       self.config.get("Replics","levels_top_line").replace("\\n","\n"),
            "levels1PLevel"                     :       self.config.get("Replics","levels_1p_level").replace("\\n","\n"),
            "levels2PLevel"                     :       self.config.get("Replics","levels_2p_level").replace("\\n","\n"),
            "levelsTopNoneUser"                 :       self.config.get("Replics","levels_top_none_user").replace("\\n","\n"),
            "statisticsTitle"                   :       self.config.get("Replics","statistics_title").replace("\\n","\n"),
            "statisticsDescription"             :       self.config.get("Replics","statistics_description").replace("\\n","\n"),
            "statisticsFields"                  :       self.config.get("Replics","statistics_fields").replace("\\n","\n"),
            "economy1PBalance"                  :       self.config.get("Replics","economy_1p_balance").replace("\\n","\n"),
            "economy2PBalance"                  :       self.config.get("Replics","economy_2p_balance").replace("\\n","\n"),
            "economyTopTitle"                   :       self.config.get("Replics","economy_top_title").replace("\\n","\n"),
            "economyTopLine"                    :       self.config.get("Replics","economy_top_line").replace("\\n","\n"),
            "economyTopNoneUser"                :       self.config.get("Replics","economy_top_none_user").replace("\\n","\n"),
            "buyroleNoArgs"                     :       self.config.get("Replics","buyrole_no_args").replace("\\n","\n"),
            "buyroleNoRole"                     :       self.config.get("Replics","buyrole_no_role").replace("\\n","\n"),
            "buyroleNoMoney"                    :       self.config.get("Replics","buyrole_no_money").replace("\\n","\n"),
            "buyroleSuccessfully"               :       self.config.get("Replics","buyrole_successfully").replace("\\n","\n"),
            "pvcKickSuccessfully"               :       self.config.get("Replics","pvc_kick_successfully").replace("\\n","\n"),
            "pvcUserNoInChannel"                :       self.config.get("Replics","pvc_user_no_in_channel").replace("\\n","\n"),
            "pvcNoChannel"                      :       self.config.get("Replics","pvc_no_channel").replace("\\n","\n"),
            "pvcNameChannel"                    :       self.config.get("Replics","pvc_name_channel").replace("\\n","\n"),
            "checksUserNotFound"                :       self.config.get("Replics","checks_user_not_found").replace("\\n","\n"),
            "checksSendBot"                     :       self.config.get("Replics","checks_send_bot").replace("\\n","\n"),
            "messagePrivate"                    :       self.config.get("Replics","message_private").replace("\\n","\n"),
            "messageOnJoinPrivate"              :       self.config.get("Replics","message_on_join_private").replace("\\n","\n"),
            }
        #   Aliases
        self._aliases                           ={
            "command_admmsg"                    :   set(self.config.get("admMSG","aliases").split(",")),
            "command_duels"                     :   set(self.config.get("Duels","aliases").split(",")).union(self.duels_shotAliases),
            "command_levels"                    :   self.levels_topAliases.union(self.levels_personalInfoAliases),
            "command_statistics"                :   set(self.config.get("Statistics","aliases").split(",")),
            "command_economy"                   :   self.economy_balanceAliases.union(self.economy_topAliases),
            "command_buyrole"                   :   set(self.config.get("BuyRole","aliases").split(",")),
            "command_pvc_kick"                  :   set(self.config.get("PVC","kick_aliases").split(",")),
            "command_music"                     :   self.music_playAliases,
            "command_dev"                       :   set(self.config.get("Dev","aliases").split(",")),
            }
        return self
    async def edit(self,section,param,value):
        self.config.set(section,param,value)
        with open(self.path,"w",encoding='utf-8') as config:
            self.config.write(config)
        return self.parser()