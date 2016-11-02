mitm-perk-quiz
==============

>   **Perk Pop Quiz**

>   Well its one of those apps (available for Android/ iOS) which award you with
>   special bonuses like Gift Cards, points redeeming to Cash!, or even buy few
>   stuff with the points you have collected by playing quiz, answering to the
>   questions on any topic you like. As simple as that.

 

So? What’s mitm-perk-quiz?
--------------------------

Well straight and simple, here we are going to learn, how to be a serious smart
pant, a great genius, a walking Wikipedia, a human version of IBM’s Watson, who
could just answer any any general/technical question, like how Google would come
up with the results!. So, we learn here now, and then, answer the questions that
are asked to us in this [Perk Pop Quiz](https://play.google.com/store/apps/details?id=com.jutera.perkpopquiz.aphone&hl=en) app without having
ever gone wrong, and finally to earn points (the cash redeeming you know).

Okay! that’s enough now.. I was just kidding :skull: I ain’t got any super powers to
help you with or something I can make you cast a spell to be that “Intelligent”
:wink:. Yes but that’s true, that you would answer any question asked to you
**inside the app**, so in end you can collect the points smoothly without having
do no mistakes.

Ahem!, pretty straight to say, **just get to know the right answer, and select
it from the options given to you for that question of that particular session.**

**So how are we going to do that?**. Exactly, that is what we are going to know
how, check it out below..

 

Scenario...
-----------

Okay!, I ain’t gonna narrate any story story here :thought_balloon:. Its just how it all
started for this. I were doing some web debugging (sniffing [HTTP requests](http://rve.org.uk/dumprequest)) on the phone from my PC (performing a *mitm, [Man In The Middle attack](https://en.wikipedia.org/wiki/Man-in-the-middle_attack)*, not with any “attack” intentions really), on few of
the android apps I installed lately, just to check how and **why** often do they
communicate with network in background (of course I am damn concerned with my
phones soon battery drain issue too :disappointed: ..)

It was time for this *Perk Pop Quiz* app. Gosh!, it had too many *HTTP requests*
running in background. I played a solo quiz on a random quiz category, and
noticed, that in one of the [HTTP GET](http://www.w3schools.com/TAGS/ref_httpmethods.asp) requests the app
made (prior to the moment I started the game), it contained all the Questions,
Options, **Answers,** in [JSON](http://www.w3schools.com/js/js_json_intro.asp) format. So now I got a bit mouth watered.
I had almost thought of getting a power bank after having it known.

But damn!, there was a critical issue to have them utilized, the answers, were,
ENCRYPTED!. And those can only be decrypted by the app installed by the user.
Spent 4 days trying to analyze how is the app decrypting the answers.

Reverse Engineered the *apk* file using [Apktool](https://ibotpeaches.github.io/Apktool/).
Deep shoveled the source code, apprehended the
[Activity](https://developer.android.com/reference/android/app/Activity.html) where the quiz is performed, and finally
found the exact piece of code which decrypts the answers. And after that, I got
a complete idea, and then I could wind up the stuff like below, when the session
of quiz is just about to begin (after the ads finish displaying, and the game
ticks to start off) these things happen..

 

### Server Responsibility:

> Host = api-tv.perk.com

> URL = /v5/ppq/questions.json


1.  *Correct* answer is encrypted (actually hashed) using [SHA-1](https://en.wikipedia.org/wiki/SHA-1)
    algorithm.

2.  The **Correct** answer of each question is **digested (as hexadecimal)** by
    adding the [access\_token](https://en.wikipedia.org/wiki/Access_token) (*authentication token*
    otherwise) that was provided for the user with the right option **id** of
    that question.

3.  Server sends (on a user’s single HTTP GET request) the *questions, options*
    in normal text, with *correct* answer encrypted from the above process
    mentioned in step 2.

>   A raw idea, is something like,

>   **curl --get
>   https://api-tv.perk.com/v5/ppq/questions.json?access\_token={***a 40
>   character value***}&category\_id={** *type of quiz represented numerically*
>   }&limit= { *number of questions* }

 

### Client (User/App) Responsibility:

1.  Receive the JSON data from the server by providing the **access\_token** to
    it, that was registered and stored for that particular user.

>   For instance, the Response received is,

>   `{"status":"success","message":null,"data":{"batch_id":"df9ec8c7c5599bdab553c24b1a2071bbcbbd738b8227549e20d9f40e3649ff20","questions":[`

>   `{"id":"226702","question_text":"What is a common name for the Aurora
>   Borealis?","is_boolean":false,"img":null,"answers":[{"id":"905977","answer_text":"Gegenschein"},{"id":"905978","answer_text":"Plage"},{"id":"905975","answer_text":"Northern
>   Lights"},{"id":"905976","answer_text":"Zodiacal
>   light"}],`**"correct"**`:`*"62a541f079038ed11c83b4615c926828a42d67a3"*`},`

>   `{"id":"226700","question_text":"What is usually seen near the poles in the
>   night sky that can be red, yellow or
>   green?","is_boolean":false,"img":null,"answers":[{"id":"905969","answer_text":"Gegenschein"},{"id":"905968","answer_text":"Zodiacal
>   light"},{"id":"905967","answer_text":"Aurora"},{"id":"905970","answer_text":"Plage"}],`**"correct"**`:`*"a1359ec9c77390088796895854a7d2d5b803eedc"*`},`

>   `{"id":"226659","question_text":"When the Earth is directly between the Sun
>   and the Moon, it is called a\/an _________
>   eclipse.","is_boolean":false,"img":null,"answers":[{"id":"905806","answer_text":"Transit"},{"id":"905803","answer_text":"Lunar"},{"id":"905804","answer_text":"Solar"},{"id":"905805","answer_text":"Inferior
>   conjunction"}],`**"correct"**`:`*"0d5f38b422b2650b74ab925c86eb7749b6bc600f"*`},`

>   `{"id":"226751","question_text":"The mantle makes up about ____% of Earth's
>   volume.","is_boolean":false,"img":null,"answers":[{"id":"906171","answer_text":"84"},{"id":"906172","answer_text":"97"},{"id":"906173","answer_text":"12"},{"id":"906174","answer_text":"20"}],`**"correct"**`:`*"cb5a1e645f1ab427ac4b1654db91d0d37f5d0098"*`},`

>   `{"id":"226604","question_text":"What mineral has perfect cleavage in six
>   directions?","is_boolean":false,"img":null,"answers":[{"id":"905586","answer_text":"Fluorite"},{"id":"905585","answer_text":"Sodalite"},{"id":"905583","answer_text":"Sphalerite"},{"id":"905584","answer_text":"Diamond"}],`**"correct"**`:`*"44829a277381a356295ebllb1c1ea4d827e31d1a"*`},`

>   `{"id":"226580","question_text":"What would you call the solid material that
>   is carried within the
>   stream?","is_boolean":false,"img":null,"answers":[{"id":"905487","answer_text":"Suspended
>   load"},{"id":"905490","answer_text":"Bed
>   load"},{"id":"905488","answer_text":"Dissolved
>   load"},{"id":"905489","answer_text":"Floating
>   load"}],`**"correct"**`:`*"ece190cfc99bf5800a5a8d9b93999dca89dd828f"*`}],`

>   `"current_streak":0,"longest_streak":1,"answer_responses":{"correct":["You're
>   on a roll!","Smart cookie!","NAILED IT!","Aww
>   YEAH!",":D","BOOM!","BINGO!!!","You're on FIRE!","BINGO!!","Correct!","Good
>   one!","YES!"],"incorrect":["Try again!","Try another
>   one.",":(","Dang!","Nope :(","Ouch"]}}}`

>    

>   You can notice the correct answer for every question is encrypted.

 

1.  Parse the data and display it graphically in structured way to user.

2.  When the user selects the option, verify if it is correct in this way,

    1.  Add (concatenate) the the **access\_token** and the option’s **id**
        (JSON attribute) of that question.

    2.  Calculate the **SHA-1** of the sum from above.

    3.  Check each of the resultant hash of the options **id’s** are equal to
        the **Correct** attribute of the question. The one which equals is the
        **right option!**

>   A snippet for it from the script goes like,

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ python
def verifyRightAnswer(answer_id, correct_sha, authentication_token):
        h = HashUtil.sha1Hash
        right_answer_id = str(answer_id)
        auth_token = str(authentication_token)
        auth_correction = auth_token + right_answer_id
        result = h(auth_correction)
        #print(result)
        return (result == correct_sha)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Whoaaa!! All this happens is in matter of a second, and **you have only the next
very 5 seconds** already to answer up for the next question, by then you’ve got
to,

1.  Intercept the the HTTP requests between your phone (client) and the perk
    servers.

2.  Process the JSON data and decrypt the answers and view them.

3.  Search for question and its answer that is randomly asked from the list of
    questions the server sends.

Huff!! **hell go with the perk!** You must be saying this to me :trollface:

Do you think we should give up here?.. Nope I don’t think so :angel:, as long as we
can automate few things.

But before we proceed further, I highly recommend you have the prerequisites
that you need in order to achieve this hack successfully.

 

Things Required
---------------

-   Windows (7\~10) running **PC**

    >   To perform the hack on

-   **Android** Phone (of any API version, supporting Proxy on Wi-Fi)

    >   Play the quiz game on to

-   Telerik **Fiddler** Web Debugger
    [(Download)](https://www.telerik.com/download/fiddler)

    >   To sniff the requests between phone and perk servers, and activate the
    >   python script

-   Fiddler **SyntaxView** addon
    [(Download)](http://fiddler2.com/r/?SYNTAXVIEWINSTALL)

    >   This is required to customize the *FiddlerScript Rules file* easily.

-   **Python** 3.5/Latest release [(Download)](https://www.python.org/downloads/)

    >   Compile and run the python script that can parse the response, decrypt
    >   the answers, and display the results in organized way, that was sniffed
    >   by Fiddler.

-   **Per Pop Quiz** [(Install)](https://play.google.com/store/apps/details?id=com.jutera.perkpopquiz.aphone&hl=en)

    >   Bah! app of course, Watson you :ghost:

-   PC and Phone connected to **same network**.

    >   PC acts as a proxy to the phone, so that the network traffic over the
    >   phone can be captured as it passes through, using *Fiddler.*

-   And Authentication Token (**access\_token**) (no worries, we’ll find it once
    things are set up)

    >   This is required to decrypt the answers, the **most important**
    >   component for this whole circus to happen

 

So what are we waiting for?, lets get started right away!

 

STEP 1 (setting up the things...)
---------------------------------

>   Make sure your PC and your android phone is connected to the same network.
>   That would simply mean, connecting to a same Wi-Fi.

### Setting up the fiddler, so that we can intercept the requests of the Perk Pop Quiz on your phone.

-   Install the Fiddler, run it, go to `Tools ` in the Menu bar, click on
    `Telerik Fiddler Options...`

    -   Select `Connections` Tab,

        -   Set the value of `Fiddler listens on port:`to **8888**

        -   Check the `Monitor all connections` option

        -   Check the `Allow remote computers to connect` option

        -   Check the `Reuse client connections` option

        -   Check the `Reuse server connections` option

    -   Select `HTTPS ` Tab,

        -   Check the `Capture HTTPS connects` option

        -   Check the `Decrypt HTTPS traffic` option

-   Restart the Fiddler.

-   Now navigate to `Control Panel > Network and Internet > Network and Sharing
    Center > Change adapter settings.` Right click on the Wi-Fi adapter your
    internet works on, select `Status,`click on `Details...`, and note down the
    `Autoconfiguration IPv4 address.`

-   In your android phone, Go to Wi-Fi settings, long press the network you are
    connected to.

    -   Click on `Modify network config,` check on `Show advanced
        options,`you’ll be provided with more options to configure.

    -   Select `Manual` for under *Proxy* spinner.

    -   Now type the `Autoconfiguration IPv4 address` of the PC you noted down,
        in the `Proxy hostname`textview, and there below, enter the number
        `8888` in the `Proxy port` textview.

-   Go to your phones default web browser, and type `http://ipv4.fiddler:8888/`
    in the search bar. Download the certificate and install it. This trusted
    certificate is required to help the network of your android phone to be
    monitored by fiddler.

>   I haven’t tried up with iPhone version. Well things should remain same as
>   long as iOS permits to install the certificates, and run proxy over Wi-Fi.

-   Run the fiddler now.

If everything was followed up correctly so far, you should see all the web
sessions (the requests and their responses) captured inside fiddler, made by all
your installed android apps (and of your systems too).

 

STEP 2 (getting your Perk identity)
-----------------------------------

### Finding the authentication token (**access\_token**)

As the requests are made by the phone, you can see them getting added up in the
session list of the Fiddler one after the other. Its time now, we capture that
request which holds the *access\_token* that designates our identity in the app.

-   Open the *Perk Pop Quiz* app in your phone,. You may notice continuous
    requests that are made by the app are being updated on Fiddler in your PC.
    For now, you don’t have to investigate anything. Let them get captured.

-   Play any quiz of your choice. Well if you did any mistakes in this quiz, it
    might be the last time ha ha :broken_heart:. Well after you finish playing, close the
    app.

-   Head back to Fiddler, press `Ctrl+F` or you can go to `Edit > Find
    Sessions...` from the menu strip.

-   Type `https://api-tv.perk.com/v6/ppq/tags?access_token=`

    -   You can see the session being highlighted. That’s it, there goes your
        access\_token !!. Just look at your left in `Inpector` section, under
        `Header` tab.

    You will have it in this way,

    >   GET
    >   /v6/ppq/tags?**access\_token=c6ffaXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXfe4d1**
    >   HTTP/1.1

    >   *(the original characters are replaced with...XXXXX... in above to hide
    >   my access\_token, no worries)*

-   Note down the access\_token (that 40 character value you just found). I
    believe this might vary if you reinstall the app, or if you installed the
    app in other phone, with your identity.

The above two steps are not required to perform repeatedly, on each hack. As
long as you are not performing the this hack on different Wi-Fi network.

 

STEP 3 (sharpening up the tools)
--------------------------------

>   Make sure you’ve installed SyntaxView addon for fiddler. Not compulsory
>   though.

This was the most difficult part for me to step up. But thankfully succeeded in
making it out. I wouldn’t even write this all if I failed. Everything was done,
I got even the script written to decrypt, and display the results. So when I
tried playing the quiz, with the things I had now, the moment I begun with the
quiz, captured the response (one which server sends from the URL
*/v5/ppq/questions.json*), and immediately fed the response data to the script
from the notepad, and got the results too. But guess what? I could just still
answer one bloody question correctly :D.

Because it took me 13 seconds to do this after the quiz started. And another 5-6
seconds to search for question and its answer that is randomly asked from the
list server sends (which I was talking about initially). And of all, the whole
quiz session is just of 30-45 seconds hardly. I was doom struck with this. Can’t
just have a partner to help me find and read out the answers. It sounds so
ugly-hack! Yew :X.

Then I taught of integrating any of open source available sniffers like
[Pyshark](https://pypi.python.org/pypi/pyshark/0.1) or [Scapy](http://www.secdev.org/projects/scapy/) within my script. So
that the things I did by feeding the response data to script manually, should
now be done automatically in background, by programming in such a way to sniff
just on the host *api-tv.perk.com*, and any request made to this host matches to
the request which we need, its response should be fed to the scripts main module
which process’s and display the results. Which would remove that 13-15 seconds
lag to answer.

Googled a lot to get it done. But, Windows didn’t let me to integrate it in some
or the other way. The dependencies, different build tools required, the sniffers
failed to compile, version mismatch issues with the dependencies, huff!, I
reached the ends but felt to just give up. It was like all the time digging in,
went in misery so far.

But a few days later, I accidentally came on this, `Customize Rules..`option
under `Rules` of the menu, in Fiddler. Damn good it was to know there’s such
option too. Got hands little dirty in it, and Tada!, found the solution. The
steps to follow are below..

### Make the script to self trigger, the moment when quiz starts

-   Create a text file in your preferred directory (not under *C:\\*\* ), for
    instance, in my case *“H:\\\#alshell\\perk\_data.txt”.*

-   Click on `Rules` option in the Menu, Select `Customize Rules...` under it.

-   You can see the *FiddlerScript Rules file* opened in Fiddler Script Editor.

-   Look out for the function, `static function OnDone(oSession: Session),`which
    is actually commented by default.

-   Uncomment that function, and place the below code inside it,.

```c#
    if(oSession.fullUrl.Contains("https://api-tv.perk.com/v5/ppq/questions.json?"))
    {
      String filePerk = "H:\\#alshell\\perk_data.txt";
      System.IO.File.WriteAllText(filePerk, oSession.GetResponseBodyAsString());
      System.Diagnostics.Process.Start("python", filePerk);
    }
```
 

That is it! Done. You are just a step away now.

 

FINAL STEP
----------

### Set the access\_token in the script.

-   Open the **MainMod.py**

-   Replace the value of class attribute `def_auth_token` with the
    *access\_token* you noted down in **STEP 2**

-   Cheers!. You are about to be that smart pant.

 

Ultimately...
-------------

-   Make yourself comfortable.

-   Get ready.

-   Open the the Perk Pop Quiz in your phone.

-   Select **any** quiz category to play.

-   Watch the screen of your PC, serving you with answers, the moment quiz
    begins.

-   Seamlessly tap the answers.

-   Buy a power bank for me soon ha ha :joy:

 

Hope you felt cozy with the steps. I’d be grateful if I were too let know
with different approach than this.

Do fork me. Have a nice perk time :boom:

 

>   Copyright (c) 2016 alshell7.

>   Permission is hereby granted, free of charge, to any person obtaining

>   a copy of this software and associated documentation files (the "Software"),

>   to deal in the Software without restriction, including without limitation

>   the rights to use, copy, modify, merge, publish, distribute, sub license,

>   and/or sell copies of the Software, and to permit persons to whom the
>   Software

>   is furnished to do so, subject to the following conditions:

>   The above copyright notice and this permission notice shall be included in

>   all copies or substantial portions of the Software.

>   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,

>   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES

>   OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT.

>   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY

>   CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,

>   TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE

>   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
