import java.util.*;
import java.io.*;
class project2 {
    public static void main(String[] args) throws FileNotFoundException {
    
    //initializing boolean and scanner
    Boolean yes = true; 
    Scanner read = new Scanner(System.in);
    String newF;
    
    //getting the file name
    System.out.println("Enter your file name");
    File f = new File(read.nextLine());
    
    //Starting the loop, seeing if f exists
    while (yes==true){        
    if(!f.exists())
    //if the file doesn't exist, it will ask for a different one and reloop
      System.out.println("File does not exist, try a different one.");
    
    else{
    CharReader cr = new CharReader(f);//new CharReader object 
    
    cr.next();
    System.out.println(cr.Program());
    
    /* Project1
    //Implementing the lexical analizer
    cr.next();//reads the next lexem and prints the info
    System.out.println(cr.position()+cr.kind()+cr.value());
    while (!cr.kind().equals("'end-of-text'")) 
    {//While kind isn't 'end-of-text'
      cr.next();//reads the next Lexem and print the info
      System.out.println(cr.position()+cr.kind()+cr.value());
    }
    */
    }
    
    //Getting the next file for the next loop
    System.out.println("What is your next file? (Enter 'quit' or 'exit' to end)");
    newF = read.nextLine();//requesting a new file or request to end
    if(newF.equals("quit")||newF.equals("exit"))
      yes=false; //seeing if it was a request to end
    else
      f=new File(newF);//setting f to the new file for the next itteration of the loop
    }}
    
static class CharReader{
    //Initializing charRader variables
    private String currentChar = "";//current character  
    private String currentLine = "";//current line of characters
    private int lineNum=0;//current line index
    private int charNum=0;//current char index
    private BufferedReader bf; //initializing bufferedreader
    //Declarations for project1
    private String currentLexem = "";//current Lexem
    private String currentKind = "";//current kind
    private int lexNum=0;//Index of first character in the current lexem
    private int lexLineNum=0;//Index of the line of the current lexem
    //New declerations for project2
    private File file;
    
    //Initializing charReader
    CharReader(File f)throws FileNotFoundException
    {//intitializing the functions
      this.bf = new BufferedReader(new FileReader(f));
      file=f;
      //opening BufferReader to read the file
      nextLine();//getting the next line ready
    }
    
    //Project2:
    
    
    // Starting function, goes through each function
    public boolean Program(){//
      match("program");
      match("ID");
      match(":");
      Body();
      match(".");
      return true;
    }
    
    // Match function, matches the symbol and gives the next lexem,
    //but creates an error if the current lexem doesn't match the right symbol
    void match(String t){//
      if(t.equals(currentKind)){
         next();
      }
      else{
         System.out.println(file+":"+position()+">>>>> Bad Symbol '"
               +currentKind+"' expected '"+t+"'");
         System.exit(0);
      }
    }
    
    // Matches multiple symbols at once, makes sure one of them work,
    // creates an error if none match
    void asert(String[] s){
      boolean t=false;
      for(int i=0; i<s.length; i++){
         if(s[i].equals(currentKind)){
            match(s[i]);
            t=true;
            break;
         }
      }
      if(t==false)
         error(s);
    }
    
    // body function
    // If the current lexem is a bool or in, then there are declerations
    // Then go to Statements 
    void Body(){//
      if(currentKind.equals("bool") || currentKind.equals("int"))
         Declarations();
      Statements();
    }
    
    // loops through declerations
    void Declarations(){//
      Declaration();
      while(currentKind.equals("bool") || currentKind.equals("int")){
         Declaration();
      }
    }
    
    // loops through statements 
    void Statements(){//
      Statement();
      while(currentKind.equals(";")){
         match(";");
         Statement();
      }
    }
    
    // Each decleration starts with bool or int
    // Then matches ID's seperated by comments and ended with a semicolen
    void Declaration(){//
      asert(new String[]{"bool","int"});
      match("ID");
      while(currentKind.equals(",")){
         match(",");
         match("ID");
      }
      match(";");
     }
    
