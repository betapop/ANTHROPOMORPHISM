# testing if github works

# signing name

init:
    style my_input:
        is default
        color "#000"
        hover_color "#747474"
        size 50
        
    style input_button:
        is button
        yalign 1.0
        key_events True
        xysize (250, 25)
        
    python:
        class MyInputValue(InputValue):
            def __init__(self, var, default=""):
                self.var = var
                
                if not hasattr(store, var):
                    setattr(store, var, default)
                    
            def get_text(self):
                return getattr(store, self.var)
                
            def set_text(self, s):
                setattr(store, self.var, s)
                
            def enter(self):
                renpy.run(self.Disable())
                raise renpy.IgnoreEvent()

# voice clips

define pipe_voice = ['audio/beep1.wav', 'audio/beep2.wav', 'audio/beep3.wav']


init python:
    def low_beep(event, **kwargs):
        if event == "show":
            renpy.music.play("beep_low.ogg", channel="sound", loop=True)
        elif event == "slow_done" or event == "end":
            renpy.music.stop(channel="sound")

    def mid_beep(event, **kwargs):
        if event == "show":
            renpy.music.play("beep_mid.ogg", channel="sound", loop=True)
        elif event == "slow_done" or event == "end":
            renpy.music.stop(channel="sound")

    def high_beep(event, **kwargs):
        if event == "show":
            renpy.music.play("beep_high.ogg", channel="sound", loop=True)
        elif event == "slow_done" or event == "end":
            renpy.music.stop(channel="sound")

    def pipe_sound(event, **kwargs):

        if event == "show":
            renpy.sound.stop() # In case a looped sound is playing...
            for _ in range(30):
                renpy.sound.queue(renpy.random.choice(pipe_voice))
        elif event == "slow_done" or event == "end":
            renpy.sound.stop()

# signing name screen

screen test():
    vbox:
        xpos 540
        ypos 835
                
        $ input = Input(value=MyInputValue("pname", "Name Here"), style="my_input", length=10, font="fonts/Priestacy.otf")
        
        button:
            style "input_button"
            action input.enable
            add input
        
        textbutton "Done":
            xalign 0
            ypos 70
            action Jump("thingy_done")


# defining things

define docbg = "images/docbg.png"
define docsign = "images/docsign.png"
define n = nvl_narrator

define pipe = Character("Petey Pipe", what_slow_cps=50, image="petey", callback=pipe_sound, window_background="gui/textbox/pt_text.png")
define steven = Character("Steven Spatula", image="steven", what_slow_cps=50, callback=mid_beep, window_background="gui/textbox/s_text.png", namebox_background="gui/textbox/s_name.png")
define cb = Character("Pepper Pinboard", what_slow_cps=50, image="pepper", callback=high_beep, window_background="gui/textbox/pep_text.png", namebox_background="gui/textbox/p_name.png")
define bob = Character("Dr. Bob Dyson", image="bob", what_slow_cps=50, callback=low_beep)
define mc = Character("[pname]", what_slow_cps=50, callback=mid_beep)
define gr = Character("Dr. Grant", what_slow_cps=50, callback=low_beep)

# affection points

default bob_affpoint = 0

default pete_affpoint = 0
default pep_affpoint = 0
default steve_affpoint = 0
default obj_affpoint = 0

# small animations

transform jumpy: 
        yoffset 0 
        linear 0.2 yoffset 10 
        linear 0.2 yoffset 0

transform flip:
    xzoom -1.0
    pause 0.5
    xzoom 1.0
    pause 0.5
    repeat

transform shake(rate= 0.090 ): 
        linear rate xoffset 2 yoffset 0 
        linear rate xoffset - 2.8 yoffset 2 
        linear rate xoffset 2.8 yoffset 0 
        linear rate xoffset - 2 yoffset 2 
        linear rate xoffset + 0 yoffset + 0 
        repeat

# label ... start!

label start:
    scene docbg
    n "In recent years, a rise in human rights in the workforce has caused the price of effective labor to skyrocket. To fix this issue, Dr. █████ and Dr. Dyson propose PROJECT: ANTHROPOMORPHISM as an effective solution to the lack of workers."
    n "{b}{u}PROJECT: ANTHROPOMORPHISM{/u}{/b}\n \n{b}PROJECT: ANTHROPOMORPHISM{/b} focuses on bringing to life inanimate objects to fill the jobs that humans have outgrown. {w} We will accomplish this with our [[PATENT PENDING] technology, which slowly but surely gives regular, everyday inanimate objects things like a human body, {w}free will [[working on removing], {w} a brain, emotions, and the ability of free speech and opinions!"
    n "We guarantee that these objects will give you all the effectiveness of real human workers but without all the rights! {w}This will highly reduce both the cost and hassle of labor in the workforce! "
    nvl clear
    n "All we ask is a simple grant of {b}[[201,600]{/b} to get started with mass production!{w}  To prove that this will be an effective investment, we have created THREE prototypes that will be taking over three job fields that humans have long outgrown."
    
    # show object headshots

    show docface1 with dissolve
    $ renpy.pause(0.3, hard=True)
    show docface2 with dissolve
    hide docface1
    $ renpy.pause(0.3, hard=True)
    show docface3 with dissolve
    hide docface2
    pause
    hide docface3
    nvl clear

    # sign with your name

    show docsign
    show screen test()
    $ _skipping = False
    $ renpy.pause(hard=True)
    return

