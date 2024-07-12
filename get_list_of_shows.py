import re

def extract_show_name(file_name):
    """
    Extract the show name from the file name.
    """
    # Regular expression pattern to match the show name
    result = re.sub(r'S\d{2}.*$', '', file_name)
    result = re.sub(r'\b\d{4}\b', '', result)
    result = re.sub(r'(?i)Integrale.*', '', result)
    result = re.sub(r'\[.*?\]', '', result)
    result = re.sub(r'(?i)COMPLETE.*', '', result)
    result = re.sub(r'-.*$', '', result)

    result = result.replace(".", " ")
    result = re.sub(r'\s{2,}', ' ', result)
    return result.strip()

def list_of_dir_to_shows(file_list):
    # Set to store unique show names
    unique_shows = set()

    # Loop through the file list and extract unique show names
    for file_name in file_list:
        show_name = extract_show_name(file_name)
        # print(file_name, "---->" ,repr(show_name))
        unique_shows.add(show_name)

    return unique_shows

# récupérer les fichiers dans qbittorent
file_list = ["Mindhunter.S01.MULTi.HDR.DV.2160p.NF.WEB-DL.DDP5.1.H265-R3MiX","Rome.S01.MULTi.1080p.BluRay.x265-FLOP","The.Rising.of.the.Shield.Hero.S01.MULTi.1080p.BluRay.x264-T3KASHi","3.Body.Problem.S01.MULTi.HDR.2160p.WEB.H265-FW","True.Detective.S01.Multi.Truefrench.1080p.Bluray.x265-XMiCHOU","The.Shield.S01.1080p.Multi.Bluray.X265-Papaya","Happy.Valley.S01.MULTi.1080p.BluRay.x264-NoNE","Unbelievable.S01.MULTi.1080p.NF.WEB.H264-UNiKORN","The.Night.Of.S01.MULTi.1080p.WEB.H264-NoNE","Homeland.S01.Multi.Bluray.1080p.x265-SN2P","Ripley.S01.MULTi.1080p.WEB.x264-FW","Chernobyl S01 (2019) MULTi VFI 2160p 10bit 4KLight HDR BluRay DTS-HDMA 5.1 x265-QTZ","24 Heures Chrono - S01 - Multi HEVC-AC3","Succession.S01.MULTi.1080p.10bits.MULTi.BLURAY.x265.AvALoN","Severance.2022.S01.MULTi.1080p.10bit.WEBRiP.x265.HEVC.EAC3-JOC.AvALoN","House.Of.Cards.S01.MULTi.1080p.PROPER.HDLight.x264.5.1-TRUNKDU92","Violet Evergarden S01 + OVA (2018) CUSTOM MULTi 1080p 10bits BluRay x265 AAC -Punisher694","The.Expense.S01","The.Long.Shadow.S01.MULTi.1080p.WEB.x264-FW","Sugar.2024.S01E01.MULTi.HDR.DV.2160p.WEB.H265-FW","[SR-71] Re Zero kara Hajimeru Isekai Seikatsu S01 VOSTFR [1080p][X265][10BITS]","Better.Call.Saul.2015.S01.MULTI.1080p.BluRay.x265-SceneGuardians","Shogun.2024.S01E01.MULTi.HDR.DV.2160p.WEB.H265-FW","Dark.S01.MULTi.1080p.NF.WEBRip.5.1.x265-R3MiX","Sugar.2024.S01E02.MULTi.HDR.DV.2160p.WEB.H265-FW","Shogun.2024.S01E10.FiNAL.MULTi.HDR.DV.2160p.WEB.H265-FW","Shogun.2024.S01E08.MULTi.HDR.DV.2160p.WEB.H265-FW","Shogun.2024.S01E02.MULTi.HDR.DV.2160p.WEB.H265-FW","Shogun.2024.S01E05.MULTi.HDR.DV.2160p.WEB.H265-FW","Shogun.2024.S01E06.MULTi.HDR.DV.2160p.WEB.H265-FW","Shogun.2024.S01E04.MULTi.HDR.DV.2160p.WEB.H265-FW","Shogun.2024.S01E07.MULTi.HDR.DV.2160p.WEB.H265-FW","The.Fall.S01.MULTi.1080p.BluRay.HDLight.x265-H4S5S","Shogun.2024.S01E03.MULTi.HDR.DV.2160p.WEB.H265-FW","Kaamelott.S01.FRENCH.DVDRip.XViD-RULE","Star.Wars.Tales.of.the.Empire.S01.MULTi.1080p.WEB.H264-FW","Shogun.2024.S01E09.MULTi.1080p.WEB.H264-FW","Sugar.2024.S01E03.L.incrocio.di.Shibuya.ITA.ENG.1080p.ATVP.WEB-DL.DDP5.1.H.264-MeM.GP.mkv","Dark.Matter.2024.S01E02.MULTi.1080p.WEB.H265-FW","The.Acolyte.S01E01.MULTi.1080p.WEB.H264-FW","Dark.Matter.2024.S01E03.MULTi.1080p.WEB.H265-FW","The.Acolyte.S01E02.MULTi.1080p.WEB.H264-FW","Dark.Matter.2024.S01E01.MULTi.1080p.WEB.H265-FW","The.Office.S01.Multi.Web-DL.1080p.x265-SN2P","Solo.Leveling.S01E02.SUBFRENCH.1080p.WEB.x264.AAC-Tsundere-Raws.mkv","Solo.Leveling.S01E10.SUBFRENCH.1080p.WEB.x264.AAC-Tsundere-Raws.mkv","Solo.Leveling.S01E04.SUBFRENCH.1080p.WEB.x264.AAC-Tsundere-Raws.mkv","Solo.Leveling.S01E03.SUBFRENCH.1080p.WEB.x264.AAC-Tsundere-Raws.mkv","Solo.Leveling.S01E01.SUBFRENCH.1080p.WEB.x264.AAC-Tsundere-Raws.mkv","Solo.Leveling.S01E07.VOSTFR.1080p.WEBRiP.x265-KAF.mkv","Solo.Leveling.S01E06.VOSTFR.1080p.WEBRiP.x265-KAF.mkv","Solo.Leveling.S01E05.VOSTFR.1080p.WEBRiP.x265-KAF.mkv","Solo.Leveling.S01E08.VOSTFR.1080p.WEBRiP.x265-KAF.mkv","Sugar 2024 S01E07 1080p WEB H264-SuccessfulCrab","Sugar 2024 S01E05 1080p WEB H264-SuccessfulCrab","Sugar.2024.S01E06.720p.WEB.x265-MiNX[TGx]","Sugar 2024 S01E04 1080p WEB H264-SuccessfulCrab","Sugar 2024 S01E08 Farewell 1080p ATVP WEB-DL DDP5 1 Atmos H 264-FLUX"]

unique_shows1 = list_of_dir_to_shows(file_list)

for show in sorted(unique_shows1):
    print(repr(show))


print('------------------')

import os

path = '/media/downloads/complete'

# Get a list of all directories in the specified path
directories = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

unique_shows2 = list_of_dir_to_shows(directories)

for show in sorted(unique_shows2):
    print(repr(show))

print(len(unique_shows1), len(unique_shows2))