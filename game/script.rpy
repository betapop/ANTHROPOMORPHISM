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

define pipe = Character("Petey Pipe", what_slow_cps=50, image="petey", callback=pipe_sound)
define steven = Character("Steven Spatula", image="steven", what_slow_cps=50, callback=mid_beep)
define cb = Character("Pepper Pinboard", what_slow_cps=50, image="pepper", callback=high_beep)
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
    scene bg cubes
    show bob wave at center with moveinleft 
    show bob salute
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
    # scene bg - lab
    scene black with fade
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
            show pepper shy with move:
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
            show steven idle at jumpy
            steven "STOP STARING AND START EXPLAINING!"
            bob "IN A MINUTE STEVEN I AM TRYING TO HAVE A CIVIL CONVERSATION!!"
            bob "{sc}NOT THAT YOU WOULD KNOW WHAT THATS LIKE!!{/sc}"
            bob "Ahem, sorry about that! I promise he is an excellent chef, just as long as you don't go into the kitchen!"
            $ ste_seen = True
            jump creations

        "Petey" if pete_seen == False:
            show petey noeyes at center with moveinright
            bob "In this corner we have Petey Pipe! The amazing... actually kind of creepy..."
            show bob eh at left with moveinleft
            bob "You know what? Gimme one second to fix this..."
            show bob salute at center with move
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
    steven "... Sounds fishy to me..."
    bob point "One at a time please, one at a time! But to answer Pepper's questions."
    bob "Humanity refers to all humans, and humanity is in dire need of one thing...{w=0.5} Workers!"
    cb idle "So... where do we come in?"
    steven "Pepper... Im pretty sure he's saying {i}we{/i} are the workers..."
    bob salute "Great listening ears, Steven! That is absolutely correct! You guys will fill the roles that humans have outgrown!"
    show steven idle at shake
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
            show bob eh
            cb "Could be worse I suppose... thank you."
            pipe "{i}*PIPE NOISE!*{/i}"
            steven "Im not buying it..."

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
    # scene change - kitchen
    scene black with fade

    show steven idle at center with moveinright
    "{i}[[[pname!u] WALKS INTO KITCHEN TO SEE A VERY ANGRY STEVEN YELLING AT WHAT SEEMS TO BE A PLATE WITH A WHOLE RAW EGG ON A PAN]{/i}"
    steven "{sc}ITS BLOODY RAW!{/sc}"
    steven "Oh, hello [pname]. I was just cooking breakfast,{w=0.5} its the most important meal of the day you know."
    steven "Actually it's not, I don't know why I said that, {w}that was a myth food companies created in the 1800s and 1900s to sell more cereal and bacon."
    mc "I'm surprised you know that considering you were a spatula 2 days ago."
    mc "Also you know you need to crack the egg... {w=0.3}right?"
    if steve_affpoint >= 1:
        show steven at jumpy
        steven "...Oh... that... actually makes a lot of sense...{w} uh.. thank you..."
    else:
        steven "...Yes... I knew that. I am a chef after all! How dare you assume my intelligence!"

    steven "ANYWAY, what made you wanna come into the kitchen, I presume, it was to see me, but there has to be another reason."
    mc "You would be correct! I came here to check on you and tell you to go to the cubicles to socialize,{w} as I tell Bob, you can't be a shut in all your life."
    steven "I don't know how you work with that guy, he's so... I don't know."
    steven "He looks like he'd sell out his family for some turkish delight and have no regrets, you know what I mean?"
    mc "No? Not really, sorry."
    steven "Never mind, lets go."
    $ steve_affpoint += 1