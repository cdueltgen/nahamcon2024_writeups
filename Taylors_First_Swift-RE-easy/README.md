# Taylor's First Swift
Category: Reverse Engineering<br>
Difficulty: Easy

Challenge:
> OMG did you hear that they named a programming language after Taylor Swift?
> 
Contents: One binary file called `taylor`

### Recon
First thing's first, I suppose.
```
$ file taylor
taylor: Mach-O 64-bit executable arm64

$ strings -n 6 taylor
sorry bestie but thats not it...
omg yayayay!
*sad violin*
pwease twell me the fwag uwu >> 
Division results in an overflow in remainder operation
Swift/arm64e-apple-macos.swiftinterface
Fatal error
Division by zero in remainder operation
```
Not a lot to go on there. I suppose it was too much to ask that it just spit the flag out with `strings` but it was
worth a shot.

### Research
Searched for "Mach-O" and found it is a MacOs and IOs native binary format. If I actually wanted to try to understand
what was happening in the binary, this [Wikipedia article](https://en.wikipedia.org/wiki/Mach-O) would probably be a
decent place to start

Honestly, there's not much more in the way of research I could have done here, so let's just move on to how I tried
to solve it.

### Solve it!
Reverse Engineering is one of the categories of CTFs I feel the least confident about, and that's saying something.
It makes me feel like this:

![I have no idea what I'm doing](https://i.kym-cdn.com/photos/images/newsfeed/000/234/765/b7e.jpg)

I'm cool with that, though. I'm here to learn, and I just have to remember that I know stuff and can figure stuff out.

I did, however, along with my awesome teammates, recently finish in second place in the Wicked6 cyber battles
tournament, and the prize was a one-year Binary Ninja license, so I'm leaning in on trying to get better at Reverse
Engineering. I'm still learning how to use it and understand what it's showing me, but it definitely gives a leg up
in challenges like this. Any other binary analysis tool would probably do the trick here, I'm just focusing on
learning this one.

The first tutorial in Binary Ninja tells you to check the "Triage Summary" first, so that's what I did. It showed a lot
more things that looked like strings than `strings` did, but still no obvious flags.

There were a bunch of things in the strings section that looked like they could be function names of a sort.
The most promising of these was: `_$s6taylor9flagCheckySbSSF`

So I went hunting for it in the main BN window and found a huge function that's doing all sorts of things I can't yet
understand, but this was the relevant bit:

```commandline
...
100001468      x0_8 = _$ss27_allocateUninitializedArrayySayxG_BptBwlF(9, _$ss5UInt8VN);
100001478      int32_t var_a0 = 0x73;
10000147c      __builtin_strncpy(x1_6, "swifties!", 9);
100001494      int32_t var_9c = 0x66;
1000014bc      _$ss27_finalizeUninitializedArrayySayxGABnlF();
1000014cc      int64_t x0_10;
1000014cc      int64_t x1_9;
1000014cc      x0_10 = _$s6taylor10xorEncryptySSSays5UInt8VG_AEtF(x0_7, x0_8);
1000014e0      _swift_bridgeObjectRelease(x0_8);
1000014e8      _swift_bridgeObjectRelease(x0_7);
1000014f4      int64_t var_58_1 = x0_10;
1000014fc      int64_t var_50_1 = x1_9;
100001500      int64_t x0_14;
100001500      int64_t x1_11;
100001500      x0_14 = _$sSS4utf8SS8UTF8ViewVvg();
10000151c      int64_t var_68 = x0_14;
100001520      int64_t var_60 = x1_11;
100001524      int64_t x0_16 = _$sSaySayxGqd__c7ElementQyd__RszSTRd__lufC(&var_68, _$ss5UInt8VN, _$sSS8UTF8ViewVN, x0_1);
100001538      int64_t x0_17;
100001538      int64_t x1_14;
100001538      x0_17 = _$ss27_allocateUninitializedArrayySayxG_BptBwlF(0x34, _$ss5UInt8VN);
100001550      __builtin_strncpy(x1_14, "FRsIAQ8PVBUVEREIVERbBkURFkUIBxVQVkAYFxJfV0FYVkIVQgo=", 0x34);
10000166c      _$ss27_finalizeUninitializedArrayySayxGABnlF();
100001688      int32_t x0_19 = _$sSasSQRzlE2eeoiySbSayxG_ABtFZ(x0_16);
100001698      _swift_bridgeObjectRelease(x0_17);
...
```
The two lines that start with `__builtin_strncpy(...)` are exactly what we're looking for. One is just a string,
so we'll stash that for later, and the other is a base64 encoded string. Which, if you've been doing CTFs for any
amount of time, you know might be hiding something useful.

So I did what any good CTFer would do and ran over to CyberChef, thinking I had found the answer. Well, when you
base64 decode that string, you get...garbage. Or at least something not ASCII. No flag yet. Rats.

Let's take another look at the code up there. See the line that contains `_$s6taylor10xorEncryptySSSays5UInt8VG_AEtF`?
If you look a little closer, it says "xorEncrypt" in it. So I figured what the heck. Went back to CyberChef, added an
XOR to my base64 decode, set it to UTF8 with the key set to the only other string I'd found anywhere which was
'swifties!' and would you look at that! A flag! flag{f1f4bfa202c60e2aaa9339de61513141}

Make no mistake, I still feel like that dog most of the time when I'm looking at RE challenges, but I'm trying not
to let that bother me.