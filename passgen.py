import secrets,string,unicodedata
__all__ = ["secrandint", "secure_shuffle", "gen_pass", "chrgen", "valpasgen",
              "validate_string", "val_pass", "cpasgen", "langpass", "Lang_range"]

#This function is the secure version of randint 
#Also note the default length of the password generation is chosen as 12 but feel free to change and explore around
l=12 #default length
def secrandint(a,b):
    ''' This is analogous to randint function and does it securely using secure.randbelow'''
    if a>b:
        raise ValueError("a must be less than or equal to b")
    return a+secrets.randbelow(b-a+1)
def secure_shuffle(text: str) -> str:
    """Shuffles a string securely using the Fisher-Yates algorithm and secrandint."""
    char_list = list(text)
    # Fisher-Yates shuffle
    for i in range(len(char_list) - 1, 0, -1):
        j = secrandint(0,i)  # Secure random index from 0 to i
        char_list[i], char_list[j] = char_list[j], char_list[i]  
        
    return "".join(char_list)

def gen_pass(l=12,d:tuple=()):
    '''This Function is the crux of the password generator and while passing tuple ensure (no of digits,no of alphabets and no of special characters)'''
    p=""
    alpha=string.ascii_letters
    digits="0123456789"
    spec="~!@#$%^&*()_-+={}[]\\|;'/?<>"
    if d ==():
        for i in range(l):
            a=secrets.choice((alpha,spec,digits))
            k=secrets.choice(a)
            p+=k
        return p
    else:
        di,a,s=d
        for i in range(di):
            p+=secrets.choice(digits)
        for i in range(a):
            p+=secrets.choice(alpha)
        for i in range(s):
            p+=secrets.choice(spec)
        return secure_shuffle(p)    
#validates the string 
def validate_string(text:str):
    '''This function validates the password given to it as a input '''
    lo= any(char in string.ascii_lowercase for char in text)
    up = any(char in string.ascii_uppercase for char in text)
    di = any(char in string.digits for char in text)
    return (lo,di,up)
#validates according to Custom  stds present in the docstring given below
def val_pass(text:str):
    '''validates password provided according to custom standards '''
    '''
    inclusion of 1 space
    inclusion of 1 uppercase
    inclusion of 1 lowercase
    inclusion of 1 special character
  * minimum of 8 characters
    '''
    l=len(text) >=8
    lo= any(char in string.ascii_lowercase for char in text)
    up = any(char in string.ascii_uppercase for char in text)
    di = any(char in string.digits for char in text)
    sp=" " in text
    spl=any(char in "!@#$%_-" for char in text)
    return lo and up and di and sp and spl and l


def chrgen(l=12):
    ''' returns a secure random generated sequence based on ASCII sequence '''
    p=""
    for i in range(l):
        p+=chr(secrandint(33,126))
    return p    
 def valpasgen(l=12):
   '''This password generator is custom password compliant'''
   if l < 8:
       raise ValueError("Password length must be at least 8 to meet custom criteria.")
   while True:
       rest = (gen_pass(l-5)
               + secrets.choice(string.ascii_lowercase)
               + secrets.choice(string.ascii_uppercase)
               + secrets.choice(string.digits)
               + secrets.choice("!@#$%_-"))
       rest = secure_shuffle(rest)
       i = secrandint(1, len(rest) - 1)   # interior position only
       p = rest[:i] + " " + rest[i:]
       if val_pass(p):
           return p
def cpasgen(l:int,s:str,n:int,o=None):
    """ 
    Creates custom passwords based on user inputs.

    Parameters:
    - l (int): Length of the password
    - s (str): Input string
    - n (str): Input number
    - o (int, optional): Bypass flag to skip extra user input
    mode 1: s + random + n | 2: all shuffled together | 3: random + s + n
    mode 0: prints the value of all the three versions
    """
    s=str(s)
    n=str(n)
    if len(s) + len(n) > l:
        raise ValueError("s and n together are longer than l")
    p=""
    ps=""
#Removes the need of input
    if o==None:    
        i=int(input("mode 1: s + random + n | 2: all shuffled together | 3: random + s + n | mode 0: prints the value of all the three versions\n"))
    else:
        i=o
    if i==1:
        for _ in range(l-len(s)-len(n)):
            ps+=(secrets.choice(string.punctuation))
        return s+ps+n   
    elif i==2:
        for _ in range(l-len(s)-len(n)):
            ps+=(secrets.choice(string.punctuation))
        return secure_shuffle(s+ps+n)  
    elif i==3:
        for _ in range(l-len(s)-len(n)):
            ps+=(secrets.choice(string.punctuation))
        return ps+s+n                
    elif i==0:
        print(cpasgen(l,s,n,1))
        print(cpasgen(l,s,n,2))
        print(cpasgen(l,s,n,3))   
        return None
    else:
        raise ValueError("mode must be 0, 1, 2 or 3")
#Example of a language dictionary which consists of a select languages feel free to add or edit languages here
Lang_range = {
    "cyrillic": (0x0410, 0x044F),
    "arabic": (0x0621, 0x064A),
    "korean": (0xAC00, 0xD7A3),
    "chinese": (0x4E00, 0x9FA5),
    "latin": (0x0041, 0x005A),
    'hiragana': (0x3040, 0x309F),
    "thai": (0x0E00, 0x0E7F),
    "hindi":(0x0900, 0x097F),
    "tamil": (0x0B80, 0x0BFF),
    "tibetan": (0x0F00, 0x0FFF),
    "sinhala": (0x0D80, 0x0DFF),
    "georgian": (0x10A0, 0x10FF),
    "ethiopic": (0x1200, 0x137F),
    "telugu": (0x0C00, 0x0C7F),
    "gujarati": (0x0A80, 0x0AFF),
    "punjabi": (0x0A00, 0x0A7F),
    "greek": (0x0370, 0x03FF)
}
POOLS = {
    name: [chr(c) for c in range(a, b + 1)
           if unicodedata.category(chr(c)) in ("Lo", "Ll", "Lu")]
    for name, (a, b) in Lang_range.items()
}
def langpass(l,lan:list=None)->str:
    """
    Generates a secure password using characters from selected language blocks.
    Use with caution as some sites do not support it.
    """
    if l < 8:
        raise ValueError("Password length must be at least 8.")
    if not lan:
        lan = Lang_range  # Default to select languages mentioned above
        
    # Validate that requested languages exist
    for i in lan:
        if i not in Lang_range:
            raise ValueError(f"Language '{i}' is not supported. Choose from: {list(Lang_range.keys())}")
    p = ""
    for _ in range(2):
        p+=chr(secrandint(48,57))
    p+=secrets.choice("!@#$%^&*()_-+,./?")    
    for _ in range(l-3):
        # Picks a random language from the user's list
        chosen_lang = secrets.choice(list(lan))
        # Generate a character from that language's Unicode range
        p += secrets.choice(POOLS[chosen_lang])
    return secure_shuffle(p)