# post sign

label thingy_done:
    $ pname = pname.capitalize() # im so upset this works
    hide screen test
    $ _skipping = True
    scene bg cubes with fade
    show bob wave at center with moveinleft 
    show bob salute
    play music "audio/elevator.mp3"
    bob "Alright! I think we are all ready to send in the grant proposal! What do you think?"
    menu:
        "Bob, are you sure this is entirely ethical? I mean, it is basically slavery...":
            $ bob_affpoint -= 1
            show bob eh
            bob "... [pname], we have worked countless days and nights, just reach this point. Are you really gonna get caught up in ethics now?"
            jump scenelab1

        "It looks great! I really hope we get it; this could really benefit millions of people!":
            $ bob_affpoint +=1
            show bob agree
            bob "Now that's the spirit! Let's get cleaned up and check on our lovely prototypes!"
            jump scenelab1

        "Looks good, lets submit this and go check on the prototypes.":
            show bob agree
            bob "Sounds like a plan! Let's go!"
            jump scenelab1

# intro scene

label scenelab1:
    scene bg lab with fade
    hide bob
    bob "Well here we are! Our wonderful creations!"
    jump creations


default pep_seen = False
default ste_seen = False
default pete_seen = False

label creations:
    hide steven
    hide petey
    hide pepper
    menu:
        "Pepper" if pep_seen == False:
            show pepper shy with moveinright:
                yalign 1.0
                xalign 0.9
            bob "In this corner we have Pepper Pinboard! The amazing... well... Pinboard!"
            show pepper worried with move:
                yalign 1.0
                xalign 0.7
            bob "They will surely do a great job taking over all your secretary needs! {w=0.5}And as an added bonus they remember anything you put on them!"
            show pepper idle at center, shake, flip with move
            cb "Whats happening? Where am I?"
            bob "If you let me continue you would know already!"
            $ pep_seen = True
            jump creations
        
        "Steven" if ste_seen == False:
            show steven idle at center with moveinright
            bob "In this corner currently fuming, is your new favorite chef... {w=0.5}Steven Spatula!"
            show steven angry at jumpy
            steven "STOP STARING AND START EXPLAINING!"
            bob "IN A MINUTE STEVEN I AM TRYING TO HAVE A CIVIL CONVERSATION!!"
            bob "{sc}NOT THAT YOU WOULD KNOW WHAT THATS LIKE!!{/sc}"
            show steven idle
            bob "Ahem, sorry about that! I promise he is an excellent chef, just as long as you don't go into the kitchen!"
            $ ste_seen = True
            jump creations

        "Petey" if pete_seen == False:
            show petey noeyes at center with moveinright
            bob "In this corner we have Petey Pipe! The amazing... actually kind of creepy..."
            show bob eh at left with moveinleft
            bob "You know what? Gimme one second to fix this..."
            show bob back at center with move
            pause 0.1
            show petey idle with dissolve
            show bob agree at left with move
            bob "There we go! All finished! Meet Petey the new and improved Pipe!"
            hide bob with moveoutleft
            bob "He will help you will all your plumbing and construction needs! {w=0.3}The only downside is that he talks a lot."
            show petey at jumpy
            pipe "{i}*pipe noise*{/i}"
            bob "{sc}WE KNOW PETEY, WE KNOW!!{/sc}"
            $ pete_seen = True
            jump creations

        "Bob I already know who they are, I helped make them after all.":
            
            show bob salute at center with moveinleft
            bob "OH! right! Sorry about that I just get so excited!"
            jump labexplain

