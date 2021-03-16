### My 3 technical elements

##### Element 1: Function **print_report**
I've chosen to implement a function ***print_report*** to use for every report.

This function has the ability to print either a Rich table or export the file.  
For exporting there are 2 different options, *.xlsx* and *.csv*.  
They can be used at the same time, thus exporting 2 files at the "same time".  
Both are widely used for reporting.

>Without this you would have to keep repeating yourself for every report option while programming.  
>This ofcourse is not done!  
>Also without implementing the exports into this, you would have to call every function seperately.  
>This would be prone to error.

##### Element 2: File **\_\_init__**
I've chosen to place the ***\_\_init__*** file in the *superpy\_package*.  
This way it is automatically performed at first use in the used directory.  
All neccesary permanent files will be written if they don't exist.  

>Without this you would have to call the needed functions seperately.  
>The initialisation is there for a reason. This is the right place to be for this!

##### Element 3: Module **Rich**
I've chosen to import and use the external module ***Rich***.

This makes printing ***tables*** easy and improves readability.  
* The color of the values is the color *cyan* because I think this is easy on the eyes.
* The headers are kept the color *white* so they stand out against the black background.
* The background is purposely not changed, because, in my eyes, a command line interface should stay as-is: mostly color *black*.

Also this module is used for other ***printed output***.  
* Every correct output is in the color *green*.
* Every error output is in the color *red*.

>With this the readability improves greatly with the use of colors. This is much more reader-friendly.  
>Also problems are detected easier because people are triggered by red.