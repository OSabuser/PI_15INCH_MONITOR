/* 
 * Project: MACH piZeroW for UIM-6000 car station
 * Copyright (c) 2021 Dmitri Akimov.
 * 
 * This program is free software: you can redistribute it and/or modify  
 * it under the terms of the GNU General Public License as published by  
 * the Free Software Foundation, version 3.
 *
 * This program is distributed in the hope that it will be useful, but 
 * WITHOUT ANY WARRANTY; without even the implied warranty of 
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License 
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */


#include "rasp_uim.h"



#include <time.h>
#include <string.h>
#include <assert.h>
#include <ctype.h>
#include <signal.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <termios.h>
#include <stdio.h>
#include "backgroundLayer.h"
#include "imageLayer.h"
#include "key.h"
#include "loadpng.h"
#include "bcm_host.h"
#include <bcm2835.h>  




static void gpio_init(void)
{
    /*Setting up GPIO's*/
    bcm2835_gpio_fsel(GONG_PIN,BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_set_pud (GONG_PIN, BCM2835_GPIO_PUD_UP );    
}

static void play_gong(void)
{
    bcm2835_gpio_write(GONG_PIN, LOW);
    bcm2835_delay(250);
    bcm2835_gpio_write(GONG_PIN, HIGH); 
}

static uint8_t char_to_hex(char a, char b)
{
    a = (a <= '9')  ?  a - '0' : (a & 0x7) + 9;
    b = (b <= '9')  ?  b - '0' : (b & 0x7) + 9;
    
    return (a << 4) + b;
}


int main(int argc, char* argv[])
{
    /*Initialize bcm library*/
    if (!bcm2835_init()) return 1; 
    
    gpio_init();
    
    bcm_host_init();
    
 //#############################DISPLAY INIT####################################         
#if 1    
    /*DispmanX structure wrappers*/
    IMAGE_LAYER_T background_layer, floor_layer, arrow_layer;

    /*Create init image objects*/
    ImageObject_t   background = 
    {   
        .background = 0x00, 
        .layer = 1, 
        .display_number = 0, 
        .pos_X = 0, 
        .pos_Y = 0, 
    };
    
    ImageObject_t   floor = 
    {
        .background = 0x00, 
        .layer = 2, 
        .display_number = 0, 
        .pos_X = 670, 
        .pos_Y = 32, 
        .image_path = "./pictures/0.png"
    };
    
    ImageObject_t   arrow = 
    {
        .background = 0x00, 
        .layer = 3, 
        .display_number = 0, 
        .pos_X = 610, 
        .pos_Y = 480, 
        .image_path = "./pictures/BLANK_ARROW.png"
    };
    
    const char *work_mode = argv[1];
    
    
    /*Check operation mode*/
    if(strcmp(work_mode, "-static") == 0)
    {
        background.image_path = "./pictures/BACKGROUND.png";
    }
    else if (strcmp(work_mode, "-dynamic") == 0)
    {
        background.image_path = "./pictures/BLANK_SYMBOL.png";
    }
    else
    {
         fprintf(stderr, "Incorrect command line option %s\n", work_mode);
         exit(EXIT_FAILURE);
    }
    

    // Load image_2 from path
    if (loadPng(&(background_layer.image), background.image_path) == false)
    {
        fprintf(stderr, "unable to load %s\n", background.image_path);
        exit(EXIT_FAILURE);
    }
   
    if (loadPng(&(floor_layer.image), floor.image_path) == false)
    {
        fprintf(stderr, "unable to load %s\n", floor.image_path);
        exit(EXIT_FAILURE);
    }
  
    // Load image_3 from path
    if (loadPng(&(arrow_layer.image), arrow.image_path) == false)
    {
        fprintf(stderr, "unable to load %s\n", arrow.image_path);
        exit(EXIT_FAILURE);
    }
    
    printf("Images loaded successfully! \n");
    
    /*Variable for storing return codes*/
    int result = -1;
     
    DISPMANX_DISPLAY_HANDLE_T display_1;

    
    display_1 = vc_dispmanx_display_open(background.display_number);
    assert(display_1 != 0);
    
    DISPMANX_MODEINFO_T info;
    
    result = vc_dispmanx_display_get_info(display_1, &info);
    assert(result == 0);

    createResourceImageLayer(&background_layer, background.layer);
    createResourceImageLayer(&floor_layer, floor.layer);
    createResourceImageLayer(&arrow_layer, arrow.layer);

    DISPMANX_UPDATE_HANDLE_T update = vc_dispmanx_update_start(0);
    assert(update != 0);

    addElementImageLayerOffset(
        &background_layer,
        background.pos_X,
        background.pos_Y,
        display_1,
        update);
    
    addElementImageLayerOffset(
        &floor_layer,
        floor.pos_X,
        floor.pos_Y,
        display_1,
        update);
    
    addElementImageLayerOffset(
        &arrow_layer,
        arrow.pos_X,
        arrow.pos_Y,
        display_1,
        update);
    
    result = vc_dispmanx_update_submit_sync(update);
   
#endif
//##############################################################################
 
    
//##############################SERIAL INIT#################################### 
#if 1
   /*mini UART, TX-14, RX-15 */
   struct termios serial;
    
    
    
    if(argc == 1)  //No arguments typed
    {
        printf("Usage: %s [device]", argv[0]);
        return -1;
    }

    int fd = open(argv[2], O_RDWR | O_NOCTTY | O_NDELAY);
    
    if(fd == -1)
    {
            perror(argv[2]);
            return -1;
    }
    else printf("%s opening was successful \n", argv[2]);
    
    
    if(tcgetattr(fd, &serial) < 0)
    {
            perror("Getting configuration");
            return -1;
    }
    
    //Serial port setting up
    serial.c_iflag = 0;
    serial.c_oflag = 0;
    serial.c_lflag = 0;
    serial.c_cflag = 0;
    serial.c_cc[VMIN] = 0;
    serial.c_cc[VTIME] = 0;
    serial.c_cflag = B9600 | CS8 | CREAD;
    
    //Apply settings
    tcsetattr(fd, TCSANOW, &serial);
    
 #endif   
//############################################################################
    static uint8_t new_floor = 0, new_direction = 0, old_direction = 0, old_floor = 0, floor_number =0, dir_state = 0;
    static bool arrow_refresh = false, floor_refresh = false, lost_connection = false, show_one_time = true;
    static Current_State_t state = MESSAGE_PROCESSING;
    
    
    while(1)
    {
      
        while (state == MESSAGE_PROCESSING) 
        {    
            char buffer[8]; 
            int x;
            
            while ((x = read(fd, buffer, 1)) != 1 ) { }
            if (buffer[0] != '!') continue;   
		

            int rcount = read(fd, buffer, 7);
            if (buffer[6] != '#') continue; 

            if(rcount < 0)
            {
                printf("Read error!\n");
                perror(errno);
                return -1;
            }
            else if (rcount != 0) //Mesage handling
            {
                printf("received %d chars\n", rcount);
                buffer[rcount] = '\0';
                printf("Message: %s \n", buffer);
                
              if(buffer[0] == 'M')
              {
                  
                  if( (buffer[2] == 'L') && (buffer[3] == 'O') && (buffer[4] == 'S') && (buffer[5] == 'T') )
                  {
                      old_direction = 0;
                      lost_connection = true;
                      state = DISPLAY_REFRESHING;
                      printf("LOST CONNECTION!\n");
                  }
                  else
                  {
                      show_one_time = true;
                      lost_connection = false;
                  }
                  
                  if(!lost_connection)
                  {
                        //new_floor = buffer[5] - '0';
                        
                        new_floor = char_to_hex(buffer[4], buffer[5] );
                        new_direction = buffer[3] - '0';
                  
                        printf("Current floor: %d, current direction: %d\n", new_floor, new_direction);
                  
                        if(new_floor != old_floor)
                        {
                            floor_number = new_floor;
                            floor_refresh = true;
                            state = DISPLAY_REFRESHING;
                        }
                  
                        if(new_direction != old_direction)
                        {
                            dir_state = new_direction;
                            arrow_refresh = true;
                            state = DISPLAY_REFRESHING;
                        }
                  
                        old_direction = new_direction;
                        old_floor = new_floor;
    
                  }//if(!lost_connection)
                    
              }//if(buffer[0] == 'M')
                  
            }//else if (rcount != 0) 
            
        }//while (state == MESSAGE_PROCESSING) 
        
        

        while (state == DISPLAY_REFRESHING)
        {
 
            result = vc_dispmanx_update_submit_sync(update); //Update images
            state = MESSAGE_PROCESSING;// Messages handling state
            
            
            if( (lost_connection) && (show_one_time) )
            {
                    destroyImageLayer(&arrow_layer);
                    destroyImageLayer(&floor_layer);
                    
                    lost_connection = false;
                    show_one_time = false;
                    // Load image_2 from path
                    if (loadPng(&(arrow_layer.image), "./pictures/BLANK_ARROW.png") == false)
                    {
                        exit(EXIT_FAILURE);
                    }
                    createResourceImageLayer(&arrow_layer, arrow.layer);
                    
                    if (loadPng(&(floor_layer.image), "./pictures/LOST.png") == false)
                    {
                        exit(EXIT_FAILURE);
                    }
                    createResourceImageLayer(&floor_layer, floor.layer);
                 
                    DISPMANX_UPDATE_HANDLE_T update = vc_dispmanx_update_start(0);
                    assert(update != 0);
                  
                    addElementImageLayerOffset(&arrow_layer,
                               arrow.pos_X,
                               arrow.pos_Y,
                               display_1,
                               update);
                    
                    addElementImageLayerOffset(&floor_layer,
                               floor.pos_X,
                               floor.pos_Y,
                               display_1,
                               update);
                    
                    result = vc_dispmanx_update_submit_sync(update); //Update images
                    
            }
            
            
            if(arrow_refresh ==true)
            {
                printf("Arrow refresh!\n");
                arrow_refresh = false;
                 
                if((dir_state == 0) || (dir_state == 3))
                {
                    destroyImageLayer(&arrow_layer);
                    // Load image_2 from path
                    if (loadPng(&(arrow_layer.image), "./pictures/BLANK_ARROW.png") == false)
                    {
                        exit(EXIT_FAILURE);
                    }
                    createResourceImageLayer(&arrow_layer, arrow.layer);
                 
                    DISPMANX_UPDATE_HANDLE_T update = vc_dispmanx_update_start(0);
                    assert(update != 0);
                    
                    addElementImageLayerOffset(&arrow_layer,
                               arrow.pos_X,
                               arrow.pos_Y,
                               display_1,
                               update);
                    result = vc_dispmanx_update_submit_sync(update); //Update images
                }
                else if(dir_state == 1) 
                {
                         
                    destroyImageLayer(&arrow_layer);
                // Load image_2 from path
                if (loadPng(&(arrow_layer.image), "./pictures/ARROW_UP.png") == false)
                {
                    exit(EXIT_FAILURE);
                }
                createResourceImageLayer(&arrow_layer, arrow.layer);
                 
                    DISPMANX_UPDATE_HANDLE_T update = vc_dispmanx_update_start(0);
                    assert(update != 0);
                
                    addElementImageLayerOffset(&arrow_layer,
                               arrow.pos_X,
                               arrow.pos_Y,
                               display_1,
                               update);
                    
                    result = vc_dispmanx_update_submit_sync(update); //Update images
                }
                else if(dir_state == 2) 
                {

                    destroyImageLayer(&arrow_layer);
                // Load image_2 from path
                if (loadPng(&(arrow_layer.image), "./pictures/ARROW_DOWN.png") == false)
                {
                    exit(EXIT_FAILURE);
                }
                createResourceImageLayer(&arrow_layer, arrow.layer);
                 
                    DISPMANX_UPDATE_HANDLE_T update = vc_dispmanx_update_start(0);
                    assert(update != 0);
                
                    addElementImageLayerOffset(&arrow_layer,
                               arrow.pos_X,
                               arrow.pos_Y,
                               display_1,
                               update);
                    
                    result = vc_dispmanx_update_submit_sync(update); //Update images
                }
                
                
            }
            
            if(floor_refresh == true)
            {
                floor_refresh = false;
                printf("Floor refresh!\n");
                
                char str[40];
                sprintf(str, "./pictures/%d.png", floor_number);
                    
                destroyImageLayer(&floor_layer);
                // Load image_2 from path
                if (loadPng(&(floor_layer.image), str) == false)
                {
                    exit(EXIT_FAILURE);
                }
                createResourceImageLayer(&floor_layer, floor.layer);
                 
                    DISPMANX_UPDATE_HANDLE_T update = vc_dispmanx_update_start(0);
                    assert(update != 0);
                
                    addElementImageLayerOffset(&floor_layer,
                               floor.pos_X,
                               floor.pos_Y,
                               display_1,
                               update);
                    
                    result = vc_dispmanx_update_submit_sync(update); //Update images
                
            }
            

            
            
        }
      
    }
    
    //Never reach this lines
    destroyImageLayer(&arrow_layer);
    destroyImageLayer(&floor_layer);
    destroyImageLayer(&background_layer);

    result = vc_dispmanx_display_close(display_1);
    assert(result == 0);

   

    return 0;
}





    