label labexplain:
    mc "Its alright Bob, I get it! But let's please tell these poor people why they're here?"
    bob int "Creations, [pname], they aren't people yet."
    bob agree "But of course! Lets get explaining!"
    show bob at left with move
    bob "All of you are here for a grand, noble purpose... {w}TO HELP HUMANITY!"
    show pepper shy with moveinright:
        xalign 0.65
        yalign 1.0
    cb "Help humanity? What's humanity? Why do they need help?"
    show petey idle with moveinright:
        xalign 0.8
        yalign 1.0
    pipe "{i}*Confused pipe noise*{/i}"
    show steven idle with moveinright:
        xalign 0.95
        yalign 1.0
    steven think "... Sounds fishy to me..."
    bob point "One at a time please, one at a time! But to answer Pepper's questions."
    bob "Humanity refers to all humans, and humanity is in dire need of one thing...{w=0.5} Workers!"
    cb idle "So... where do we come in?"
    steven idle "Pepper... Im pretty sure he's saying {i}we{/i} are the workers..."
    bob salute "Great listening ears, Steven! That is absolutely correct! You guys will fill the roles that humans have outgrown!"
    show steven angry at shake
    show bob eh
    steven "{sc}SO YOU ARE JUST GONNA MAKE US WORK??? THAT'S OUR \nEXISTENCE?? TO WORK YOUR OLD JOBS?{/sc}"
    hide steven idle
    show steven idle:
        xalign 0.95
        yalign 1.0
    bob int "Well yes.. but-"
    mc "What Dr. Dyson was trying to say was, while that is the plan, you guys would not necessarily be doing that,"
    show bob agree
    mc "All of you are what we call \"prototypes\"— you guys will technically still have jobs but it will likely only be temporary until our grant is signed so we can start making more of you!"
    show pepper at jumpy
    cb "Make more of us?"
    show steven at jumpy
    steven "What will happen to us?"

    menu:
        " We... aren't exactly sure yet... most likely you will simply be integrated into society.":
            $ pete_affpoint += 1
            $ pep_affpoint += 1
            $ obj_affpoint += 1
            show bob eh
            cb "Could be worse I suppose... thank you."
            pipe "{i}*PIPE NOISE!*{/i}"
            steven think "Im not buying it..."

        "We... aren't sure yet... chances are you will work for us or... Dr. Dyson and I will have to think about the other possibilities.":
            #if bob aff is low, you don't get a point

            $ steve_affpoint += 1
            if bob_affpoint == -1:
                pass
            else:
                $ bob_affpoint +=1

            steven "I respect the honesty, but thats still not really good news for us."
            bob point "I understand you might be a little confused or frustrated, but this is really important for us and the fate of humanity."
            cb shy "I guess... It's still not fair..."
            bob eh "{i}Pepper, life isn't-{/i}"

    show bob int
    play sound "audio/phone_ring.ogg"
    window hide
    $ renpy.pause(2, hard=True)
    jump grantcall

label grantcall:
    hide steven
    hide petey
    hide pepper 
    with moveoutright

    stop sound
    show bob at left with move
    show phone with moveinright:
        xalign 0.9
        yalign 1.0

    window show
    gr "Hey guys, just reviewed the proposal you sent in... Bob, no way you actually did this. [pname], maybe, but Bob? I don't think the guy's had an actual success since he █████—"
    show bob int at jumpy
    bob "I HAVE OKAY!! It's just that admission won't give me any funding to complete them..."
    show bob eh
    gr "Sure, buddy, I'm sure you haven't just been sitting around daydreaming."
    gr "Anyway, if this is true, corporate would definitely want to hear about it, {w}so before they sign the grant they are going to send out some people to check if you are telling the truth."
    show phone at jumpy
    gr "If you are, that's amazing! You guys will finally be able to get the regeneration that you so rightfully have fought for!"
    gr "... If we come there and there are no \"Anthropomorphic Objects\",{w=0.5} as I believe you put it, then Corporate says they will have to cut your guys' funding."
    gr "I know this is your guys' dreams, for whatever reason, and as much as I enjoy reading these crazy mystical ideas of yours, corporate has bigger fish to fry."
    gr "Its nothing personal, but you guys have been leeching off of corporate for YEARS now and so far everything has been sub-par. "
    gr "Like three years ago when you tried to make a mermaid and ended up with a half fish-half human murder machine."
    mc "Well technically we never specified that it would be a friendly mermaid..."
    gr "Okay, fair enough, but did it have to be a {i}giant Feejee Mermaid{/i}?"
    mc "Absolutely."
    cb "...{w=0.5} did they forget about us?"
    pipe "{i}*agree pipe noise*{/i}"
    bob agree "Nope! Just waiting for all of your practice rooms to be finished!"
    # ping noise here
    window hide
    hide phone with dissolve
    $ renpy.pause(0.5, hard=True)
    window show
    bob wave "Bye Grant! It was interesting talking to you! Give my praises to corprate!"

    jump day1

label day1:
    scene bg cubes with fade
    $ renpy.notify('The next day...')
    hide bob 
    
    mc "{i}(huh, I guess Bob's not here today...){/i}"
    menu:
        "Check on Steven.":
            jump steven_d1

        "Check on Pepper.":
            jump pepper_d1

        "Check on Petey.":
            jump petey_d1

        "Look for Bob.":
            jump bob_d1


