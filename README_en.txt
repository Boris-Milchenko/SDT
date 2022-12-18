Welcome to PrimaTabla!
It's tagline - 'From obsessed obsessively to obsessed' ;) or ( - you decide;

PrimaTabla is a keyboard-ruled (keyboard rules ;) ) almost (that means not) table processor to manage patients' records. Another words - the simplest patient organiser with only (maybe just in first releases) 6 columns - NUM (id), NAME, SEX, AGE, DOMICILE and DIAGNOSIS.
As it keyboard-ruled there's some rules (not all, of course ;) ):

Types:
	DIGIT - any sequence of digits (without a sign, at least, now);
	VALUE(string) - any sequence inside the ~~(~haha ahah~, for example);
	VARIABLE - starts with $ and contains no whitespaces;
	{COLUMN} - one of {num, name, sex, age, domicile, diagnosis};
	{LaMA} - one of {+, -, *, /, AND, OR, =, !=, >, <, >=, <=)} - Logic and MAth operators;
	ENUM - sequence of above(not sure you need it with VALUE, but let it be) joined by ',' or '..' (1,2..4 equals 1,2,3,4);
	LABEL - neither fish, nor flesh (but good red herring) - all, that is not matches above types. Useful for conditions and loops;
	LIDa - >> - to identify label - (Label ID + a)
	MODIFIERS - modifies command's behavior:
		'a' - apply to all tabs,
		
Flags:
	ZF - updates every LAMa opearation. 1 if result is zero (false).

Some system variables:
	$wd - working directory, which relative addresses bounds with

Commands:
	HELP: help
		Open this file.

	QUIT: q/Q [name name1...]
		name - VALUE/VARIABLE

		q - closes determined tabs, Q - exit the program.		

	OPEN: new name [name1 name2...]
		name - VALUE/VARIABLE
		
		Open (or create and open) in new tab[s] file[s] or table[s] from database with name[s], determined in parameter[s].*
	
	LENGTH: l [name]
		Echos the number of the rows of specified table.
		
	WRITE: w [destination] 
		destination - VALUE/VARIABLE
		
		Writes data from source** to destination;*** Meanwhile, previous data from destination REPLACED and data in source turns to 0 (data moves from source to destination).

	PICK: p [destination] [scope] [condition]
		destination - VALUE/VARIABLE
		scope - ENUM/DIGIT - borders within data will be picked, by default - the whole table;
		condition**** - determines terms to choose: pick or not to pick;

		Additive to more options, this command, unlike the write command, COPIES the data from source to destination (data APPENDS to end of file).

	DELETE: d [scope] [condition]
		scope - ENUM/DIGIT
		
		Delete rows from table. If has no parameters - removes file or table. 'a' modifier works as delete all rows.

	CHANGE: r [scope] [condition] value_to_replace value_with_replace [number_of_replaces] [modifiers]
		scope - ENUM
		value_to_replace - VALUE/DIGIT/VARIABLE/{COLUMN}
		value_with_replace - VALUE/DIGIT/VARIABLE
		number_of_replaces - DIGIT
		modifiers - i/e - change values, that INCLUDES value_to_replace or EQUALS it, c - replaces in all row (may in several columns)
		
		There's no pitfalls, so, i think, it's kinda clear. 

	SORT: s column order
		column - {COLUMN}
		order - asc/desc - in ascent/descent way accordingly

		Also no pitfalls.

	FILTER: f [scope] [condition]
		scope - ENUM

		Leaves in table only determined rows (use without arguments to view all rows in table again)

	INSERT: n name sex age domicile diagnosis
		All the arguments - VALUE/VARIABLE

		Nests(iNserts) row to end of a table.
		
	JUMP: jmp/jnz/jz label
		label - LABEL
		
		Jumps with[out] condition (state of ZF) to the label's address.
	
*
  How does PrimaTabla define is current value a name of table or file, you should ask? (If you didn't then come back when you do) Well, it's pretty easy - if there is '.' in value then it is a file name and in other case - it's name of table (all.csv - file name and all - table name)
 
**
  You may define source - field, to which commands will apply before command (except NEW - by obvious reasons)
  
***
  Here and further if source or destination isn't determined the current tab is used 

****
  The every separate condition must be put in '()' and follow the syntax: {COLUMN} {LaMA} VALUE/VARIABLE/DIGIT - ((name = ~John~) and (age > 33)), for example
