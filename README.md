# Introduction to Voice Technology
## Assignment 3: Speaking Clock
### by Sarah Faste and Marjolein Spijkerman

### Small description of functionality
- languages: Dutch, English
- Functionality: Tells you current time 
- Possibile to change timezone

### Required packages and installation
- add list of necessary downloads to run code
- 
### How to run the code

### Description of workflow and design choices


  In this section we will be discussing our process of making the speaking clock. We will go through decision making, problem solving, and conclusion from our experience. The two of us ended up really enjoying making this project. We come from vastly different academic backgrounds, which is why we fit into the interdisciplinary nature of the assignment. 
  
  
  Marjolein is highly experienced in programming, and was able to help Sarah (who has only this current class in programming) through the process. Since we decided to do both Dutch and English, we determined that we would each be recording our native languages. We discussed the different possibilities of telling the time in our native language by dialect, but also the differences between Dutch and English. For example, Dutch uses the notation “27 minutes before 3”, but English does not. While we have the concept of “10 to/until 3” we do not usually subtract from the hour by more than 20 minutes, at least in our personal knowledge of English. We used the notations in both languages like “quarter past”, “half past”, and “quarter to” in addition to exact numbers to make the clock a bit more interesting and dynamic. It also gave us more practice concatenating them to create the full sentence of time in numbers and time of day (ex. evening). 
  
  
  Once we had decided on a format, Marjolien was able to create the Dutch code, then help Sarah create the English version. Marjolein helped Sarah with the English code by offering advice, instruction, and editing help. In the end, we were able to create both a working version of Dutch and English clocks that follow proper syntax in each language. 
  
  
  We definitely ran into several problems during the entire process, as is expected with coding. We made several differentiations between the Dutch and English versions, so we had to write separate code for both. The syntax of “twenty-one” (English) vs. “one and twenty” (Dutch) provided that our syntax would be different in each language. We created our sound files a bit differently as well. The English version was made to concatenate the numbers by only recording 1 - 20 individually, then only recording 30, 40, and 50 to put the ones and tens together to create the full number. We were testing out our results and noticed that our code was reading “40” as “4 and 0”, rather than a full integer, despite having its own wav file. In the end we needed to create a part of the function that would not read out the second number if that number was 0. Instead, it would be classified as a “tens” number and be directed to the proper wav file rather than reading the two numbers as separate integers. 
  
  
  In general, the most difficult part was designing the project. With such an open-ended request we needed to put a lot of time into planning the language, structure, code, and final product of our clock. If we had more time we would have liked to get more creative with it by trying different time formats, languages, accents, colorful interaction, and fun audio additions. In the end, it was especially rewarding to work on our code, fix all our errors, and hear the correct time reflect back to us like we planned. 