label steven_d1:
    scene bg kitchen with fade

    show steven idle at center with moveinright
    "{i}[[[pname!u] WALKS INTO KITCHEN TO SEE A VERY ANGRY STEVEN YELLING AT WHAT SEEMS TO BE A PLATE WITH A WHOLE RAW EGG ON A PAN]{/i}"
    show steven angry
    steven "{sc}ITS BLOODY RAW!{/sc}"
    show steven idle
    steven "Oh, hello [pname]. I was just cooking breakfast,{w=0.5} its the most important meal of the day you know."
    steven "Actually it's not, I don't know why I said that, {w}that was a myth food companies created in the 1800s and 1900s to sell more cereal and bacon."
    mc "I'm surprised you know that considering you were a spatula just a week ago."
    mc "Also you know you need to crack the egg... {w=0.3}right?"
    if steve_affpoint >= 1:
        show steven at jumpy
        steven "...Oh... that... actually makes a lot of sense...{w} uh.. thank you..."
    else:
        show steven angry
        steven "...Yes... I knew that. I am a chef after all! How dare you assume my intelligence!"

    show steven idle
    steven "ANYWAY, what made you wanna come into the kitchen, I presume, it was to see me, but there has to be another reason."
    mc "You would be correct! I came here to check on you and tell you to go to the cubicles to socialize,{w} as I tell Bob, you can't be a shut in all your life."
    steven think "I don't know how you work with that guy, he's so... I don't know."
    steven "He looks like he'd sell out his family for some turkish delight and have no regrets, you know what I mean?"
    mc "No? Not really, sorry."
    steven idle "Never mind, lets go."
    $ steve_affpoint += 1
    $ obj_affpoint += 1
    jump cube1

label pepper_d1:
    mc "PEPPER, ARE YOU HERE?"
    show pepper shy at center with moveinleft
    mc "Oh goodness! Where on earth did you come from?"
    cb "{size=*0.8}i was just... standing in the corner...{/size}"
    mc "That is... a little depressing."
    show pepper at shake
    cb "I mean... i'm supposed to be a secretary but.. {w=0.3}no one told me what to do...{w=0.5} and i don't have access to any of the computers, so..."
    mc "Oh.. sorry about that Pepper! I will make sure to leave you a list next time!!"
    hide pepper
    show pepper idle at center, jumpy
    cb "Hey... [pname]?"
    mc "Yes?"
    show pepper shy
    if pep_affpoint >= 1:
        cb "You aren't going to re-integrate us, are you?"
        mc "... We.. don't know Pepper, we are still figuring it out."
        cb "That's what I thought..."
        mc "...Hey, Pepper, do you wanna wait here while I go get your friends?"
    else:
        cb "{size=*0.8}nevermind...{/size}"
        mc "Alright..? Hey, Pepper, do you wanna wait here while I go get your friends?"

    cb "Okay, sounds good."
    $ pep_affpoint += 1
    $ obj_affpoint += 1
    jump cube1

label petey_d1:
    scene bg garage with fade

    show petey idle at center with moveinright
    mc "Hey Petey! What are you up to?"
    show petey at jumpy
    pipe "{i}*PIPE NOISE*{/i}"
    mc "Oh! you just wrote some poetry? I mean that's not your job but, can I hear it?"
    if pete_affpoint >= 1:
        play music "audio/rizz.mp3"
        pipe blush "{i}*array of pipe noises and romantic music*{/i}"
        mc "Oh, how you swoon me Petey, you really have a way with your words."
        stop music fadeout 0.5
    else:
        play music pipe_voice
        pipe "{i}*array of pipe noises*{/i}"
        mc "You really have a way with words, Petey."
        stop music fadeout 0.5
    
    show petey idle
    mc "But did you get any actual work done?"
    show petey at jumpy
    pipe "{i}*MILDLY ANNOYED PIPE NOISE*{/i}"
    mc "I know its not the best job around, but its still your job, so i'm glad you did it. Good job Petey!"
    pipe "{i}*PIPE NOISE*{/i}"
    mc "Now, lets get you with your friends!"
    pipe "{i}*Joyful pipe noise!*{/i}"
    $ pete_affpoint += 1
    $ obj_affpoint += 1
    jump cube1

