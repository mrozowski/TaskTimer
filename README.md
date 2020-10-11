# TaskTimer
The timer in Python. I wrote it to learn more about multithreading in Python language. For GUI I used the PyQT framework. It works really smoothly. I use it often when I study or coding because I have a tendency to forget about the world when I focus too much. And we all need to eat something or do some exercises once a while. Sitting many hours by computer is not much healthy.



![Screen](Screenshots/main.JPG?raw=true "Main")

## 1. Design 
As usual, I start programming with making design :D
Usually, I use Figma where I can easily make a nice looking interface. This step is really useful. I know exactly what elements I'll need and what will be the functionality of each button, label, or another element. Thanks to this later when I start programming I make fewer changes in code because I already thought about all elements and functionalities.
I also use Figma to export buttons and other elements that you can see in my program.

In Illustrator I made a simple logo and icon for my TaskTimer. As a sound alarm, I used a short part from some song that I found on the YouTube library. It suits much better than regular alarm sounds. Alarm sounds are so annoying! Apart from sound, I thought it would be good to add some notification or popup messages. And fortunately, I found a win10toast library that does that for me.

## 2. GUI

For the GUI framework, I used PyQT which I used already once in the previous project. However, I think it will try another GUI framework in the future. I like creating good looking GUI but I struggled a lot with PyQT. I feel most of the custom elements I made should be much easier to implement. More then half of the time I spent with this project I spent on creating GUI. Yes, maybe it's because I don't know this framework that well but some things are really difficult and not intuitive to implement. For example Dial - There are not many ways to change the look. I had to leave the default dial. I could only change the color. 


![Screen](Screenshots/run.JPG?raw=true "Main")


## 3. Coding
For this project, I used Python language. As I mentioned above the main purpose of this program was to study multithreading in Python. I thought timer should use multiple threads and I was right. My TaskTimer has a clock together with the day of the week which is run on 2nd thread and updated every 60 seconds. The main timer after the user clicks the "Start" button is run on another thread. For that purpose, I made the class MyTimer that extends threading.Thread. As a parameter, it takes labels (hours, minutes, and seconds) and a dial that will be updated every second. It takes also a method that is called when the timer is finished to set the button back to the default mode. 

![Screen](Screenshots/CustomButton.JPG?raw=true "Main")

This screenshot shows my implementation of a custom button using png files for normal, hovered, and pressed buttons. Buttons I made by myself in Figma and then I exported them as png files. In the constructor (which is hidden on this picture) I set each png file using 
```self.pixmap = QtGui.QPixmap("Graphic/button.png")```
This button has 2 states - Start and Cancel. The first state runs timer second cancel it. In the override ```paintEvent()``` method I set the button look accordingly to the button state.


You can download exe file from Google drive and check it on your computer - [Exe file](https://drive.google.com/file/d/1S-Ts1BirXW5rBvz1X18VboquWeWjvRpE/view?usp=sharing)


