from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class Array():
    array = []

    def __init__(self,input_array:list=None) -> None:
        """
        Creates new instances of Array

        Parameters
        ----------

        array : list
                Stores the numbers from the list into the array  

        """
        if input_array is None:
            input_array = []
        self.array = input_array


    def get(self):
        """
        Returns the array

        """
        return self.array


    def insert(self,element,index:int = None):
        """
        Inserts element into the array

        Parameters
        ----------

        element : str | bytes
                Element to be inserted
        
        index : int
                Index at which the element is to be inserted.

        """
        # If index is specified then insert at that index 
        if index == None :
            self.array.append(element)

        # Else append element to array
        else: 
            self.array.insert(index,element)


    def remove(self,element):
        """
        Removes the first occurence of an element from the array

        Parameters
        ----------

        element : str | bytes
                Element to be removed
        """
        self.array.remove(element)


    def len(self):
        """
        Returns the length of the array

        """
        return len(self.array)


    def generate(self,filename:str = "array.png",background:str="white",color:str="black",font_size:int=28,padding:int=30):
        """
        Generates the image of visualization of array

        Parameters
        ----------

        filename : str 
                Name of image file to be generated
        
        background : str
                    Background color of image
        
        color : str
                Font Color for image
        
        font_size : int
                    Size of font 
        
        padding : int
                Size of padding
        """

        # Mapping Array to text
        text = ', '.join(map(str, self.array))

        # Calculating the size required for the text
        myFont = ImageFont.truetype("arial.ttf", font_size, encoding="unic")
        text_width, text_height = myFont.getsize(text)

        # Creating a canvas image with specified parameters
        canvas = Image.new('RGB', (text_width + padding, text_height + padding), background)
        draw = ImageDraw.Draw(canvas)

        # Inserting text into the image 
        draw.text((padding//2,padding//2), text,font=myFont,fill=color)

        #Saving the image with specified filename
        canvas.save(filename)
