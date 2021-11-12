# Introduction to Voice Technology
## Assignment 3: Speaking Clock
### by Sarah Faste and Marjolein Spijkerman

### Short description
- Languages: English and Dutch
- Function: Tells you the time in a specific timezone either English or Dutch.

![speaking_clock.png](https://github.com/MarjoleinSpijkerman/Intro_to_VT_Speaking_Clock/blob/main/images/speaking_clock.png)

### Required packages and installation
The code either needs to be run in the terminal in Linux or using the Anaconda prompt in Windows. It cannot be run using Google Colab, due to the code's dependency on the tkinter python library. 

To run the code you need the following packages:
- datetime
- pytz
- numpy
- scipy
- tkinter
- sounddevice
- nltk 

### How to run the code
1. Download or clone the github page
2. Use either the terminal in Linux or the Anaconda prompt in Windows
3. Go to the "Intro_to_VT_Speaking_Clock" folder
4. start the code by running:
  - in Linux: "python3 speaking_clock.py"
  - in Anaconda: "python speaking_clock.py"
5. The code now creates a new window called speaking clock

**There are multiple things you can do with the speaking clock:**
- The clock displays the current time and the current timezone in the top of the screen
- You can change the timezone by picking a timezone from the list, followed by clicking the change timezone button
- You can click on the "What is the time?" button, to make the clock tell you the current time in English
- You can click on the "Hoe laat is het?" button, to make the clock tell you the current time in Dutch
- You can make the clock say a specific time in a specific language by:
    - First, inserting the hours in the first text bar and the minutes in the second text bar. 
    - Then, you can use the menu to indicate whether you want to hear the time in English or in Dutch. 
    - Lastly, when you click on the "Tell me the given time" button, it will then say your inserted time in the language you chose. 
    - If you insert an invalid input, it will give you an error message.
        - The input for hours should be an integer between 0 and 23
        - The input for minutes should be an integer between 0 and 59


### Description of workflow and design choices


  In this section we will be discussing our process of making the speaking clock. We will go through decision making, problem solving, and conclusion from our experience. The two of us ended up really enjoying making this project. We come from vastly different academic backgrounds, which is why we fit into the interdisciplinary nature of the assignment. 
  
  
  Marjolein is highly experienced in programming, and was able to help Sarah (who has only this current class in programming) through the process. Since we decided to do both Dutch and English, we determined that we would each be recording our native languages. We discussed the different possibilities of telling the time in our native language by dialect, but also the differences between Dutch and English. For example, Dutch uses the notation “3 over half 3” for "14:33", but English does not. While we have the concept of “10 to/until 3” we do not usually subtract from the hour by more than 20 minutes, at least in our personal knowledge of English. We used the notations in both languages like “quarter past”, “half past”, and “quarter to” in addition to exact numbers to make the clock a bit more interesting and dynamic. It also gave us more practice concatenating the individual audio signals to create the full sentence of time in numbers and time of day (ex. evening). 
  
  
  Once we had decided on a format, Marjolein was able to create the Dutch code, then help Sarah create the English version. Marjolein helped Sarah with the English code by offering advice, instruction, and editing help. In the end, we were able to create both a working version of Dutch and English clocks that follow proper syntax in each language. We used our own voices for the recordings, so the ethical implications of recording are not necessary in this case. If we were to use someone else's voice, we would need to comply with data protection requirements and the GDPR. 
  
  
  We definitely ran into several problems during the entire process, as is expected with coding. We made several differentiations between the Dutch and English versions, so we had to write separate code for both. The syntax of “twenty-one” (English) vs. “one and twenty” (Dutch) provided that our syntax would be different in each language. We created our sound files a bit differently as well. The English version was made to concatenate the numbers by only recording 1 - 20 individually, then only recording 30, 40, and 50 to put the ones and tens together to create the full number. We were testing out our results and noticed that our code was reading “40” as “4 and 0”, rather than a full integer, despite having its own wav file. In the end we needed to create a part of the function that would not read out the second number if that number was 0. Instead, it would be classified as a “tens” number and be directed to the proper wav file rather than reading the two numbers as separate integers. 
  
  
  In general, the most difficult part was designing the project. With such an open-ended request we needed to put a lot of time into planning the language, structure, code, and final product of our clock. If we had more time we would have liked to get more creative with it by trying different time formats, languages, accents, colorful interaction, and fun audio additions. In the end, it was especially rewarding to work on our code, fix all our errors, and hear the correct time reflect back to us like we planned. 