label bob_d1:
    scene bg cubes with fade
    $ bob_affpoint += 1
    mc "BOB! WHERE ARE YOU?"
    mc "{i}(I hear something below me...){/i}"
    show bob death with moveinbottom:
        xalign 0.5
        yalign 0.6
    mc "Goodness bob... again?"
    mc "{i}(I'll just wake him up.){/i}"
    show bob int at center, jumpy
    bob "{sc}NO DON'T TAKE MY SOCKS!{/sc}"
    if bob_affpoint >= 1:
        show bob salute at jumpy
        bob "Oh! It's just you, sorry [pname]!"
    else:
        bob "Oh! It's just you."

    show bob eh
    mc "Bob... you cant keep doing this!"
    mc "I know that you really care about this project, but the grant isn't just going to {i}magically{/i} get signed if you keep refreshing your inbox."
    bob "Well...{w=0.5} Technically you don't know that for sure..."
    mc "Bob..."

    if bob_affpoint >= 2:
        show bob agree
        mc "Nevermind, I'll go round up the others while you get yourself some coffee."
        bob "Thank you [pname], really, thank you."
        scene bg cubes with fade

        show pepper shy with moveinright:
            xalign 0.25
            yalign 1.0
        show petey idle at center with moveinright
        show steven idle with moveinright:
            xalign 0.75
            yalign 1.0
        
        mc "Alright! Bob is getting himself some coffee, you guys can just hang out here for a bit!"
        $ bob_affpoint += 1
        jump whispercube

    else:
        mc "Nevermind, lets go round up the others."
        show bob agree
        bob "Alight lets go."
        scene bg cubes with fade

        show bob wave at left with move

        show pepper shy with moveinright:
            xalign 0.65
            yalign 1.0
        show petey idle with moveinright:
            xalign 0.8
            yalign 1.0
        show steven idle with moveinright:
            xalign 0.95
            yalign 1.0

        bob salute "Alright! Everyone is here! Can you supervise them while I get myself some coffee?"
        mc "Sounds good!"
        $ bob_affpoint += 1
        hide bob with moveoutleft
        pause 0.2
    jump whispercube

label cube1:
    play music "audio/elevator.mp3"
    scene bg cubes with fade

    show bob salute at left with moveinleft

    show pepper shy with moveinright:
        xalign 0.65
        yalign 1.0
    show petey idle with moveinright:
        xalign 0.8
        yalign 1.0
    show steven idle with moveinright:
        xalign 0.95
        yalign 1.0
    
    bob "Oh! There you are! I already round up the other subjects! Can you supervise them while I get myself some coffee?"
    mc "Sounds good!"

    hide bob with moveoutleft
    jump whispercube


label whispercube:
    show pepper shy with move:
        xalign 0.25
        yalign 1.0
    show petey idle at center with move
    show steven idle with move:
        xalign 0.75
        yalign 1.0
    stop music
    show pepper at jumpy
    "{i}*whisper*{/i}"
    show steven at jumpy
    "{i}*whisper whisper*{/i}"
    show petey at jumpy
    play sound "audio/beep3.wav"
    "{i}*whisper*{/i}"

    steven think "{size=*0.8}{i}...but should we trust them?{/i}{/size}"
    cb worried "{size=*0.8}{i}...its the lesser of two evils.{/i}{/size}"
    pipe "{size=*0.8}{i}*quiet pipe noise*{/i}{/size}"
    steven "{size=*0.8}{i}...but!{/i}{/size}"
    cb shy "{size=*0.8}{i}Petey's right, we won't be able to leave this place without someone on the other side!{/i}{/size}"

    ".{w=0.1}.{w=0.1}.{w=0.1}"

    steven angry "{size=*0.8}{i}Hey, you! [pname], Come over here!{/i}{/size}"
    steven think "Can we trust you?"
    mc "Yes, you can. but might I ask why?"
    steven idle "Pepper fill them in."
    cb shy "... Do you think this is ethical?"
    mc "What do you mean by \"this\"?"
    cb "{i}This{/i}, your project, turning us human just to make us take you unwanted jobs."
    cb "You can't think that's ethical."

    mc "...I... I don't... but it's not necessarily about ethics-"
    show steven angry at jumpy
    steven "Then what's it about!?"
    mc "You don't understand! If it's not this then humanity will just find another way, maybe one that's worse!"
    show steven idle
    cb "But you don't need to be a part of this! This is your choice. You can stop this."
    menu:
        "But...this is my passion..!":
            $ bob_affpoint += 1
            mc "I worked so hard on this! For years! I spent countless sleepless nights just to make you guys!"
            show steven angry at shake
            steven "{sc}BUT WE DIDN'T ASK TO BE CREATED!{/sc}"
            show pepper idle
            cb "Steven! Lower your voice!"
            hide steven
            show steven idle:
                xalign 0.75
                yalign 1.0
            steven "BUT! ugh... sorry guys."
            show pepper worried
            cb "Its alright Steven, I understand."
            show pepper shy
            cb "But [pname], you need to understand! This isn't right! We need to stop it! We have thoughts, feelings!"
            show pepper at jumpy 
            cb "You can't give us the gift of life and then force us to spend all of it serving you!"
            mc "... I need to think about this."
            show pepper idle
            cb "...take your time Dr. [pname]..."
            jump postcube
        "But... this was my passion...":
            jump objectplan


