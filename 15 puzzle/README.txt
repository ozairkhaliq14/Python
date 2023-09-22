I used python 3.11.2 64-bit on windows for this project
IDE: VS Code

Used ChatGPT to debug and improve code.

Some of the prompts I typed in were:

I had two different versions of python downloaded, the actual python from pythons website and the microsoft store one. 
That caused a lot of confusion and I gave up trying to make psutil work.
When I had issues with psutil not working, I tried using import resource, then found out that that only works on linux.
So ChatGPT helped me install psutil through the command prompt and got it working on VS Code.
So then the code I wrote for the resource module needed to be converted back to a windows compatible version for psutil.
I just wrote "convert "..." to work on windows using import psutil"
ChatGPT was really helpful when calculating the memory.

Whenever I got any erros on gradescope I would just copy paste that part of the code and say "autograder gives error "..." for this part of the code".
And then ChatGPT would explain what the reason for the error is and give the corrected code.


