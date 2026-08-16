COMMAND_NAME = "feed"
COMMAND_DESC = "give potatochip something to eat"
FOOD_DES = "wat u feed pohatoe chip"

# maps (highest_stat_increased, final_dominant_mood) to a response string.
RESPONSES = {
    # happy inc
    ("happy", "happy"): lambda f: f"OMG THAMK YUU FOR GIVING MEE **{f}**!! ITS LIEK ONE OF MY FVARUITEEES EEEE THANK UU :33333",
    ("happy", "sad"): lambda f: f"i deid enjoi the **{f}** a litle bit.... ahah ttthank you for the treat... ;w;",
    ("happy", "angry"): lambda f: f"this **{f}** is realy nice but auaghhwhwbhwaf,i stil feele so upsoett !1! ;c",
    ("happy", "fear"): lambda f: f"nom nmom.., tthnak you...",
    ("happy", "quiet"): lambda f: f".. thnaks for the **{f}**.",
    ("happy", "loud"): lambda f: f"NOM NOM NOMN ONMONMNOM **{f}** HEHEHEHEHEHEHEHEE THANUUK YYUU :3c",

    # sad inc
    ("sad", "happy"): lambda f: f"ahaha, how did you know that **{f}** would cheer me up.. hehe..",
    ("sad", "sad"): lambda f: f"waahahhhh... ;c",
    ("sad", "angry"): lambda f: f"thanks for the **{f}** twt hmpft.. ",
    ("sad", "fear"): lambda f: f"auagahahaa i cant take it no mor ;w;",
    ("sad", "quiet"): lambda f: f"... ;c",
    ("sad", "loud"): lambda f: f"WAHUAUHAUAUAHAHAHUAHHA ;W; TwT",

    # angry inc
    ("angry", "happy"): lambda f: f"GRAHUGHGAHA YUMMMEYY, THANMK FOR THE **{f}**",
    ("angry", "sad"): lambda f: f"GRAAAHH THE **{f}** TASTES LIKE ASS TWT",
    ("angry", "angry"): lambda f: f"GRAAAHHAWDHWFFWAWFBJAWFJBKFWABH >;c",
    ("angry", "fear"): lambda f: f"mmmm whwhwat is hrthata.. *nom's **{f}*** ",
    ("angry", "quiet"): lambda f: f"munch munch munch >.>",
    ("angry", "loud"): lambda f: f"pWAHAHAHAHAAH DIS IS SO GOOD I COUDLD DIE",

    # fear inc
    ("fear", "happy"): lambda f: f"waah, wtf is dis... **{f}**, ough wait its yumy, thamk u.",
    ("fear", "sad"): lambda f: f"guwah *gag* uagh.... ;w; why",
    ("fear", "angry"): lambda f: f"UWAH WAT DAT FUK IS **{f}** =wdjkbwafjkafwjkafjk",
    ("fear", "fear"): lambda f: f"*shakes in fear*",
    ("fear", "quiet"): lambda f: f"mm.. thanks.. bye",
    ("fear", "loud"): lambda f: f"AAHAHAHAHHAH WHFFF IS TAHATAT GET IT AWYA FORM MEE. ",

    # quiet inc
    ("quiet", "happy"): lambda f: f"C:",
    ("quiet", "sad"): lambda f: f":C",
    ("quiet", "angry"): lambda f: f">.>",
    ("quiet", "fear"): lambda f: f">-<",
    ("quiet", "quiet"): lambda f: f"...",
    ("quiet", "loud"): lambda f: f"... YAAAAYAYAYSYDYDUAWHWHK",

    # loud inc
    ("loud", "happy"): lambda f: f"YAYAYAYAYAY I GET TOT EAT **{f}**!",
    ("loud", "sad"): lambda f: f"BWAAAHHH I HAVE TO EQT **{f}**!?? ;W;",
    ("loud", "angry"): lambda f: f"GRHWAJDAFAF **{f}** ISS SEWW GOOD DI NEEED MORE I ENED ITT NWOWWW! !!11",
    ("loud", "fear"): lambda f: f"WAAAHAH WHWY IS IT WEIRD THE **{f}** IS SWCARYR ;C!",
    ("loud", "quiet"): lambda f: f"BURRRP. oh.",
    ("loud", "loud"): lambda f: f"*deafens u* MWAH MUWANCH MUCNH NOM NOMNOMNOMNOMNOMNOMN  !!!!!!!",
}

def get_feed_response(food: str, highest_emo: str, final_mood_category: str) -> str:
    # all negative edge case
    if highest_emo == "none":
        return f"stare..."
        
    response_fn = RESPONSES.get((highest_emo, final_mood_category))
    
    # fallback
    if not response_fn:
        return f"potatochip ate the **{food}**!"
        
    return response_fn(food)