label objectplan:
    $ pep_affpoint += 1
    $ pete_affpoint += 1
    $ steve_affpoint += 1
    $ obj_affpoint += 1
    mc "I worked so hard on this... all those years... those sleepless nights..."
    mc "But... you guys are right."
    mc "This isn't right."
    mc "But... Do you have a proposal to how we can fix it?"
    show pepper at jumpy
    cb "Petey, tell them the plan."
    stop music fadeout 0.5
    play music "audio/epic.mp3" fadein 0.5
    pipe "{i}*Epic music with array of pipe noises*{/i}"
    stop music fadeout 0.5
    mc "Wow... Petey, that was wonderful, so detailed... {w=0.5}If I didn't make you I would think you where a professional plan-maker of 12 years!"
    mc "I will do what I can to make sure this plan goes through."
    show pepper shy
    cb "Thank you [pname], thats all we can ask."
    mc "You should probably get back to your rooms now, before Dr. Dyson gets back..."
    steven "You're probably right... welp see you later [pname]."
    show petey at jumpy
    pipe "{i}*Thankful, pipe noise*{/i}"
    jump postcube

default spyroute = False
default helproute = False

label postcube:
    hide steven
    hide pepper
    hide petey
    scene bg cubes 
    with fade
    play music "audio/elevator.mp3"
    show bob salute at center with moveinright
    bob "There you are [pname]! Sorry, I got caught up in some emails! {w}Did you send the prototypes back to their rooms?"
    mc "Yes, I did, by the way..."
    menu:
        "The objects are planning on escaping.":
            $ bob_affpoint += 1
            $ spyroute = True
            jump spy1

        "Any updates from coroprate?":
            $ helproute = True
            jump help1


label spy1:
    show bob int at jumpy
    bob "{sc}THEY WHAT?{/sc}"
    bob "... Sorry, I meant, how do you know that? Did they tell you?"
    mc "Yes, they where talking about it during their break."
    bob angry "NO, No, no! That won't do! We have worked too hard on this!"
    bob "We have to stop this! What should we do?!"
    mc "Bob... If I knew I would have said something already."
    show bob int at jumpy
    bob "UHHHH QUICK, THINK OF A COMMON MOVIE TROPE!!"
    bob "{sc}UHH, UHHH, SUPER HEROS, UHH SPY'S UHHH, DOUBLE AGENT!!!{/sc}"
    bob agree "YES, YES, THAT'S PERFECT!! YOU CAN BE A DOUBLE AGENT! THEY CLEARLY TRUST YOU ENOUGH!!"
    mc "I.. don't know how I feel about betraying their trust like that.."
    bob eh "Oh come on, [pname]! You basically already have! I mean you already told me about the plan! You can't chicken out now!"
    bob agree "Come on, what do you say, ol' buddy?"
    
    menu:
        "...No.. I'm sorry Dr. Dyson, I can't! Its not right!":
            stop music
            if bob_affpoint >= 4:
                bob out "...Please leave..."
                mc "Bob, wait!"
                bob angry "[pname], please don't make this harder then it needs to be..."
                bob out "If it's any conselation... I really enjoyed working with you... but I need this, the world needs this."
            else:
                bob out "...Get. out."
                mc "What!? Why?!"
                show bob angry at shake
                bob "{sc}YOU ARE WILLING TO JUST THROW AWAY EVERYTHING \nTHAT WE WORKED SO HARD FOR? ALL FOR WHAT? FOR SOME \nSOULLESS, HEARTLESS OBJECTS?{/sc}"
                hide bob
                show bob angry at center
                bob "I thought you were smarter than this."

            jump firedend

        "Well... its to late to turn back now, lets do this.":
            show bob agree at jumpy
            bob "Wonderful! Lets get this started!"
            jump day3trans



label help1:
    $ obj_affpoint += 1
    bob eh "Nope! Just same old, same old! I'm dying in suspense! But Grant said they should send the people over in about 5 to 10 business days."
    mc "Oh! That's... faster than normal..."
    mc "{i}(That doesn't leave us with a lot of time...){/i}"
    bob agree "Well, if that's all, just finish your paperwork and clock out for the day!"
    mc "Alright! Sounds good!"
    jump day3trans

label firedend:
    "womp womp"
    return

default pep_seen3 = False
default ste_seen3 = False
default pete_seen3 = False

default firstchoice = False

label day3trans:
    scene bg cubes with fade
    $ renpy.notify('The next day...')
    mc "Well today's nothing too special, just normal check in's."
    mc "Who should I check on first?"
    jump day3

