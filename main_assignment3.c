/*
 Author = "Alireza Khodamoradi"
*/

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include "cycletime.h"

unsigned int get_cyclecount_wrap(void){
  return get_cyclecount();
}

void init_counters_wrap(int32_t do_reset, int32_t enable_divider){
    init_counters(do_reset, enable_divider);
}

