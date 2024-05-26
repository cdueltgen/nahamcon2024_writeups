# Base3200
Category: Scripting<br>
Difficulty: Easy

The only instruction for this challenge says: 

> You know what to do.

The challenge contained a file called `theflag.xz`

The first thing I did was the first thing you really ought to do with any 
file after decompressing it, which is to run `file` on it. This said it 
was an plain old ASCII file, so nothing too terribly interesting there. 
Then I ran `head` on it to see what I was dealing with. LOL. That was a 
bit of a mistake since it just starting spewing a wall of text into my 
terminal and wasn't super interested in being interrupted. A little more 
digging using `wc` showed me I was dealing with a file that had only one 
line, but it was 79918301(!) characters long. That explains that.

Since I did not, in fact, know what to do, some searching was in order. 
A few searches later, with keywords like "base3200" and "CTF" led me to 
something that pointed out that 3200 is 64 * 50. This made me think that 
it was likely the flag base64 encoded 50 times. Well, that's easy enough 
to sort out.

Wrote up a quick little Python script to decode, and whaddya know, a flag!

The Python file is included here, if you're curious, but I'm not putting 
it straight in the readme in case you stumble across it and want to try 
to write it yourself.


