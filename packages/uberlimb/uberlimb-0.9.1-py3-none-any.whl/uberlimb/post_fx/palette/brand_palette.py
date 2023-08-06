from typing import Dict, List

from uberlimb.parameters import FrameColorMap


def hex2dict(hex_string: str) -> Dict:
    return {
        'r': [0, int(hex_string[0][1:3], 16), int(hex_string[1][1:3], 16), int(hex_string[2][1:3], 16), 255],
        'g': [0, int(hex_string[0][3:5], 16), int(hex_string[1][3:5], 16), int(hex_string[2][3:5], 16), 255],
        'b': [0, int(hex_string[0][5:7], 16), int(hex_string[1][5:7], 16), int(hex_string[2][5:7], 16), 255]
    }


hex_palettes = {
    "JetBrains": ["#ed3d7d", "#7c59a4", "#fcee39"],
    "Space": ["#009AE5", "#3BEA62", "#FCF84A"],
    "IntelliJ IDEA": ["#087cfa", "#fe2857", "#fc801d"],
    "PhpStorm": ["#b74af7", "#6b57ff", "#ff318c"],
    "PyCharm": ["#21d789", "#fcf84a", "#07c3f2"],
    "RubyMine": ["#fe2857", "#fc801d", "#6b57ff"],
    "WebStorm": ["#07c3f2", "#087cfa", "#fcf84a"],
    "CLion": ["#21d789", "#009ae5", "#ed358c"],
    "DataGrip": ["#21d789", "#6b57ff", "#ff318c"],
    "AppCode": ["#087cfa", "#07c3f2", "#21d789"],
    "GoLand": ["#087cfa", "#b74af7", "#3bea62"],
    "ReSharper": ["#dd1265", "#ff45ed", "#fdb60d"],
    "ReSharper C++": ["#fdb60d", "#ff45ed", "#dd1265"],
    "dotCover": ["#fc801d", "#7866ff", "#ff45ed"],
    "dotMemory": ["#fdbc2c", "#6b57ff", "#ff45ed"],
    "dotPeek": ["#00caff", "#6b57ff", "#e343e6"],
    "dotTrace": ["#fc1681", "#6b57ff", "#ff45ed"],
    "Rider": ["#c90f5e", "#087cfa", "#fdb60d"],
    "TeamCity": ["#07c3f2", "#6b57ff", "#3bea62"],
    "YouTrack": ["#07c3f2", "#6b57ff", "#ff318c"],
    "Upsource": ["#22b1ef", "#9062f7", "#fd8224"],
    "Hub": ["#00b8f1", "#9758fb", "#ffee45"],
    "Kotlin": ["#22b1ef", "#9062f7", "#fd8224"],
    "Mono": ["#ffffff", "#4c4c4c", "#000000"],
    "MPS": ["#087cfa", "#21d789", "#fcf84a"],
    "IntelliJ IDEA Edu": ["#f97a12", "#fe2857", "#fc801d"],
    "PyCharm Edu": ["#f4e800", "#fcf84a", "#07c3f2"],
    "DataSpell": ["#21d789", "#fcf84a", "#087cfa"],
    "Qodana": ["#07c3f2", "#6b57ff", "#fa3290"],
    "Datalore": ["#087cfa", "#fcf84a", "#3bea62"],
    "CodeWithMe": ["#3bea62", "#009aaf", "#6b57ff"],
}

rgb_palette = {}
for k, v in hex_palettes.items():
    rgb_palette[k] = hex2dict(v)

PALETTE: Dict[FrameColorMap, Dict[str, List[int]]] = {
    FrameColorMap.BC_JETBRAINS: rgb_palette['JetBrains'],
    FrameColorMap.BC_SPACE: rgb_palette['Space'],
    FrameColorMap.BC_IDEA: rgb_palette['IntelliJ IDEA'],
    FrameColorMap.BC_PHPSTORM: rgb_palette['PhpStorm'],
    FrameColorMap.BC_PYCHARM: rgb_palette['PyCharm'],
    FrameColorMap.BC_RUBYMINE: rgb_palette['RubyMine'],
    FrameColorMap.BC_WEBSTORM: rgb_palette['WebStorm'],
    FrameColorMap.BC_CLION: rgb_palette['CLion'],
    FrameColorMap.BC_DATAGRIP: rgb_palette['DataGrip'],
    FrameColorMap.BC_APPCODE: rgb_palette['AppCode'],
    FrameColorMap.BC_GOLAND: rgb_palette['GoLand'],
    FrameColorMap.BC_RESHARPER: rgb_palette['ReSharper'],
    FrameColorMap.BC_RESHARPER_C: rgb_palette['ReSharper C++'],
    FrameColorMap.BC_DOTCOVER: rgb_palette['dotCover'],
    FrameColorMap.BC_DOTMEMORY: rgb_palette['dotMemory'],
    FrameColorMap.BC_DOTPEEK: rgb_palette['dotPeek'],
    FrameColorMap.BC_DOTTRACE: rgb_palette['dotTrace'],
    FrameColorMap.BC_RIDER: rgb_palette['Rider'],
    FrameColorMap.BC_TEAMCITY: rgb_palette['TeamCity'],
    FrameColorMap.BC_YOUTRACK: rgb_palette['YouTrack'],
    FrameColorMap.BC_UPSOURCE: rgb_palette['Upsource'],
    FrameColorMap.BC_HUB: rgb_palette['Hub'],
    FrameColorMap.BC_KOTLIN: rgb_palette['Kotlin'],
    FrameColorMap.BC_MONO: rgb_palette['Mono'],
    FrameColorMap.BC_MPS: rgb_palette['MPS'],
    FrameColorMap.BC_IDEA_EDU: rgb_palette['IntelliJ IDEA Edu'],
    FrameColorMap.BC_PYCHARM_EDU: rgb_palette['PyCharm Edu'],
    FrameColorMap.BC_DATASPELL: rgb_palette['DataSpell'],
    FrameColorMap.BC_QODANA: rgb_palette['Qodana'],
    FrameColorMap.BC_DATALORE: rgb_palette['Datalore'],
    FrameColorMap.BC_CODEWITHME: rgb_palette['CodeWithMe'],
    FrameColorMap.APPLELIKERNBW: {
        'r': [int('5e', 16), int('ff', 16), int('f7', 16), int('e2', 16),
              int('97', 16), int('00', 16), int('00', 16)],
        'g': [int('bd', 16), int('b9', 16), int('82', 16), int('38', 16),
              int('39', 16), int('9c', 16), int('9c', 16)],
        'b': [int('3e', 16), int('00', 16), int('00', 16), int('38', 16),
              int('99', 16), int('df', 16), int('df', 16)]},
    FrameColorMap.VALERACUSTOM: {
        'r': [int('f3', 16), int('82', 16), int('49', 16), int('bb', 16),
              int('f3', 16), int('00', 16)],
        'g': [int('64', 16), int('f3', 16), int('d7', 16), int('49', 16),
              int('d7', 16), int('9c', 16)],
        'b': [int('49', 16), int('49', 16), int('f3', 16), int('f3', 16),
              int('49', 16), int('df', 16)]},
}