    // There are 4 types of statements
    // Finds which statement it is
    // Gives an error if it doesn't match any
    void Statement(){//
      if(currentKind.equals("ID"))
         AssignmentStatement();
      else if(currentKind.equals("if"))
         ConditionalStatement();
      else if(currentKind.equals("while"))
         IterativeStatement();
      else if(currentKind.equals("print"))
         PrintStatement();
      else
         error(new String[]{"IDENTIFIER","if","while","print"});//Error
    }
    
    // Checks syntax for assigning a value to an ID
    void AssignmentStatement(){//
      match("ID");
      match(":=");
      Expression();
    }
    
    // Checks syntax for if then statements 
    void ConditionalStatement(){//
      match("if");
      Expression();
      match("then");
      Body();
      if(currentKind.equals("else")){
         match("else");
         Body();
      }
      match("end");
    }
    
    // Checks syntax for for while statements 
    void IterativeStatement(){//
      match("while");
      Expression();
      match("do");
      Body();
      match("end");
    }
    
    // Checks syntax for print statements 
    void PrintStatement(){//
      match("print");
      Expression();
    }
    
    // loops through simple expressions seperated by relational opertors
    void Expression(){
      SimpleExpression();
      if(currentKind.equals("<")||currentKind.equals("=<")||currentKind.equals("=")||
            currentKind.equals("!=")||currentKind.equals(">=")||currentKind.equals(">")){
         RelationalOperator();
         SimpleExpression();
      }
    }
    
    // loops through terms seperated by additives opertors
    void SimpleExpression(){
      Term();
      while(currentKind.equals("+")||currentKind.equals("-")||currentKind.equals("or")){
         AdditiveOperator();
         Term();
      }
    }
    
    // Asserts symbols for rational operators
    void RelationalOperator(){
      asert(new String[]{"<","=<","=","!=",">=",">"});
    }
    
    // loops through factors seperated by multiplicative opertors
    void Term(){
      Factor();
      while(currentKind.equals("*")||currentKind.equals("/")||
            currentKind.equals("mod")||currentKind.equals("and")){
         MultiplicativeOperator();
         Factor();
      }
    }
    
    // asserts symbols for additive operators
    void AdditiveOperator(){
      asert(new String[]{"+","-","or"});
    }
    
    // gives a possible unary operator then a mandatory either
    // unary operator, ID, ( expressions ), or litteral
    // If none match, then it gives an error
    void Factor(){
      if(currentKind.equals("-")||currentKind.equals("not"))
         UnaryOperator();
      if(currentKind.equals("ID"))
         match("ID");
      else if(currentKind.equals("(")){
         match("(");
         Expression();
         match(")");
      }
      else if(currentKind.equals("NUM")||currentKind.equals("true")||
            currentKind.equals("false"))
         Literal();
      else
         error(new String[]{"IDENTIFIER","(","INTEGER","true","false","-","not"});//Error
    }
    
    // Asserts symbols for multiplicative operator
    void MultiplicativeOperator(){
      asert(new String[]{"*","/","mod","and"});
    }
    
    // Asserts symbols for unary operator
    void UnaryOperator(){
      asert(new String[]{"-","not"});
    }
    
    // Eithr is a num of a boolean litteral
    void Literal(){
      if(currentKind.equals("NUM"))
         match("NUM");
      else
         BooleanLiteral();
    }
    
    // asserts symbols for boolean literals 
    void BooleanLiteral(){
      asert(new String[]{"true","false"});
    }
    
    //This function deals with errors 
    void error(int x)
    {
      if(x==1)//Illegal Character Error
      {  //Print error messege then exit the program
         System.out.println(position()+">>>>> Illegal character '" + currentChar+"'");
         System.exit(0);
      }
    }
    
    //Error for printing a messege with many expected symbols
    // Loops through symbols in the string to print them in the 
    // error messege. Then exits the program. 
    void error(String[] s){
      System.out.print(file+":"+position()+">>>>> Bad Symbol '"
               +currentKind+"' expected one of");
      for(int i=0; i<s.length-1; i++)
         System.out.print(" '"+s[i]+"'");
      System.out.println(" and '"+s[s.length-1]+"'");
      System.exit(0);
    }
    
    //------------------------------------------------------------------
    //Project 1:
    