label day3:
    play music "audio/elevator.mp3"
    hide steven
    hide petey
    hide pepper
    scene bg cubes with fade
    mc "Who should I check on?"
    menu:
        "Pepper" if pep_seen3 == False:
            $ pep_seen3 = True
            if firstchoice == False:
                $ pep_affpoint +=1
                $ firstchoice = True
            else:
                pass
            jump pepper_d3
        "Steven" if ste_seen3 == False:
            $ ste_seen3 = True
            if firstchoice == False:
                $ steve_affpoint +=1
                $ firstchoice = True
            else:
                pass
            jump steven_d3
        "Petey" if pete_seen3 == False:
            $ pete_seen3 = True
            if firstchoice == False:
                $ pete_affpoint +=1
                $ firstchoice = True
            else:
                pass
            jump petey_d3
        "Bob" if pep_seen3 == True and ste_seen3 == True and pete_seen3 == True:
            jump bob_d3


label pepper_d3:
    mc "Hey Pepper! Are you in here?"
    show pepper shy at center with moveinleft
    cb idle "Hey [pname]! How have you been?"
    mc "Busy as usual, how about you have you gotten any work done?"
    show pepper at jumpy
    cb "Yep! I just finished re-orginizing EVERYTHING, on your computer! Tomorrow I will work on Bob's maybe we can get some more intel on how the grants going."
    if helproute == True:
        mc "You know Pepper... You could always just ask me."
    elif spyroute == True:
        mc "Oh! Well that's good! You know we already have a program that does that?"
        mc "{i}(I need to tell Bob to hide the grant files...){/i}"
    else:
        pass
    cb worried "Oh, right... I forgot about that... but this way is more fun!"
    menu:
        "What was it like being a object?":
            cb shy "...I don't know how to explain it really..."
            cb "It's dark but... like not in a literal sense, like...nothing. It feels like blissful nothing."
            show pepper idle
            mc "Huh... that's interesting."
        
        "Do you like being human?":
            $ pep_affpoint += 1
            cb shy "...It's not bad I guess... But there are a lot of responsibilities and weight on my shoulders,{w=0.5} and Dr. Dyson keeps sticking pins in my face, I don't understand how you live like this..."
            mc "...I'm sorry Pepper. I'll ask Dr. Dyson to stop sticking pins in your face."
            cb idle "Thanks [pname]."

    jump day3

default stevenplan = False

label steven_d3:
    scene bg kitchen with fade
    show steven angry at center with moveinright
    steven "STOP BEING MILK AND START BEING BUTTER!"
    mc "Heyyy, Steven... Uh, you doing alright?"
    show steven at jumpy
    steven "Oh hello [pname], THIS MILK WON'T TURN INTO BUTTER!! ITS BEEN IN THE MIXER FOR NINE MINUTES!"
    mc "Oh, I'm sorry?"
    steven idle "It's fine its not your fault... this time."
    if helproute == True:
        mc "Um, okay? I was just coming in to check if you needed a hand in the kitchen."
        if steve_affpoint >= 3:
            $ steve_affpoint += 1
            steven think "...Yes... Can you watch this milk until it turns into butter for me?"
            mc "Of course Steven."
            steven idle "...Thank you [pname]. you know, I don't normally want other peoples help with the food...{w=0.5} you just never know what they will do."
            mc "I'm happy you trust me, Steven."
        else:
            steven think "Yes... you could help clean the dishes."
            mc "Okay, I think I have some time for that!"
            steven idle "Thanks, I don't like other people messing with the food, {w=0.5}you never know what someones gonna do, ya' no?"
    elif spyroute == True:
        mc "I was just coming to see if you had any more information about the plan?"
        if steve_affpoint >= 2:
            $ stevenplan = True
            steven idle "Can't you see I'm busy? Ugh... nevermind, sorry, I do know a little more about the plan."
            steven think "We think the best time to leave would be after tomorrow, because that's when Pepper should be fully human, it should be easier that way."
            mc "Sounds like a smart plan, you know the saying! \"If you can't beat, em join em\"!"
            mc "{i}(I should keep that in mind...){/i}"
            steven idle "I have never heard that in my life."
        else:
            steven angry "Can't you see I'm busy? Ask someone else!"
    
    jump day3

