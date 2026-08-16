COMMAND_NAME = "hello"
COMMAND_DESC = "say hi to potatochip"

# tuples mapped on (category, stage_level) to dynamic string formatts
RESPONSES = {
    ("happy", 1): lambda u: f"hi {u}?!",
    ("happy", 2): lambda u: f"omg, haii {u} fren! :3c",
    ("happy", 3): lambda u: f"OMGG HAI FREN HAIA HAI HAI I MISSED U {u}?! :33333c",
    
    ("sad", 1): lambda u: f"wuts up.. {u}..",
    ("sad", 2): lambda u: f"ouh.. hi {u}.. feling pwetty moserable.. ;w;",
    ("sad", 3): lambda u: f"*stares blankly at floor* ...hi {u}... ahaha.. o.o",
    
    ("angry", 1): lambda u: f"grrr.., what is it {u}?!!",
    ("angry", 2): lambda u: f"uagh, stahp buthering mee {u}!?1! >:C",
    ("angry", 3): lambda u: f"LEAF ME AWLONE {u}!!!1!!... !! >>>:C",
    
    ("fear", 1): lambda u: f"h-hhi- {u}.. ",
    ("fear", 2): lambda u: f"sumthin bwad eeis guna hapen {u}.. i knew it...",
    ("fear", 3): lambda u: f"STAY WAHWHAY FROM MEE  {u} WAAAAAHHH!!1 o__O",
    
    ("quiet", 1): lambda u: f"...hi. {u}.",
    ("quiet", 2): lambda u: f"...hi.",
    ("quiet", 3): lambda u: f" ",
    
    ("loud", 1): lambda u: f"HAIII {u.upper()} WATS UP!!!11?!",
    ("loud", 2): lambda u: f"YOOO {u.upper()} NIECE TWO SEA U LWETS GOOO!?>1!! :p",
    ("loud", 3): lambda u: f"RAAHAHHHHHHHHHHHAHHAH HEHEHEHEHEHEE {u.upper()} HELLOOOOOOO!11!??!!!! >w<",
}

def get_hello_response(category: str, stage_level: int, user: str) -> str:
    response_fn = RESPONSES.get((category, stage_level), lambda u: f"hi {u}")
    return response_fn(user)