    /*reads the next lexeme in the input file. 
    (This will not return any thing: it will cause
    the next token to be recognized.)*/
    public void next()
    {
      currentLexem="";//Initializing the current lexem to be empty
      lexNum=charNum;//Initializing the new char and line number
      lexLineNum=lineNum;
      //We have reached the end of text
      if(currentChar.equals("$"))//If the current char is $
      {
         currentLexem="$";//The current lexem is $ 
         currentKind="end-of-text";
      }
      //Checking for whitespace. If there is, the program will take
      //the next char and run next again to get the nextLexem.
      else if(currentChar.equals(" ")||currentChar.equals(" ")||currentChar.equals(""))
      {
         nextChar();
         next();
      }
      //Checking if the next Lexem is an ID or symbol
      else if(IsLetter(currentChar))
      {
         currentKind="ID";//Assuming it is an ID
         while(IsLetter(currentChar)||IsDigit(currentChar)||currentChar.equals("_"))
            {//Keeps checking to see when the word ends
               currentLexem+=currentChar;
               //The next char will be added to the current lexem
               nextChar();
            }//find the nextChar for the next round
         if(IsKeyword(currentLexem))//if the currentLexem is a keyword
            currentKind=currentLexem;//the kind is updated to be that keyword
      }
      //now checking for an integer
      else if(IsDigit(currentChar))
      {
         currentKind="NUM";//Kind is set to NUM since only NUMs start with digits
         while(IsDigit(currentChar))
            {//As long as the current char is a number
               currentLexem+=currentChar;
               //current char is added onto the currentLexem
               nextChar();
            }//nextChar is found for the next round
      }//Now checking if s is a symbol
      else if(IsSymbol(currentChar)||currentChar.equals("!"))
      {//If the currentChar is '!', we check for that too since '!' is not a stand alone keyword
         currentLexem=currentChar;//The current lexem is the currentChar
         nextChar();//Finding the next char
         //If the next char is part of a keyword, we need to check for that
         //And read the char after for the next round
         if(currentLexem.equals(":"))//Checking if the lexem is :,=,!,>
         {//since they can be followed by another char
            if(currentChar.equals("="))//testing if it's the right value
            {
               currentLexem+=currentChar;//If it's not nothing happens for :,=,>
               //Update the currentLexem if it is
               nextChar(); //reading the next char for the next round
            }//Otherwise we already have the current lexem and nextChar ready
            currentKind=currentLexem;//Since it is a symbol the current kind will be the current lexem
         }
         else if(currentLexem.equals("="))//same for equals
         {
            if(currentChar.equals("<"))
            {
               currentLexem+=currentChar;
               nextChar();//reading the char for the next round
            }
            currentKind=currentLexem;//Since it is a symbol the current kind will be the current lexem
         }
         else if(currentLexem.equals("!"))//Same for ! except if there is not =
         {//Following it, it will produce an error messege
            if(currentChar.equals("="))
            {
               currentLexem+=currentChar;
               nextChar(); //reading the next char for the next round
               currentKind=currentLexem;//Update the kind since it's a symbol
            }
            else //But if ! is not followed by = then there is an error
            error(1);//Error(1) means the character is invalid
         }
         else if(currentLexem.equals(">"))//Same for >
         {
            if(currentChar.equals("="))
            {
               currentLexem+=currentChar;
               nextChar(); //reading the next char for the next round
            }
            currentKind=currentLexem;
         }
         else if(currentChar.equals("/"))
         {//If / is followed by /, the // means comment out the whole line
            if(currentChar.equals("/"))
            {
               nextLine();//We take the next line, then run through 
               //next() again since a comment is ignored
               next();//This will give us the next lexem
               //We don't have to worry about resetting the lexem since the next()
               //Function will do it for us
               return;
            }
         }
         currentKind=currentLexem;//Since it wasn't a comment
      }
      else //Since the character wasn't the begining of an ID, keyeword, NUM, symbol, whitespace, or end-of-text
         error(1);//Error 1 is symbol not recognized
    }
    
    /*returns the kind of the lexeme that was just read.*/
    public String kind()
    {//Bellow are my personal notes
    //"ID": letter (letter|digit|"_")
    //"NUM": digits
    //keywords and symbols
    //"end-of-text": "$"
      return "'"+currentKind+"'";//Returns currentKind surrounded by '
    }
    