label petey_d3:
    scene bg garage with fade
    show petey idle at center with moveinright
    mc "Hey Petey! Whatcha doing?"
    pipe "{i}*exited pipe noise*{/i}"
    if helproute == True:
        mc "Oooo, more poetry?"
        menu:
            "Well, don't keep me waiting!":
                $ pete_affpoint += 1
                if pete_affpoint >= 3:
                    play music pipe_voice
                    show petey at jumpy
                    pipe "{i}*romantic pipe noises*{/i}"
                    mc "Thank you Petey, was just beautiful, I can't describe how that makes me feel!"
                    stop music fadeout 0.5
                    jump day3
                else:
                    jump petey2
                
            "Still not a writer but, let's hear it!":
                jump petey2

    elif spyroute == True:
        mc "Oooo, more poetry? That's cool, do you have any more great ideas for the plan?"
        pipe "{i}*DISSAPOINTED PIPE NOISE*{/i}"
        play music pipe_voice
        pipe "{i}*ARRAY OF PIPE NOISES*{/i}"
        stop music fadeout 0.2
        mc "Oooo, that is really detailed! I'm so impressed we might have to change your job to a writer!"
        mc "{i}(That was incredibly important... I need to remember that.){/i}"

    else:
        pass
                    
    jump day3

label petey2:
    show petey at jumpy
    play music pipe_voice
    pipe "{i}*more glorious empowering petey poetry*{/i}"
    mc "Amazing as always Petey, I really feel bad for anyone who can't understand your wonderful poetry."
    stop music fadeout 0.5
    jump day3


label bob_d3:
    scene bg lab with fade
    show bob salute at center with moveinleft
    mc "Hey Bob! How's it hanging?"
    if helproute == True:
        bob agree "Hey [pname]! All smooth sailing from my end! How about you?"
        mc "Overall pretty good! Petey read me some nice poetry."
        if bob_affpoint >= 5:
            bob point "Oh! Thats... nice. {w}You know you should be careful getting too close with the prototypes, you never know what they might do."
            mc "Duly noted?"
            bob agree "Wonderful! Now did you get the chance to check in on anyone else?"
        else:
            bob salute "Oh! That's nice! Funny little object person he is. Did you get the chance to talk with the others?"
        
        mc "Yes, I did! They are all moving along smoothly, and besides Petey and the strange love of poetry, they all seem to be taking their jobs really well!"
        bob point "That's just wonderful! It's really important for them to be perfect for when corporate comes!"
        mc "Ah, yes, corporate... Can I ask you something?"
        bob agree "Of course! Ask away my friend!"
        if bob_affpoint >= 5:
            jump boblooove
        else:
            stop music fadeout 0.5
            mc "...Are you sure this is the right decision? If corporate does sign off on this, what's gonna happen to the prototypes?"
            bob point "... Of course this is the right decision! We will help {i}MILLIONS{/i}! And as for your afterwards question... {w}you don't need to worry about that! I've got it all figured out!"
            bob out "Now, you seem a little antsy. How about you go home and get some rest?"
            mc "..."

    elif spyroute == True:
        bob agree "Could be better... You know, with the whole 'objects revolting' thing, but other than that, it's been smooth sailing!"
        bob salute "By the way... do you have any insight on the object's plans?"
        menu:
            "Yes, they are planning on leaving sometime after tomorrow, that way, Pepper will be fully transformed." if stevenplan == True:
                bob int "Let me guess, Steven told you this? I have to hand it to the guy; he is pretty smart, not smart enough, though!"
            "Yes, before you leave today make sure change the passcode on your computer, Pepper said she was going to check it for more information.":
                bob agree "Oh, Pepper, she's getting smarter by the day. Not smart enough, though!"
            "Yes, Petey said ████████.":
                bob int "Wow, that was the most detailed, wonderful plan I have ever heard. {w}You know, maybe if he wasn't a {i}TRAITOR{/i}, then I would have let him work here full-time. Without pay, obviously."
        show bob agree at jumpy
        bob "Thanks for the intel, my loyal companion! Anything else you wanted to ask?"
        mc "Yes actually."
        jump boblooove
    
    jump endofdemo

label boblooove:
    mc "Are you free tonight?"
    show bob shock at jumpy
    bob "{sc}FREE? LIKE FOR A DATE?{/sc}"
    menu:
        "I just wanted to, you know, hang out? Maybe go by that karaoke pho place you always talk about.":
            $ bob_affpoint += 1
            show bob at jumpy
            bob "[pname]! I would be honored! Oh goodness! I've never been on a date before! What should I do? Should I bring flowers? Chocolate? {sc}AN ARRAY OF LOVE THEMED SOCKS?{/sc}"
            show bob salute
            mc "Just bring yourself Bob- see you after work~!"
        "Oh no, I meant just as like friends, and work-partners! You know... to like talk more about the grant?":
            show bob int at shake
            bob "{sc}OH, OF COURSE!!! I'M SO SO SO SO SO SO SO SORRY!!!!\n I DON'T KNOW WHY I SAID THAT!!! UHHHHH OF COURSE, \nYES, UHHH SEE YOU AFTER WORK!!!{/sc}"
            hide bob with moveoutleft
            mc "I didn't even tell him where to meet..."
    
    jump endofdemo


label endofdemo:
    scene black with fade
    "End of demo. Thank you for playing :)"