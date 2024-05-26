# Seventy Eight
Category: Misc<br>
Difficulty: Medium

The challenge instructions said:
> aaaaaaaaababy. Welcome to Seventy Eight. It's a great language. We promise. Just print out i want flag please?

Okay. So that's a bit weird, but it's clearly info we need for the challenge and not a typo or anything, so let's come
back to it when we have more info.

Clicking the "Start" button in the upper corner of the challenge starts a container and gives you an address & port to
open in your browser to complete the challenge.

### Recon
The first thing we see when we open the site is something that says:
> seventyeight With the power of seven and eight, we can...print ascii... probably

Then there's a section that starts with a header called "AAAAAA FACTS."<br>
There's that repeating pattern of A's again. I'm starting to suspect it means something.

Under that there are three lines of...not exactly instructions, but I bet they're important.
> seventy eight is based on the numbers 7 and 8.<br>
> seventy eight is divisible by two, but not by seventy seven.<br>
> f terminates the program, but only if the next instruction is you.

My inner 12-year-old snickered at the f you instruction, not gonna lie.

Lastly, at the bottom is a text submission box with the placeholder text:
> aaaaaaaaa code go here babyrb. To prove you are worthy, input code that prints out 'i want flag please'. aaaaaaaaaa!

More repeating A's and I'm once again guessing that "babyrb" is also not a typo.

### Research
I flailed around here a bit trying to get the text box to return _anything_ other than an incredibly unhelpful error and 
got absolutely nowhere. So off to the googles we go.

I was having a fairly unproductive time trying the various combinations of "AAAAAA", "Seventy Eight", "78", and "programming language"
until I stumbled across a video with John Hammond talking about "esoteric programming languages". Part of why I love doing
CTFs is that they're helping me fill in some cybersecurity vocabulary as well as helping me develop my problem-solving
intuition in this area, so my ears definitely perked up at that particular turn of phrase.

Returning to the googles and adding "esoteric programming language" to my queries got me on the right track and led to
what appears to be the only existing [GitHub repo for the language "78"](https://github.com/oatmealine/78). Feel free to
take it in in all its glory. Honestly, the syntax made my head hurt.

I tried running the examples in the readme, most if not all of which errored out on me, but at least gave me the helpful
clue that I needed to end my f-you with an exclamation point. The inner 12-y-o is still enjoying this bit. I also tried
assembling the bits of nonsense in the placeholder text and it turns out that "aaaaaaaaa" combined with "babyrb" followed
on the next line with a terminating "fuck!" (snicker) still results in an error, but at the end of the error it says:
>stdout: b'6'

Progress!

I dug a little further into the repo and found the Examples directory. Grabbing [helloworld.78](https://github.com/oatmealine/78/blob/master/examples/helloworld.78)
and pasting it into our text box, again with the trailing !, and would you look at that!
> stdout: b'hello world!'

Sure looks like one character per line is being generated from the As and Bs that end in "yrb". So the last bit of research is to see if we
can make any sense at all of the actual interpreter code. You don't have to be fluent in JavaScript to pull the relevant bits 
that we're going to need to solve this out of the code

The crucial bits of info I could glean from the code was that in the interpreter, an 'a' results in a value being incremented
by 7, and a 'b' decrements that same counter by 8. Once the string of As and Bs is terminated with a "y" the resulting number
is fed to `process.stdout.write(String.fromCharCode(mainval))`, or, in English (more-or-less) the decimal is converted to its
ASCII value and printed out.

### Solve it!
Given that the math here is pretty simple, you could brute force this with an ASCII chart, a pencil, and a piece of paper,
but we invinted computers for a reason, and if your computer's resources aren't being used to do something this ridiculous,
you probably have, like, a real job or something.

First I built a little POC function to make sure I understood the interpreter code. Since we have a bunch of 
known letters and their encodings from the Examples, I grabbed the first letter from helloworld.78 and went to work.
Here's the resulting (Python) function.
```
def decode78(instring):
    strval = 0
    for c in instring:
        if c == "a":
            strval+=7
        elif c == "b":
            strval-=8
        else:
            break
    print(chr(strval))
    
decode78("aaaaaaaaaaaaaaabayrb")
```
Okay, so that bit works to turn our strings of As and Bs into the right ASCII number, now we need to turn that around
find a way to encode a single character into 78.

Turns out decode was the easier part, for me anyway. I had a handful of fits and starts working on the encoding, including
one hilarious moment where I put a subtract by 7 in the wrong place and induced a subtraction to negative infinity that
crashed the VM I was working in. Whoops.

Shortly after recovering the VM, I had two simultaneous thoughts:
1. ChatGPT could probably have written this code for me by now
2. integer mod and div are going to be way more useful than trying to get looping subtraction right

One way to think about the logic of how to generate the encoding is that an 'a' by itself is worth 7, but a 'ba' combo is
worth -1. So unless the number is actually divisible by 7 (i.e. mod 0), in order to get the right combo of letters, we
have to overshoot with multiples of 7 (a) and then subtract back down one at a time (ba) to get to our target number.
I'm sure there's even more clever ways to do this that would eliminate the if, but this worked a lot better than the 
looping subtraction to minus infinity, so I was satisfied with this solution. In Python:
```
def encodechar(c):
    dec = ord(c)
    if (dec % 7) == 0:
        aa = "a" * (dec // 7)
        ba = ""
    else:
        aa = "a" * ((dec // 7) + 1) # overshoot
        ba = "ba" * (7-(dec % 7)) # invert the remainder and subtract
    print(aa + ba + "yrb")
```
The "yrb" isn't necessary before the terminating line, but it also doesn't appear to matter if it is there, so I didn't
complicate it any further by trying to take it out.

If you feed the line from the placeholder text (remember that from our recon?) into our encoder function character by 
character, and then drop the output into our text box and submit (don't forget the terminating 'fuck!'), we get the flag!
```
for c in "i want flag please":
    encodechar(c)
```
>flag{7deea6641b672696de44e60611a8a429}