    /*returns the value of the lexeme 
    (if it is an “ID” or a “NUM”).*/
    public String value()
    {
      if(currentKind.equals("ID")||currentKind.equals("NUM"))
      return currentLexem;//If the current kind is an ID of NUM,
      return "";//That will be the value, otherwise empty. 
    }
    
    /*returns the position of the lexeme that was just read.*/
    public String position()
    {//prints the position of the current char
      return lexLineNum+":"+lexNum+":";
    }
    
    //Finding out if k is a keyword and returning true if it is
    Boolean IsKeyword(String k)
    {
      if(k.equals("program")||k.equals("bool")||k.equals("int")||k.equals("if")||
      k.equals("then")||k.equals("else")||k.equals("end")||k.equals("while")||
      k.equals("do")||k.equals("print")||k.equals("or")||k.equals("mod")||
      k.equals("and")||k.equals("not")||k.equals("false")||k.equals("true"))
      return true;
      return false;
    }
    
    //Finding out if s is a symbol and returning true if it is
    Boolean IsSymbol(String s)
    {
      if(s.equals(":")||s.equals(".")||s.equals(",")||s.equals(";")||s.equals(":=")||
      s.equals("<")||s.equals("=<")||s.equals("=")||s.equals("!=")||s.equals(">=")||
      s.equals(">")||s.equals("+")||s.equals("-")||s.equals("*")||s.equals("/")||
      s.equals("(")||s.equals(")")||s.equals("-"))
      return true;
      return false;
    }
    
    //Finding out if x is a digit and returning true if it is
    Boolean IsDigit(String x)
    {
      if(x.equals("0")||x.equals("1")||x.equals("2")||x.equals("3")||x.equals("4")||
      x.equals("5")||x.equals("6")||x.equals("7")||x.equals("8")||x.equals("9"))
      return true;
      else return false;
    }
    
    //Finding out if x is a letter and returning true if it is
    Boolean IsLetter(String x)
    {
      if(x.equals("a")||x.equals("b")||x.equals("c")||x.equals("d")||x.equals("e")||
      x.equals("f")||x.equals("g")||x.equals("h")||x.equals("i")||x.equals("j")||
      x.equals("k")||x.equals("l")||x.equals("m")||x.equals("n")||x.equals("o")||
      x.equals("p")||x.equals("q")||x.equals("r")||x.equals("s")||x.equals("t")||
      x.equals("u")||x.equals("v")||x.equals("w")||x.equals("x")||x.equals("y")||
      x.equals("z")||x.equals("A")||x.equals("B")||x.equals("C")||x.equals("D")||
      x.equals("E")||x.equals("F")||x.equals("G")||x.equals("H")||x.equals("I")||
      x.equals("J")||x.equals("K")||x.equals("L")||x.equals("M")||x.equals("N")||
      x.equals("O")||x.equals("P")||x.equals("Q")||x.equals("R")||x.equals("S")||
      x.equals("T")||x.equals("U")||x.equals("V")||x.equals("W")||x.equals("X")||
      x.equals("Y")||x.equals("Z"))
      return true;
      else return false;
    }
    
    //reads the next character
    void nextChar()
    {
      if(currentChar=="$")//If the char $, we have reached the end of text. 
         currentChar.equals("$");//Returning $ since there is no next char
      else if(charNum >= currentLine.length())//seeing if the line is at the end
         nextLine();//The nextLine() function will increment the line
      else{//When the nextChar function is called it will give a new line and whitespace
      currentChar=currentLine.substring(charNum, charNum+1);
      charNum++;}}//The new char is the next char in line, a substring of the line
    
    //gets the next line
    void nextLine()
    {
      try{//trying: setting the current line to the next line in file
      currentLine=bf.readLine();
      if (currentLine!= null){
      lineNum++; //If the current line is not empty, 
      charNum=0; //the line will be incremented, the position set to 0, 
      currentChar="";}//and the current char is blank to signify a new line.
      else{//the current char becomes '$', signifying the end of the file
      currentChar="$";}}
      catch(IOException e) {//catching errors
        System.out.println("An error occurred while reading the file: " + e.getMessage());
        e.printStackTrace();
    }}
}}
