Sapphire is an easy programming language to learn, created by GitHub@CodeyWaffle, with the help of Google Gemini and ChatGPT, built on the basics of Python and C++ (Windows Only)
The Sapphire programming language is designed as a fast, simple, and portable tool with native UI capabilities [1]. It is licensed under MIT, allowing for building, selling, and remixing, but includes a "Be a good guy" policy emphasizing responsible use, prohibiting the creation of weapons or harmful software, requiring credit for major projects or forks, discouraging harassment automation, and promoting innovation over imitation [1]. Visit the Sapphire Programming Language GitHub repository for more details.

Executing the code
Sapphire 15 and beyond:
    Install pygamece or pygame and pygame-supported Python versions
    Download Sapphire(version) in a ZIP or directly in a folder, then extract it
    Open the launchSapphire.bat in the folder
    You can run and save the code directly on the SapphireStudio(launches when you clicked the .bat file)
before Sapphire 15, not including:
    Download Sapphire.py.
    Code a Sapphire code in any notepad application and save it as a .sp file.
    Put the Sapphire.py  interpreter in the same folder as your .sp file project.
    Change destination in your computer terminal to the folder that saved the Sapphire files.
    enter python Sapphire12.py  YourProject.sp 
    You can see your project running.
    
New Commands: (Sapphire 15 and beyond)

// - description
Variables
var type(name){value} - Creates a variable (int, flt, str, bol, lst).
Constants
const var type(name){value} - Creates a read-only variable that cannot be changed.
Jumping
jump.n - Immediately stops the current block and starts executing the area named n.
Defining Areas
def area (n) { } - Creates a named logic block for jumps or organization.
Fixed Loops
loop(n) { } - Executes the code inside $n$ times during a single main cycle.
Condition Loops
setLoopUntil(cond) { } - Runs until the condition evaluates to true.
State Loops
setLoopWhen(cond) { } - Runs as long as the condition remains true.
Conversion
convert(type1 var n){type2} - Migrates a variable from one data type to another.
Output
print() and println() - Sends data to the Studio console.
Graphics
set_screen(w, h), draw_rect(COL, x, y, w, h), and update_display().
Core Rules & Logic
Variable Declaration: Only one variable should be declared per set of brackets.
Boolean Syntax: All boolean logic must use lowercase letters (e.g., true, false, &&, ||).
Conditionals: if statements only execute the code block if the condition is strictly true.
Graphics Sequence: You must call set_screen() before using any drawing commands like draw_rect.
Encoding: Your files support full UTF-8, allowing you to use emojis and special symbols in strings.
Workspace Management: Always use the .bat file to ensure the latest library version is copied into your project folder.

Old Basic code structure:  (before Sapphire 15, not including)

.start.program{}
.setup{}
.main{}
.end.program

Old Commands: (before Sapphire 15, not including)

// - description
setLoop(n){until(a){b}} - same as for(n, a, b) in C++
jump.n - jump to an area named n
def area (n) - create an area n
loop(n) - loop n times in one .main cycle
var int (n){1} - create an integer variable n and n = 1
print() - print something
println() - print something and change line
const var int (n){1} - create a constant integer variable n and n = 1
convert(int var n){str} - convert an integer variable n into string
basic boolean logics
numerical calculations

Rules:
Only one variable in the same brackets
If satements only run if condition = true (not false)
Boolean logics in lowercase letters
